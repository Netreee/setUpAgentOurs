import inspect
import json
import os
import time
from types import SimpleNamespace
from typing import Any, Dict, List, Optional, Tuple

from bytedance.fornax.infra import FornaxClient, initialize
from bytedance.fornax.infra.prompt_service import ExecutePromptParam
from bytedance.fornax.infra.prompt_service.types import (
    AccountMode,
    FunctionCall,
    Message,
    MessageType,
    ModelConfig,
    Tool,
    ToolCall,
    ToolCallCombine,
    ToolCallConfig,
    ToolChoiceSpecification,
    ToolChoiceType,
    ToolCombine,
    ToolFunction,
    ToolType,
)


_ROLE_TO_TYPE = {
    "system": MessageType.SYSTEM,
    "user": MessageType.USER,
    "assistant": MessageType.ASSISTANT,
    "tool": MessageType.TOOL,
}
_EXECUTE_PROMPT_FIELDS: Optional[set[str]] = None
_MESSAGE_FIELDS: Optional[set[str]] = None


def _signature_fields(target: Any) -> set[str]:
    try:
        signature = inspect.signature(target)
    except (TypeError, ValueError):
        return set()
    return set(signature.parameters.keys())


def _execute_prompt_fields() -> set[str]:
    global _EXECUTE_PROMPT_FIELDS
    if _EXECUTE_PROMPT_FIELDS is None:
        _EXECUTE_PROMPT_FIELDS = _signature_fields(ExecutePromptParam)
    return _EXECUTE_PROMPT_FIELDS


def _message_fields() -> set[str]:
    global _MESSAGE_FIELDS
    if _MESSAGE_FIELDS is None:
        _MESSAGE_FIELDS = _signature_fields(Message)
    return _MESSAGE_FIELDS


def _parse_account_mode(value: Optional[Any]) -> Optional[AccountMode]:
    if value is None:
        return None
    if isinstance(value, AccountMode):
        return value
    if isinstance(value, int):
        try:
            return AccountMode(value)
        except ValueError:
            return AccountMode.UNDEFINED
    text = str(value).strip().upper()
    if text == "SHARE":
        return AccountMode.SHARE
    if text == "CUSTOM":
        return AccountMode.CUSTOM
    if text == "UNDEFINED":
        return AccountMode.UNDEFINED
    return None


def _content_to_text(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: List[str] = []
        for part in content:
            if not isinstance(part, dict):
                continue
            if part.get("type") == "text":
                text = part.get("text", "")
                if text:
                    parts.append(text)
        return "".join(parts)
    return str(content)


def _convert_messages(messages: List[Dict[str, Any]]) -> Tuple[List[Message], Message]:
    if not messages:
        raise ValueError("messages must be a non-empty list")
    system_prefix = ""
    normalized: List[Tuple[str, str, Optional[str], Optional[Any], Optional[Any]]] = []
    for msg in messages:
        if not isinstance(msg, dict):
            raise TypeError("each message must be a dict")
        role = msg.get("role", "user")
        content = _content_to_text(msg.get("content"))
        tool_call_id = msg.get("tool_call_id")
        tool_calls = msg.get("tool_calls")
        function_call = msg.get("function_call")
        if function_call is not None and tool_calls is None:
            tool_calls = _openai_function_call_to_tool_calls(function_call)
            function_call = None
        if role == "system":
            if content:
                system_prefix += content + "\n\n"
            continue
        normalized.append((role, content, tool_call_id, tool_calls, function_call))
    if not normalized:
        normalized = [("user", system_prefix.strip(), None, None, None)]
        system_prefix = ""
    if system_prefix:
        first_role, first_content, tool_call_id, tool_calls, function_call = normalized[0]
        normalized[0] = (first_role, f"{system_prefix}{first_content}", tool_call_id, tool_calls, function_call)
    fornax_messages: List[Message] = []
    message_fields = _message_fields()
    for role, content, tool_call_id, tool_calls, function_call in normalized:
        message_type = _ROLE_TO_TYPE.get(role, MessageType.USER)
        if message_type == MessageType.SYSTEM:
            message_type = MessageType.USER
        message_kwargs: Dict[str, Any] = {"message_type": message_type, "content": content}
        if tool_call_id is not None:
            if "tool_call_id" not in message_fields:
                raise NotImplementedError("Fornax Message does not support tool_call_id.")
            message_kwargs["tool_call_id"] = tool_call_id
        if tool_calls is not None:
            if "tool_calls" not in message_fields:
                raise NotImplementedError("Fornax Message does not support tool_calls.")
            message_kwargs["tool_calls"] = _openai_tool_calls_to_fornax(tool_calls)
        fornax_messages.append(Message(**message_kwargs))
    return fornax_messages[:-1], fornax_messages[-1]


def _build_model_config(
    model_name: Optional[str],
    temperature: Optional[float],
    max_tokens: Optional[int],
    top_p: Optional[float],
    frequency_penalty: Optional[float],
    presence_penalty: Optional[float],
) -> Optional[ModelConfig]:
    if (
        model_name is None
        and temperature is None
        and max_tokens is None
        and top_p is None
        and frequency_penalty is None
        and presence_penalty is None
    ):
        return None
    return ModelConfig(
        name=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )


def _extract_content(response: Any) -> str:
    if response and response.item and response.item.content:
        return response.item.content
    return ""


def _extract_usage(response: Any) -> Optional[Dict[str, int]]:
    if not response or not response.item or not response.item.token_consumption:
        return None
    usage = response.item.token_consumption
    if usage.input_token is None or usage.output_token is None:
        return None
    return {
        "prompt_tokens": int(usage.input_token),
        "completion_tokens": int(usage.output_token),
        "total_tokens": int(usage.input_token) + int(usage.output_token),
    }


def _extract_tool_calls(response: Any) -> Optional[List[Dict[str, Any]]]:
    if not response or not response.item:
        return None
    tool_calls = getattr(response.item, "tool_calls", None)
    if tool_calls:
        return [_fornax_tool_call_to_openai(call) for call in tool_calls]
    tool_call = getattr(response.item, "tool_call", None)
    if tool_call:
        return [_fornax_tool_call_to_openai(tool_call)]
    return None


def _extract_function_call(response: Any) -> Optional[Any]:
    if not response or not response.item:
        return None
    function_call = getattr(response.item, "function_call", None)
    if function_call:
        if isinstance(function_call, dict):
            return function_call
        if hasattr(function_call, "model_dump"):
            payload = function_call.model_dump()
            return {"name": payload.get("name"), "arguments": payload.get("arguments")}
        if hasattr(function_call, "dict"):
            payload = function_call.dict()
            return {"name": payload.get("name"), "arguments": payload.get("arguments")}
        return {"name": getattr(function_call, "name", None), "arguments": getattr(function_call, "arguments", None)}
    return None


def _fornax_tool_call_to_openai(tool_call: Any) -> Dict[str, Any]:
    if isinstance(tool_call, dict) and "function" in tool_call and "type" in tool_call:
        return tool_call

    if isinstance(tool_call, dict) and "tool_call" in tool_call:
        tool_call = tool_call["tool_call"]
    if hasattr(tool_call, "tool_call"):
        tool_call = tool_call.tool_call

    if isinstance(tool_call, dict):
        call_id = tool_call.get("id")
        func = tool_call.get("function") or tool_call.get("function_call") or {}
        return {
            "id": call_id,
            "type": "function",
            "function": {
                "name": func.get("name"),
                "arguments": func.get("arguments"),
            },
        }

    call_id = getattr(tool_call, "id", None)
    func_call = getattr(tool_call, "function_call", None)
    name = getattr(func_call, "name", None) if func_call else None
    arguments = getattr(func_call, "arguments", None) if func_call else None
    return {
        "id": call_id,
        "type": "function",
        "function": {"name": name, "arguments": arguments},
    }


def _openai_tool_calls_to_fornax(tool_calls: Any) -> List[ToolCallCombine]:
    if not isinstance(tool_calls, list):
        raise ValueError("tool_calls must be a list.")
    converted: List[ToolCallCombine] = []
    for call in tool_calls:
        if isinstance(call, ToolCallCombine):
            converted.append(call)
            continue
        if isinstance(call, ToolCall):
            converted.append(ToolCallCombine(tool_call=call))
            continue
        if not isinstance(call, dict):
            raise ValueError("Each tool_call must be a dict.")
        converted.append(_openai_tool_call_dict_to_fornax(call))
    return converted


def _openai_tool_call_dict_to_fornax(tool_call: Dict[str, Any]) -> ToolCallCombine:
    tool_type = tool_call.get("type")
    if tool_type not in (None, "function", "tool_call"):
        raise ValueError(f"Unsupported tool call type: {tool_type}")
    tool_id = tool_call.get("id")
    function = tool_call.get("function") or tool_call.get("function_call") or {}
    name = function.get("name") or tool_call.get("name")
    if not name:
        raise ValueError("Tool call missing function name.")
    arguments = function.get("arguments")
    if arguments is None:
        arguments = tool_call.get("args")
    if arguments is None:
        arguments = tool_call.get("arguments")
    if arguments is not None and not isinstance(arguments, str):
        arguments = json.dumps(arguments)
    function_call = FunctionCall(name=name, arguments=arguments)
    return ToolCallCombine(tool_call=ToolCall(id=tool_id, type=ToolType.FUNCTION, function_call=function_call))


def _openai_function_call_to_tool_calls(function_call: Any) -> List[ToolCallCombine]:
    if isinstance(function_call, dict):
        name = function_call.get("name")
        arguments = function_call.get("arguments")
    else:
        name = getattr(function_call, "name", None)
        arguments = getattr(function_call, "arguments", None)
    if not name:
        raise ValueError("function_call missing function name.")
    if arguments is not None and not isinstance(arguments, str):
        arguments = json.dumps(arguments)
    call = ToolCall(
        id="fornax_function_call",
        type=ToolType.FUNCTION,
        function_call=FunctionCall(name=name, arguments=arguments),
    )
    return [ToolCallCombine(tool_call=call)]


def _build_response(
    content: str,
    model: str,
    usage: Optional[Dict[str, int]],
    tool_calls: Optional[List[Dict[str, Any]]] = None,
    function_call: Optional[Any] = None,
) -> Any:
    created = int(time.time())
    message = SimpleNamespace(role="assistant", content=content)
    if tool_calls is not None:
        message.tool_calls = tool_calls
    if function_call is not None:
        message.function_call = function_call
    finish_reason = "tool_calls" if tool_calls else "stop"
    choice = SimpleNamespace(index=0, message=message, finish_reason=finish_reason)
    return SimpleNamespace(
        id=f"fornax-{created}",
        object="chat.completion",
        created=created,
        model=model,
        choices=[choice],
        usage=SimpleNamespace(**usage) if usage else None,
    )


class FornaxOpenAI:
    def __init__(
        self,
        *,
        ak: str,
        sk: str,
        prompt_key: Optional[str] = None,
        prompt_version: Optional[str] = None,
        model_name: Optional[str] = None,
        account_mode: Optional[Any] = None,
        fornax_custom_region: str = "",
        allow_custom_model_config: bool = False,
        env: Optional[Dict[str, str]] = None,
        conn_timeout: int = 1,
        read_timeout: int = 10,
    ) -> None:
        if env:
            os.environ.update({k: str(v) for k, v in env.items() if v is not None})
        if not ak or not sk:
            raise ValueError("ak and sk are required for FornaxOpenAI")
        self._prompt_key = prompt_key
        self._prompt_version = prompt_version
        self._model_name = model_name
        self._account_mode = _parse_account_mode(account_mode)
        self._allow_custom_model_config = allow_custom_model_config

        initialize(
            ak,
            sk,
            conn_timeout=conn_timeout,
            read_timeout=read_timeout,
            fornax_custom_region=fornax_custom_region or "",
        )
        self.chat = _Chat(self)

    def _create_chat_completion(
        self,
        *,
        model: str,
        messages: List[Dict[str, Any]],
        max_tokens: Optional[int],
        temperature: Optional[float],
        top_p: Optional[float],
        frequency_penalty: Optional[float],
        presence_penalty: Optional[float],
        tools: Optional[List[Dict[str, Any]]],
        tool_choice: Optional[Any],
        functions: Optional[List[Dict[str, Any]]],
        function_call: Optional[Any],
        stream: bool,
    ) -> Any:
        if stream:
            raise NotImplementedError("streaming is not supported in FornaxOpenAI")
        prompt_key = self._prompt_key or model
        contexts, message = _convert_messages(messages)
        model_config = None
        if self._allow_custom_model_config:
            model_config = _build_model_config(
                self._model_name,
                temperature,
                max_tokens,
                top_p,
                frequency_penalty,
                presence_penalty,
            )
        params_kwargs: Dict[str, Any] = {
            "prompt_key": prompt_key,
            "version": self._prompt_version,
            "message": message,
            "contexts": contexts,
            "account_mode": self._account_mode,
            "custom_model_config": model_config,
        }
        if tools is not None or tool_choice is not None or functions is not None or function_call is not None:
            if tools is not None and functions is not None:
                raise ValueError("Provide only one of tools or functions.")
            if tool_choice is not None and function_call is not None:
                raise ValueError("Provide only one of tool_choice or function_call.")
            execute_fields = _execute_prompt_fields()
            if not execute_fields:
                raise NotImplementedError("Fornax SDK does not expose tool/function calling parameters.")
            tool_params = _build_tool_params(
                execute_fields=execute_fields,
                tools=tools,
                tool_choice=tool_choice,
                functions=functions,
                function_call=function_call,
            )
            params_kwargs.update(tool_params)
        params = ExecutePromptParam(**params_kwargs)
        response = FornaxClient.global_fornax_client.execute_prompt(params, stream=False)
        content = _extract_content(response)
        usage = _extract_usage(response)
        tool_calls = _extract_tool_calls(response)
        function_call = _extract_function_call(response)
        return _build_response(content, prompt_key, usage, tool_calls=tool_calls, function_call=function_call)


class _Chat:
    def __init__(self, client: FornaxOpenAI) -> None:
        self.completions = _Completions(client)


class _Completions:
    def __init__(self, client: FornaxOpenAI) -> None:
        self._client = client

    def create(
        self,
        *,
        model: str,
        messages: List[Dict[str, Any]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        presence_penalty: Optional[float] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Any] = None,
        functions: Optional[List[Dict[str, Any]]] = None,
        function_call: Optional[Any] = None,
        n: int = 1,
        stop: Optional[Any] = None,
        stream: bool = False,
        **kwargs: Any,
    ) -> Any:
        if n != 1:
            raise NotImplementedError("n != 1 is not supported in FornaxOpenAI")
        _ = stop
        _ = kwargs
        return self._client._create_chat_completion(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            tools=tools,
            tool_choice=tool_choice,
            functions=functions,
            function_call=function_call,
            stream=stream,
        )


def _tools_to_functions(tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    functions: List[Dict[str, Any]] = []
    for tool in tools:
        if not isinstance(tool, dict):
            raise ValueError("Tool definitions must be dicts.")
        tool_type = tool.get("type")
        if tool_type != "function":
            raise ValueError(f"Unsupported tool type: {tool_type}")
        function = tool.get("function")
        if not isinstance(function, dict):
            raise ValueError("Tool definition missing 'function' dict.")
        functions.append(function)
    return functions


def _functions_to_tools(functions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [{"type": "function", "function": function} for function in functions]


def _tool_choice_to_function_call(tool_choice: Any) -> Any:
    if isinstance(tool_choice, dict):
        if tool_choice.get("type") == "function":
            function = tool_choice.get("function") or {}
            name = function.get("name")
            if name:
                return {"name": name}
    return tool_choice


def _function_call_to_tool_choice(function_call: Any) -> Any:
    if isinstance(function_call, dict):
        name = function_call.get("name")
        if name:
            return {"type": "function", "function": {"name": name}}
    return function_call


def _build_tool_params(
    *,
    execute_fields: set[str],
    tools: Optional[List[Dict[str, Any]]],
    tool_choice: Optional[Any],
    functions: Optional[List[Dict[str, Any]]],
    function_call: Optional[Any],
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if tools is not None or functions is not None:
        if "custom_tools" not in execute_fields:
            raise NotImplementedError("Fornax SDK does not accept tools/functions.")
        openai_tools = tools if tools is not None else _functions_to_tools(functions or [])
        params["custom_tools"] = _openai_tools_to_fornax(openai_tools)

    if tool_choice is not None or function_call is not None:
        if "custom_tool_config" not in execute_fields:
            raise NotImplementedError("Fornax SDK does not accept tool_choice/function_call.")
        params["custom_tool_config"] = _build_tool_call_config(tool_choice, function_call)

    return params


def _openai_tools_to_fornax(tools: List[Dict[str, Any]]) -> List[ToolCombine]:
    converted: List[ToolCombine] = []
    for tool in tools:
        if not isinstance(tool, dict):
            raise ValueError("Tool definitions must be dicts.")
        tool_type = tool.get("type")
        if tool_type != "function":
            raise ValueError(f"Unsupported tool type: {tool_type}")
        function = tool.get("function")
        if not isinstance(function, dict):
            raise ValueError("Tool definition missing 'function' dict.")
        name = function.get("name")
        if not name:
            raise ValueError("Tool function missing name.")
        description = function.get("description")
        parameters = function.get("parameters")
        if parameters is not None and not isinstance(parameters, str):
            parameters = json.dumps(parameters)
        tool_def = Tool(
            type=ToolType.FUNCTION,
            function=ToolFunction(name=name, description=description, parameters=parameters),
        )
        converted.append(ToolCombine(tool_def=tool_def))
    return converted


def _build_tool_call_config(tool_choice: Optional[Any], function_call: Optional[Any]) -> ToolCallConfig:
    if tool_choice is not None and function_call is not None:
        raise ValueError("Provide only one of tool_choice or function_call.")
    choice = tool_choice if tool_choice is not None else function_call
    if isinstance(choice, str):
        choice_lower = choice.lower()
        if choice_lower == "auto":
            return ToolCallConfig(tool_choice=ToolChoiceType.AUTO)
        if choice_lower == "none":
            return ToolCallConfig(tool_choice=ToolChoiceType.NONE)
        raise ValueError(f"Unsupported tool_choice value: {choice}")
    if isinstance(choice, dict):
        if "type" in choice or "function" in choice:
            if choice.get("type") not in (None, "function"):
                raise ValueError(f"Unsupported tool_choice type: {choice.get('type')}")
            func = choice.get("function") or {}
            name = func.get("name") or choice.get("name")
        else:
            name = choice.get("name")
        if not name:
            raise ValueError("tool_choice missing function name.")
        specification = ToolChoiceSpecification(type=ToolType.FUNCTION, name=name)
        return ToolCallConfig(tool_choice=ToolChoiceType.SPECIFIC, specification=specification)
    raise ValueError("Unsupported tool_choice/function_call payload.")

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict

try:
    from .fornax_openai import FornaxOpenAI
except ImportError:  # pragma: no cover - fallback for running as a script
    from fornax_openai import FornaxOpenAI


def _response_to_dict(response: Any) -> Dict[str, Any]:
    raw_usage = response.usage if response.usage is not None else None
    usage = vars(raw_usage) if raw_usage and hasattr(raw_usage, "__dict__") else raw_usage
    message = response.choices[0].message
    tool_calls = getattr(message, "tool_calls", None)
    function_call = getattr(message, "function_call", None)
    message_payload: Dict[str, Any] = {
        "role": message.role,
        "content": message.content,
    }
    if tool_calls is not None:
        message_payload["tool_calls"] = tool_calls
    if function_call is not None:
        message_payload["function_call"] = function_call
    return {
        "id": response.id,
        "object": response.object,
        "created": response.created,
        "model": response.model,
        "choices": [
            {
                "index": response.choices[0].index,
                "message": message_payload,
                "finish_reason": response.choices[0].finish_reason,
            }
        ],
        "usage": usage,
    }


class OpenAICompatHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
            return
        self.send_error(404, "not found")

    def do_POST(self):
        if self.path != "/v1/chat/completions":
            self.send_error(404, "not found")
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length)
        try:
            payload = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            self.send_error(400, "invalid json")
            return

        model = payload.get("model") or self.server.default_model
        if not model:
            self.send_error(400, "model is required")
            return
        messages = payload.get("messages") or []
        if not messages:
            self.send_error(400, "messages is required")
            return

        try:
            response = self.server.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=payload.get("max_tokens") or 4096,
                temperature=payload.get("temperature"),
                top_p=payload.get("top_p"),
                frequency_penalty=payload.get("frequency_penalty"),
                presence_penalty=payload.get("presence_penalty"),
                tools=payload.get("tools"),
                tool_choice=payload.get("tool_choice"),
                functions=payload.get("functions"),
                function_call=payload.get("function_call"),
                n=payload.get("n", 1),
                stop=payload.get("stop"),
                stream=payload.get("stream", False),
            )
        except Exception as exc:
            self.send_error(500, f"completion failed: {exc}")
            return

        response_body = json.dumps(_response_to_dict(response)).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

    def log_message(self, format: str, *args: Any) -> None:
        return


def main() -> None:
    port = int(os.getenv("FORNAX_OPENAI_PORT", "8000"))
    ak = os.getenv("FORNAX_AK")
    sk = os.getenv("FORNAX_SK")
    prompt_key = os.getenv("FORNAX_PROMPT_KEY")
    prompt_version = os.getenv("FORNAX_PROMPT_VERSION")
    account_mode = os.getenv("FORNAX_ACCOUNT_MODE")
    model_name = os.getenv("FORNAX_MODEL_NAME")
    fornax_custom_region = os.getenv("FORNAX_CUSTOM_REGION", "")

    if not ak or not sk:
        raise ValueError("FORNAX_AK and FORNAX_SK must be set")

    client = FornaxOpenAI(
        ak=ak,
        sk=sk,
        prompt_key=prompt_key,
        prompt_version=prompt_version,
        model_name=model_name,
        account_mode=account_mode,
        fornax_custom_region=fornax_custom_region,
    )

    server = HTTPServer(("0.0.0.0", port), OpenAICompatHandler)
    server.client = client
    server.default_model = prompt_key or ""
    server.serve_forever()


if __name__ == "__main__":
    main()

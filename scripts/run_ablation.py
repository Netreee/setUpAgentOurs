#!/usr/bin/env python3
"""
消融实验脚本：对同一批 repo 跑 4 种配置，比较 XPU 各组件的贡献。

配置定义：
  A: 无 XPU（基线）
  B: 完整 XPU（RetrieverAgent + 延迟审计）
  C: XPU 但禁用延迟审计
  D: XPU 但禁用 RetrieverAgent（退化为直接向量检索）

用法：
  .venv/bin/python scripts/run_ablation.py \\
    --list data/ablation_30.jsonl \\
    --configs A B C D \\
    --workers 3 \\
    --max-steps 50 \\
    --subprocess-timeout 3600 \\
    --output results/ablation_results.json
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any


# ==================== 配置定义 ====================

CONFIGS: dict[str, dict[str, str]] = {
    "A": {
        "label": "无XPU（基线）",
        "XPU_DISABLED": "true",
        "XPU_ENABLED": "false",
        "XPU_VECTOR_ENABLED": "false",
    },
    "B": {
        "label": "完整XPU（RetrieverAgent+延迟审计）",
        "XPU_VECTOR_ENABLED": "true",
        "XPU_DISABLED": "false",
        "XPU_RETRIEVER_DISABLED": "false",
        "XPU_AUDIT_DISABLED": "false",
    },
    "C": {
        "label": "XPU+禁用延迟审计",
        "XPU_VECTOR_ENABLED": "true",
        "XPU_DISABLED": "false",
        "XPU_RETRIEVER_DISABLED": "false",
        "XPU_AUDIT_DISABLED": "true",
    },
    "D": {
        "label": "XPU+禁用RetrieverAgent（直接向量检索）",
        "XPU_VECTOR_ENABLED": "true",
        "XPU_DISABLED": "false",
        "XPU_RETRIEVER_DISABLED": "true",
        "XPU_AUDIT_DISABLED": "false",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="消融实验：4 种 XPU 配置对比")
    parser.add_argument("--list", default="data/ablation_30.jsonl", help="仓库清单 JSONL 路径")
    parser.add_argument("--configs", nargs="+", default=["A", "B", "C", "D"],
                        choices=["A", "B", "C", "D"], help="要跑的配置（默认全部）")
    parser.add_argument("--workers", type=int, default=3, help="并发 worker 数（跨 repo 并行）")
    parser.add_argument("--max-steps", type=int, default=50, help="单仓库最大步数")
    parser.add_argument("--subprocess-timeout", type=int, default=3600, help="单次运行超时秒数")
    parser.add_argument("--output", default="results/ablation_results.json", help="结果输出路径")
    parser.add_argument("--log-dir", default="log/ablation", help="日志目录")
    parser.add_argument("--repos", help="只跑指定 repo（逗号分隔，用于调试）")
    return parser.parse_args()


def load_repo_list(path: Path) -> list[dict]:
    repos = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                repos.append(json.loads(line))
    return repos


def run_one(
    repo: str,
    repo_url: str,
    config_name: str,
    config_env: dict[str, str],
    max_steps: int,
    log_dir: Path,
    subprocess_timeout: int,
) -> dict[str, Any]:
    """运行单个 repo × 单个配置，返回结果字典"""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_path = log_dir / f"{repo}_{config_name}_{timestamp}.log"

    env = os.environ.copy()
    for k, v in config_env.items():
        if k != "label":
            env[k] = v
    env["LOG_FILE"] = str(log_path)

    cmd = [sys.executable, "-m", "src.main", repo_url, str(max_steps)]

    # 记录启动前的容器，超时后只清理本次新增的
    pre_snap = subprocess.run(["docker", "ps", "-q"], capture_output=True, text=True)
    pre_containers: set = set(pre_snap.stdout.split()) if pre_snap.returncode == 0 else set()

    start_time = time.time()
    proc = None
    timed_out = False
    try:
        with log_path.open("w", encoding="utf-8") as fp:
            # 用 Popen + start_new_session 创建独立进程组，超时时 SIGKILL 整个组
            proc = subprocess.Popen(
                cmd, stdout=fp, stderr=fp, env=env,
                start_new_session=True,
            )
            try:
                proc.wait(timeout=subprocess_timeout)
            except subprocess.TimeoutExpired:
                timed_out = True
                # 强杀整个进程组（包含所有子进程），不等待响应
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                except ProcessLookupError:
                    pass
                proc.wait()  # 等 SIGKILL 生效，此时应立即返回

        elapsed = time.time() - start_time

        if timed_out:
            _cleanup_new_containers(pre_containers)
            return {
                "repo": repo,
                "config": config_name,
                "success": False,
                "elapsed_sec": round(elapsed),
                "log": str(log_path),
                "status": "timeout",
                "steps": -1,
                "verdict": None,
            }

        # 尝试从 log 目录读取 result.json
        safe_name = repo_url.rstrip("/").split("/")[-1]
        result_path = Path("log") / f"{safe_name}_result.json"
        verdict = _parse_result(result_path)

        return {
            "repo": repo,
            "config": config_name,
            "success": proc.returncode == 0,
            "elapsed_sec": round(elapsed),
            "log": str(log_path),
            **verdict,
        }
    except Exception as e:
        elapsed = time.time() - start_time
        if proc is not None:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except Exception:
                pass
        return {
            "repo": repo,
            "config": config_name,
            "success": False,
            "elapsed_sec": round(elapsed),
            "log": str(log_path),
            "status": "error",
            "steps": -1,
            "verdict": None,
            "error": str(e)[:200],
        }


def _parse_result(result_path: Path) -> dict:
    """从 result.json 提取关键字段"""
    if not result_path.exists():
        return {"status": "no_result", "steps": -1, "verdict": None}
    try:
        data = json.loads(result_path.read_text())
        phase2 = data.get("phase2", {})
        setup = data.get("setup", {})
        verdict = phase2.get("verdict") or ("pass" if phase2.get("success") else None)
        status = phase2.get("status") or ("pass" if phase2.get("success") else "error")
        steps = setup.get("steps_taken", -1)
        return {"status": status, "steps": steps, "verdict": verdict}
    except Exception:
        return {"status": "parse_error", "steps": -1, "verdict": None}


def _cleanup_new_containers(pre_containers: set) -> None:
    """清理本次新增的容器"""
    post_snap = subprocess.run(["docker", "ps", "-q"], capture_output=True, text=True)
    if post_snap.returncode == 0:
        new_containers = set(post_snap.stdout.split()) - pre_containers
        for cid in new_containers:
            subprocess.run(["docker", "kill", cid], capture_output=True)
    subprocess.run(["docker", "container", "prune", "-f"], capture_output=True)


def load_existing(output_path: Path) -> dict[tuple[str, str], dict]:
    """加载已有结果（断点续跑）"""
    if not output_path.exists():
        return {}
    try:
        data = json.loads(output_path.read_text())
        existing = {}
        for item in data.get("results", []):
            existing[(item["repo"], item["config"])] = item
        return existing
    except Exception:
        return {}


def save_results(output_path: Path, results: list[dict], configs: list[str]) -> None:
    """保存结果到 JSON 文件"""
    # 汇总统计
    summary: dict[str, Any] = {}
    for cfg in configs:
        cfg_results = [r for r in results if r["config"] == cfg]
        if not cfg_results:
            continue
        verdicts = [r.get("verdict") for r in cfg_results]
        statuses = [r.get("status") for r in cfg_results]
        pass_count = sum(1 for v in verdicts if v in ("pass", "not_guilty"))
        summary[cfg] = {
            "label": CONFIGS[cfg]["label"],
            "total": len(cfg_results),
            "pass": pass_count,
            "timeout": statuses.count("timeout"),
            "error": statuses.count("error"),
            "no_result": statuses.count("no_result"),
            "pass_rate": round(pass_count / len(cfg_results), 4) if cfg_results else 0,
        }

    output = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary": summary,
        "results": results,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2))


def main() -> int:
    args = parse_args()
    list_path = Path(args.list)
    log_dir = Path(args.log_dir)
    output_path = Path(args.output)
    log_dir.mkdir(parents=True, exist_ok=True)

    repos = load_repo_list(list_path)

    # 过滤指定 repo
    if args.repos:
        want = set(args.repos.split(","))
        repos = [r for r in repos if r["repo"] in want]

    if not repos:
        print("未读取到任何仓库", file=sys.stderr)
        return 1

    configs = args.configs
    total_tasks = len(repos) * len(configs)
    print(f"消融实验：{len(repos)} 个 repo × {len(configs)} 种配置 = {total_tasks} 次运行")
    cfg_labels = ", ".join(f"{c}({CONFIGS[c]['label']})" for c in configs)
    print(f"配置：{cfg_labels}")
    print(f"并发 worker：{args.workers}，超时：{args.subprocess_timeout}s/次")
    print(f"输出：{output_path}")
    print()

    # 启动前检查磁盘，低于 50Gi 拒绝启动
    free_gb = shutil.disk_usage("/").free / (1024 ** 3)
    if free_gb < 50:
        print(f"磁盘可用空间不足（{free_gb:.1f}Gi < 50Gi），请先清理 Docker 后重试", file=sys.stderr)
        print("清理命令：docker container prune -f && docker image prune -af", file=sys.stderr)
        return 1
    print(f"磁盘可用：{free_gb:.1f}Gi")

    # 断点续跑：加载已有结果
    existing = load_existing(output_path)
    if existing:
        print(f"断点续跑：已有 {len(existing)} 条结果，将跳过已完成任务")

    # 构建任务列表（跳过已完成的）
    tasks = []
    for repo_obj in repos:
        for cfg in configs:
            key = (repo_obj["repo"], cfg)
            if key in existing:
                continue
            tasks.append((repo_obj, cfg))

    skipped = total_tasks - len(tasks)
    if skipped:
        print(f"跳过已完成：{skipped} 个，剩余：{len(tasks)} 个")

    all_results: list[dict] = list(existing.values())
    lock = threading.Lock()
    done = 0
    ok = 0

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(
                run_one,
                repo_obj["repo"],
                repo_obj["repo_url"],
                cfg,
                CONFIGS[cfg],
                args.max_steps,
                log_dir,
                args.subprocess_timeout,
            ): (repo_obj["repo"], cfg)
            for repo_obj, cfg in tasks
        }

        for future in as_completed(futures):
            repo_name, cfg = futures[future]
            result = future.result()
            with lock:
                done += 1
                verdict = result.get("verdict")
                is_pass = verdict in ("pass", "not_guilty")
                if is_pass:
                    ok += 1
                all_results.append(result)
                # 每完成一个任务就保存（断点安全）
                save_results(output_path, all_results, configs)
                status_str = result.get("status", "unknown")
                print(f"[{done}/{len(tasks)}] {repo_name} @ {cfg}: {status_str} "
                      f"({result.get('elapsed_sec', 0)}s)")
                # 每 5 个任务清理一次 Docker 和磁盘检查
                if done % 5 == 0:
                    subprocess.run(["docker", "container", "prune", "-f"], capture_output=True)
                    subprocess.run(["docker", "image", "prune", "-f"], capture_output=True)
                    free_gb = shutil.disk_usage("/").free / (1024 ** 3)
                    if free_gb < 20:
                        print(f"⚠ 磁盘告警：可用仅 {free_gb:.1f}Gi，执行深度清理")
                        subprocess.run(["docker", "image", "prune", "-af"], capture_output=True)

    print()
    print("消融实验完成")
    save_results(output_path, all_results, configs)

    # 打印汇总表
    print("\n=== 结果汇总 ===")
    print(f"{'配置':<4} {'标签':<30} {'通过率':<8} {'pass':<6} {'total':<6} {'timeout':<8} {'error':<6}")
    print("-" * 80)
    final = json.loads(output_path.read_text())
    for cfg in configs:
        s = final["summary"].get(cfg, {})
        print(f"{cfg:<4} {s.get('label',''):<30} {s.get('pass_rate',0)*100:.1f}%    "
              f"{s.get('pass',0):<6} {s.get('total',0):<6} {s.get('timeout',0):<8} {s.get('error',0):<6}")

    print(f"\n结果已写入：{output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

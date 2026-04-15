#!/usr/bin/env python3
"""
XPU 知识库膨胀脚本：向 xpu_inflated 数据库注入噪声条目，模拟大规模知识库场景。

噪声策略：
  1. 上下文扰动：修改现有 XPU 的 Python 版本、OS、工具链
  2. 交叉嫁接：取 A 的 signals + B 的 advice，组合成似是而非的条目
  3. 泛化模糊：把具体建议改成模糊的通用建议
  4. 跨语言干扰：Node.js / Rust / Go 的环境配置经验

用法：
  .venv/bin/python scripts/inflate_xpu_db.py --target 2000
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env", override=True)

INFLATED_DB = "postgresql://postgres:password@localhost:5432/xpu_inflated"


def load_originals() -> list[dict]:
    """从 xpu_inflated 加载原始 421 条"""
    import psycopg2
    conn = psycopg2.connect(INFLATED_DB)
    cur = conn.cursor()
    cur.execute("SELECT id, context, signals, advice_nl, atoms, telemetry FROM xpu_entries")
    rows = cur.fetchall()
    conn.close()
    entries = []
    for r in rows:
        entries.append({
            "id": r[0],
            "context": r[1],
            "signals": r[2],
            "advice_nl": r[3],
            "atoms": r[4],
            "telemetry": r[5],
        })
    return entries


def gen_context_perturbations(entry: dict, n: int = 2) -> list[dict]:
    """策略1：上下文扰动——修改 Python 版本、OS、工具"""
    variants = []
    py_versions = ["3.8", "3.9", "3.10", "3.11", "3.12", "3.13"]
    os_options = [["linux"], ["linux", "macos"], ["linux", "windows"]]
    tool_noise = ["conda", "poetry", "pipenv", "pdm", "hatch", "uv", "mamba"]

    for _ in range(n):
        v = copy.deepcopy(entry)
        ctx = v["context"]
        if isinstance(ctx, dict):
            ctx["python"] = [random.choice(py_versions)]
            ctx["os"] = random.choice(os_options)
            if random.random() > 0.5:
                existing_tools = ctx.get("tools", [])
                ctx["tools"] = existing_tools + [random.choice(tool_noise)]
        v["id"] = f"noise_ctx_{int(time.time())}_{os.urandom(3).hex()}"
        v["telemetry"] = {"hits": 0}
        variants.append(v)
    return variants


def gen_cross_graft(entries: list[dict], n: int = 100) -> list[dict]:
    """策略2：交叉嫁接——A 的 signals + B 的 advice + C 的 atoms"""
    variants = []
    for _ in range(n):
        a, b, c = random.sample(entries, 3)
        v = {
            "id": f"noise_graft_{int(time.time())}_{os.urandom(3).hex()}",
            "context": copy.deepcopy(a["context"]),
            "signals": copy.deepcopy(b["signals"]),
            "advice_nl": copy.deepcopy(c["advice_nl"]),
            "atoms": copy.deepcopy(random.choice([a, b, c])["atoms"]),
            "telemetry": {"hits": 0},
        }
        variants.append(v)
        time.sleep(0.001)  # 避免 ID 碰撞
    return variants


def gen_vague_entries(entries: list[dict], n: int = 100) -> list[dict]:
    """策略3：泛化模糊——把具体建议改成模糊的通用建议"""
    vague_advice = [
        ["检查 Python 版本是否满足项目要求", "确保使用正确的 Python 版本运行项目"],
        ["安装项目的依赖包", "使用 pip install 安装缺少���依赖"],
        ["检查系统是否安装了必要的编译工具", "安装 build-essential 或等效工具包"],
        ["确保虚拟环境已激活", "使用 venv 或 conda 创建并激活虚拟环境"],
        ["检查 PATH 环境变量是否包含必要路径", "确认可执行文件路径已添加到 PATH"],
        ["运行 pip install -e . 安装项目", "以开发模式安装项目以便测试"],
        ["安装测试依赖", "检查 requirements-test.txt 或 pyproject.toml 中的测试依赖"],
        ["检查配置文件是否正确", "确认环境变量和配置文件与测试环境匹配"],
        ["升级 pip 和 setuptools", "使用 pip install --upgrade pip setuptools wheel"],
        ["检查网络连接", "确认 pip 可以正常访问 PyPI 仓库"],
        ["处理依赖版本冲突", "使用 pip install --force-reinstall 解决版本冲突"],
        ["安装系统级依赖", "使用 apt-get 安装缺少的系统库"],
    ]
    vague_signals_kw = [
        ["安装失败", "依赖问题", "环境配置"],
        ["ModuleNotFoundError", "导入错误"],
        ["pip install", "包管理"],
        ["编译失败", "build error", "gcc"],
        ["权限问题", "Permission denied"],
        ["版本冲突", "incompatible", "requires"],
    ]

    variants = []
    for _ in range(n):
        base = random.choice(entries)
        v = copy.deepcopy(base)
        v["id"] = f"noise_vague_{int(time.time())}_{os.urandom(3).hex()}"
        v["advice_nl"] = random.choice(vague_advice)
        v["signals"]["keywords"] = random.choice(vague_signals_kw)
        v["atoms"] = []  # 模糊建议没有具体操作
        v["telemetry"] = {"hits": 0}
        variants.append(v)
        time.sleep(0.001)
    return variants


def gen_cross_lang_entries(n: int = 100) -> list[dict]:
    """策略4：跨语言干���——Node.js / Rust / Go 的经验"""
    cross_lang = [
        {
            "context": {"lang": "javascript", "os": ["linux"], "tools": ["npm", "node"]},
            "signals": {"keywords": ["npm install", "node_modules", "package.json"], "regex": [], "situation_triggers": ["npm 安装失败"]},
            "advice_nl": ["使用 npm install 安装依赖时，如果报 ERESOLVE 错误，尝试 npm install --legacy-peer-deps"],
            "atoms": [{"name": "shell", "args": {"command": "npm install --legacy-peer-deps"}}],
        },
        {
            "context": {"lang": "javascript", "os": ["linux"], "tools": ["yarn"]},
            "signals": {"keywords": ["yarn install", "yarn.lock"], "regex": [], "situation_triggers": ["yarn 安装问题"]},
            "advice_nl": ["yarn install 失败时检查 node 版本是否满足 engines 要求"],
            "atoms": [{"name": "shell", "args": {"command": "yarn install --ignore-engines"}}],
        },
        {
            "context": {"lang": "rust", "os": ["linux"], "tools": ["cargo"]},
            "signals": {"keywords": ["cargo build", "rustc", "Cargo.toml"], "regex": [], "situation_triggers": ["Rust 编译失败"]},
            "advice_nl": ["cargo build 失败时检查 Rust toolchain 版本", "使用 rustup update 更新工具链"],
            "atoms": [{"name": "shell", "args": {"command": "rustup update stable"}}],
        },
        {
            "context": {"lang": "go", "os": ["linux"], "tools": ["go"]},
            "signals": {"keywords": ["go build", "go mod", "go.sum"], "regex": [], "situation_triggers": ["Go 模块下载失败"]},
            "advice_nl": ["go mod download 失败时设置 GOPROXY=https://goproxy.cn,direct"],
            "atoms": [{"name": "set_env", "args": {"key": "GOPROXY", "value": "https://goproxy.cn,direct"}}],
        },
        {
            "context": {"lang": "ruby", "os": ["linux"], "tools": ["bundler", "gem"]},
            "signals": {"keywords": ["bundle install", "Gemfile", "gem install"], "regex": [], "situation_triggers": ["Ruby gem 安装失败"]},
            "advice_nl": ["bundle install 失败时先安装系统依赖: apt-get install ruby-dev libsqlite3-dev"],
            "atoms": [{"name": "apt_install", "args": {"packages": ["ruby-dev", "libsqlite3-dev"]}}],
        },
    ]

    variants = []
    for _ in range(n):
        base = copy.deepcopy(random.choice(cross_lang))
        base["id"] = f"noise_lang_{int(time.time())}_{os.urandom(3).hex()}"
        base["telemetry"] = {"hits": 0}
        variants.append(base)
        time.sleep(0.001)
    return variants


def compute_and_insert(variants: list[dict], batch_label: str) -> int:
    """计算 embedding 并批量插入数据库"""
    from src.xpu.xpu_vector_store import text_to_embedding
    import psycopg2

    conn = psycopg2.connect(INFLATED_DB)
    cur = conn.cursor()

    inserted = 0
    for i, v in enumerate(variants):
        # 构造 embedding 文本（和原始入库时一致）
        advice_text = " ".join(v["advice_nl"]) if isinstance(v["advice_nl"], list) else str(v["advice_nl"])
        signals = v.get("signals", {})
        keywords = " ".join(signals.get("keywords", []))
        triggers = " ".join(signals.get("situation_triggers", []))
        embed_text = f"{advice_text} {keywords} {triggers}"

        try:
            embedding = text_to_embedding(embed_text)
        except Exception as e:
            print(f"  [{batch_label}] embedding 失败 ({i+1}): {e}")
            continue

        try:
            cur.execute(
                """INSERT INTO xpu_entries (id, context, signals, advice_nl, atoms, embedding, telemetry)
                   VALUES (%s, %s, %s, %s, %s, %s::vector, %s)
                   ON CONFLICT (id) DO NOTHING""",
                (
                    v["id"],
                    json.dumps(v["context"], ensure_ascii=False),
                    json.dumps(v["signals"], ensure_ascii=False),
                    json.dumps(v["advice_nl"], ensure_ascii=False),
                    json.dumps(v["atoms"], ensure_ascii=False),
                    str(embedding),
                    json.dumps(v["telemetry"], ensure_ascii=False),
                )
            )
            inserted += 1
        except Exception as e:
            print(f"  [{batch_label}] 插入失败 ({i+1}): {e}")
            conn.rollback()
            continue

        if (i + 1) % 50 == 0:
            conn.commit()
            print(f"  [{batch_label}] 进度: {i+1}/{len(variants)}")

    conn.commit()
    conn.close()
    return inserted


def current_count() -> int:
    import psycopg2
    conn = psycopg2.connect(INFLATED_DB)
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM xpu_entries")
    n = cur.fetchone()[0]
    conn.close()
    return n


def main():
    parser = argparse.ArgumentParser(description="XPU 知识库��胀")
    parser.add_argument("--target", type=int, default=2000, help="目标条目数")
    args = parser.parse_args()

    print(f"目标: {args.target} 条")
    print(f"当前: {current_count()} 条")

    originals = load_originals()
    # 只取原始 421 条（id 不以 noise_ 开头）
    originals = [e for e in originals if not e["id"].startswith("noise_")]
    print(f"原始条目: {len(originals)} 条")

    need = args.target - current_count()
    if need <= 0:
        print("已达目标，无需膨胀")
        return

    # 按比例分配噪声
    n_ctx = int(need * 0.35)       # 35% 上��文扰动
    n_graft = int(need * 0.25)     # 25% 交叉嫁接
    n_vague = int(need * 0.25)     # 25% 泛化模糊
    n_lang = need - n_ctx - n_graft - n_vague  # 剩余 跨语言

    print(f"\n生成噪声: 上���文扰动 {n_ctx} + 交叉嫁接 {n_graft} + 泛化模糊 {n_vague} + 跨语言 {n_lang} = {need}")

    # 1. 上下文扰动（需要 embedding）
    print(f"\n[1/4] 生成上下文扰动 ({n_ctx} 条)...")
    ctx_variants = []
    per_entry = max(1, n_ctx // len(originals))
    sampled = random.sample(originals, min(len(originals), n_ctx // max(per_entry, 1)))
    for e in sampled:
        ctx_variants.extend(gen_context_perturbations(e, per_entry))
    ctx_variants = ctx_variants[:n_ctx]
    inserted = compute_and_insert(ctx_variants, "上下文扰��")
    print(f"  插入 {inserted} 条，当前总计 {current_count()}")

    # 2. 交叉嫁接
    print(f"\n[2/4] 生成交叉��接 ({n_graft} 条)...")
    graft_variants = gen_cross_graft(originals, n_graft)
    inserted = compute_and_insert(graft_variants, "交叉嫁接")
    print(f"  插入 {inserted} 条，当前总计 {current_count()}")

    # 3. 泛化模糊
    print(f"\n[3/4] 生成泛化模糊 ({n_vague} 条)...")
    vague_variants = gen_vague_entries(originals, n_vague)
    inserted = compute_and_insert(vague_variants, "泛化模糊")
    print(f"  插入 {inserted} 条，当前��计 {current_count()}")

    # 4. 跨��言���扰
    print(f"\n[4/4] 生��跨语言干扰 ({n_lang} 条)...")
    lang_variants = gen_cross_lang_entries(n_lang)
    inserted = compute_and_insert(lang_variants, "跨语言")
    print(f"  插入 {inserted} 条，当前���计 {current_count()}")

    print(f"\n膨胀完成！最终: {current_count()} 条")


if __name__ == "__main__":
    main()

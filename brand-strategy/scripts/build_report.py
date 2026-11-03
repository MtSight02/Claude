#!/usr/bin/env python3
"""Concatenate all brand-strategy Markdown files into REPORT.md (run from anywhere)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARTS = [
    ("第一部分 · 共用底稿", "00-shared"),
    ("第二部分 · 方案 A：Finch & Flare（推荐）", "finch-and-flare"),
    ("第三部分 · 方案 B：Wren & Wink", "wren-and-wink"),
    ("第四部分 · 方案 C：Lark & Luce", "lark-and-luce"),
]
TAIL = [("第五部分 · 对比总结与推荐", "09-comparison.md"),
        ("第六部分 · 大胆版方向", "10-bold-concept.md")]

def demote(text: str) -> str:
    # shift every heading one level down so each file nests under its part heading
    out, fence = [], False
    for line in text.splitlines():
        if line.startswith("```"):
            fence = not fence
        if not fence and line.startswith("#"):
            line = "#" + line
        out.append(line)
    return "\n".join(out).strip() + "\n"

def main():
    sections, toc = [], []
    def add(title, files):
        toc.append(f"- {title}")
        body = [f"# {title}\n"]
        for f in files:
            first = next((l for l in f.read_text(encoding="utf-8").splitlines() if l.startswith("# ")), f.stem)
            toc.append(f"  - {first[2:].strip()}")
            body.append(demote(f.read_text(encoding="utf-8")))
        sections.append("\n\n".join(body))
    for title, d in PARTS:
        add(title, sorted((ROOT / d).glob("*.md")))
    for title, f in TAIL:
        add(title, [ROOT / f])
    head = ("# DTC 珠宝品牌方案 · 总报告\n\n"
            "> 本文件由 `scripts/build_report.py` 从各分文件自动合成，请修改分文件后重新运行脚本。\n"
            "> 首页 HTML 样稿：`site/index.html`（Finch & Flare，浏览器直接打开）。\n\n"
            "## 目录\n\n" + "\n".join(toc) + "\n")
    (ROOT / "REPORT.md").write_text(head + "\n\n---\n\n" + "\n\n---\n\n".join(sections), encoding="utf-8")
    print("wrote", ROOT / "REPORT.md")

if __name__ == "__main__":
    main()

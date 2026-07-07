#!/usr/bin/env python3
"""Self-check for the full-book deconstruction scaffold."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    root = Path(tempfile.mkdtemp(prefix="novel-orchestrator-check-"))
    try:
        source = root / "book.txt"
        out = root / "book-拆书"
        source.write_text(
            "第一章 开始\n主角获得系统。\n\n第二章 危机\n组织登场。\n\n第三章 兑现\n主角解决危机。\n",
            encoding="utf-8",
        )
        subprocess.run(
            [
                sys.executable,
                str(Path(__file__).with_name("scaffold_full_book_deconstruction.py")),
                str(source),
                "--out",
                str(out),
                "--chapters-per-volume",
                "2",
                "--write-source-chunks",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        expected = [
            "00-项目说明/00-拆书说明.md",
            "01-章节索引/01-章节索引.md",
            "01-章节索引/02-coverage-ledger.md",
            "02-全书总览/01-全书承诺与核心循环.md",
            "08-角色拆解/01-主要角色/角色-001-待命名.md",
            "08-角色拆解/02-重要配角/角色-001-待命名.md",
            "08-角色拆解/03-反派角色/角色-001-待命名.md",
            "08-角色拆解/04-功能角色/角色-001-待命名.md",
            "16-卷级精拆/vol-01-卷级精拆.md",
            "16-卷级精拆/vol-02-卷级精拆.md",
            "17-原文切块/chapter-001.txt",
            "99-总报告/99-总报告.md",
        ]
        for rel in expected:
            assert (out / rel).exists(), rel
        role_text = (out / "08-角色拆解/01-主要角色/角色-001-待命名.md").read_text(encoding="utf-8")
        for marker in ("## 外貌与识别", "## 性格与心理", "## 成长与变化", "| 性格变化 |"):
            assert marker in role_text, marker
        setting_text = (out / "04-世界观设定/01-基础规则/规则-001-待命名.md").read_text(encoding="utf-8")
        for marker in ("| 例外条件 |", "| 违反后果 |", "| 可迁移风险 |"):
            assert marker in setting_text, marker
        volume_text = (out / "16-卷级精拆/vol-01-卷级精拆.md").read_text(encoding="utf-8")
        assert "| 卷级承诺 |" in volume_text
        assert not [path for path in out.iterdir() if path.is_file()]
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    main()

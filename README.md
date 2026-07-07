# Novel Orchestrator

Codex skill for Chinese web-novel creation, diagnosis, setting-bible analysis, full-book detailed deconstruction, and evidence-backed 拆书.

## What It Does

- Diagnose premises, openings, setting libraries, outlines, and chapters.
- Route work through reader promise, hooks, expectation chains, 起承转合, and long-arc continuity.
- Use completed manual case evidence through `batch-169`, cases `001-845`.
- Consult 845 completed subgenre/structure modules.
- Produce concrete revision plans, training tasks, diagnosis reports, full-book 拆书 folders, or 拆书 outputs.

## Use

Invoke the skill in Codex:

```text
$novel-orchestrator
```

Typical requests:

```text
用 $novel-orchestrator 分析这个网文设定库，判断哪些设定能支撑前三章。
用 $novel-orchestrator 拆这本小说的开篇、期待链和长线不断档。
用 $novel-orchestrator 完整精拆这本 txt，按章节、单元、卷级和全书总报告输出。
用 $novel-orchestrator 诊断我的第一章为什么没有追读感。
```

## Contents

- `SKILL.md`: routing rules and output contract.
- `references/orchestrator/`: total entry, routing matrix, concepts, workflows, checklists.
- `references/modules/`: reader promise, opening hooks, expectation/emotion, 起承转合, long-arc continuity, 拆书取证.
- `references/genre-modules/`: eight major genre modules.
- `references/subgenre-modules/`: 845 completed subtype/structure modules.
- `references/case-library/精拆/`: 169 manual拆书 batches, 845 cases.
- `references/curriculum/`: newcomer training path and acceptance criteria.
- `references/templates/`: reusable creation and diagnosis templates.
- `scripts/scaffold_full_book_deconstruction.py`: scaffold a fully nested full-book 拆书 tree with chapter index, coverage ledger, category folders, per-character/item templates, `16-卷级精拆/`, and `99-总报告/`.

## Boundary

This repository intentionally excludes unfinished `batch-170+`, raw corpus indexes, source-workbench tooling, and evidence images. The skill is a completed snapshot, not the active corpus workbench.

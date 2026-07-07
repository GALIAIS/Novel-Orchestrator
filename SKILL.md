---
name: novel-orchestrator
description: Chinese web-novel creation and diagnosis orchestrator for premises, setting bibles, openings, reader promise, expectation chains, unit structure, long-arc continuity, manual case evidence, full-book detailed deconstruction, fine-grained taxonomy breakdowns, and evidence-backed 拆书. Use when the user asks to analyze or improve 网文 ideas, settings, chapters, outlines, genre fit, hooks, 爽点/期待感, 起承转合, 新人训练, 拆书取证, 完整拆一本书, 设定/大纲/角色精拆, or consult the completed local 网文创作分析编排系统 snapshot.
---

# Novel Orchestrator

Use this skill as a completed snapshot of `网文创作分析编排系统`.

## Boundary

- Include only completed material copied into `references/`.
- Treat manual high-weight cases as complete only through `batch-169`, cases `001-845`.
- Treat subgenre modules as complete only for the 845 modules indexed in `references/subgenre-modules/README.md`.
- Do not claim `batch-170` or later exists in this skill. If the user asks to continue corpus整理, work in the source workspace, not inside this skill snapshot.
- Do not load raw corpus indexes, scripts, tools, or evidence images from this skill; they were deliberately excluded.

## Route

1. Read `references/orchestrator/00-总控入口.md`.
2. Use `references/orchestrator/01-router-matrix.md` to choose one main module.
3. Read only the matching file in `references/modules/`.
4. If genre fit matters, read the relevant file in `references/genre-modules/`.
5. If a reusable subtype is needed, search `references/subgenre-modules/README.md`, then read only the matching module file.
6. If evidence from completed manual cases is needed, search `references/case-library/精拆/manual-ledger-completed.md`, then read the cited `batch-xxx.md`.
7. Use `references/templates/` only when the user asks for a reusable card/report format.
8. For local full-book txt/md deconstruction, run `scripts/scaffold_full_book_deconstruction.py <book-file>` first, then fill the generated files.

## Output Rules

- Return a concrete creation, diagnosis, revision, training, or evidence-backed拆书 deliverable first.
- Separate confirmed evidence, interpretation, and invention.
- Prefer one routed module over mixing every framework.
- Preserve the user's core idea unless asked to reinvent it.
- For web novels, always check reader promise, opening hook, expectation chain, payoff, and next expectation.
- For full-book 拆书, create one independent top-level folder per major category, including `16-卷级精拆/` for all `vol-xx` files and `99-总报告/` for the final report. For characters, create subfolders for main characters, important supporting characters, antagonists, and function characters, then write one detailed md per character covering profile, appearance, personality/psychology, growth/change, plot function, relationships, performance evidence, and craft analysis. Apply the same item-level split to settings, forces, events, foreshadowing, expectations, scenes, and transfer templates; summary tables are indexes, not substitutes for detailed files.
- Format generated markdown for scanning: use heading hierarchy plus `字段 / 内容` tables for fill-in fields; keep summary ledgers as normal markdown tables.

## Reference Map

- `references/orchestrator/`: total entry, routing, core concepts, workflows, checklists, source index.
- `references/modules/`: task modules for reader promise, opening hooks, expectation/emotion,起承转合, long-arc continuity,拆书取证.
- `references/genre-modules/`: eight major genre modules.
- `references/subgenre-modules/`: 845 completed subtype/structure modules.
- `references/case-library/精拆/`: 169 completed manual batches, 845 cases.
- `references/curriculum/`: newcomer training path, training task bank, acceptance criteria.
- `references/templates/`: creation card and diagnosis report templates.
- `scripts/scaffold_full_book_deconstruction.py`: create the nested full-book 拆书 folder tree, including chapter index, coverage ledger, category folders, per-character/item templates, volume folder, and report folder.

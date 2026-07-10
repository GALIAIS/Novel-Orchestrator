---
name: novel-orchestrator
description: Creation and analysis orchestrator for serial fiction, light novels, and manga, covering premises, setting bibles, openings, reader promise, expectation chains, unit structure, long-arc continuity, manual case evidence, full-book detailed deconstruction, fine-grained taxonomy breakdowns, and evidence-backed 拆书. Use when the user asks to analyze or improve ideas, settings, chapters, outlines, genre fit, hooks, 爽点/期待感, 起承转合, 新人训练, 拆书取证, 完整拆一本书, 设定/大纲/角色精拆, or consult the completed local creation-analysis system snapshot.
---

# 创作编排器

Use this skill as a completed snapshot of `网文创作分析编排系统`.

## Boundary

- Include only completed material copied into `references/`.
- Treat manual high-weight cases as complete only through `batch-418`, cases `0001-2090`.
- Treat subgenre modules as complete only for the 2090 modules indexed in `references/subgenre-modules/README.md`.
- Do not claim `batch-419` or later exists in this skill. If the user asks to continue corpus整理, work in the source workspace, not inside this skill snapshot.
- Do not load raw corpus indexes, scripts, tools, or evidence images from this skill; they were deliberately excluded.

## Route

1. Read `references/orchestrator/00-总控入口.md`.
2. Use `references/orchestrator/01-router-matrix.md` to choose one main module.
3. Read only the matching file in `references/modules/`.
4. If genre fit matters, read the relevant file in `references/genre-modules/`.
5. If a reusable subtype is needed, use `rg -n "关键词1|关键词2|同义词" references/subgenre-modules/README.md` instead of loading the 2090-entry index in full; read only the 1-3 best-matching module files.
6. If evidence from completed manual cases is needed, use `rg -n "关键词1|关键词2|标题词" references/case-library/精拆/manual-ledger-completed.md`, then read only the cited `batch-xxx.md` and relevant case section.
7. Use `references/templates/` only when the user asks for a reusable card/report format.
8. For local full-book txt/md deconstruction, run `scripts/scaffold_full_book_deconstruction.py <book-file>` first, then fill the generated files.

## Output Rules

- Return a concrete creation, diagnosis, revision, training, or evidence-backed拆书 deliverable first.
- Separate confirmed evidence, interpretation, and invention.
- Treat case conclusions as bounded writing evidence, not external verification of platform data, income, market trends, or reader universals.
- Prefer one routed module over mixing every framework.
- Preserve the user's core idea unless asked to reinvent it.
- For web novels, always check reader promise, opening hook, expectation chain, payoff, and next expectation.
- For full-book 拆书, create one independent top-level folder per major category, including `16-卷级精拆/` for all `vol-xx` files and `99-总报告/` for the final report. For characters, create subfolders for main characters, important supporting characters, antagonists, and function characters, then write one detailed md per character covering profile, appearance, personality/psychology, growth/change, plot function, relationships, performance evidence, and craft analysis. Apply the same item-level split to settings, forces, events, foreshadowing, expectations, scenes, and transfer templates; summary tables are indexes, not substitutes for detailed files.
- For light novels, additionally analyze voice, dialogue density, character attributes, daily-life/mainline balance, illustration beats, and volume hooks. For manga, additionally analyze panel flow, page-turn hooks, panel density, visual hooks, character design, expression acting, action lines, speech balloons, stillness/blank space, and climax pages.
- Format generated markdown for scanning: use heading hierarchy plus `字段 / 内容` tables for fill-in fields; keep summary ledgers as normal markdown tables.

## Reference Map

- `references/orchestrator/`: total entry, routing, core concepts, workflows, checklists, source index.
- `references/modules/`: task modules for reader promise, opening hooks, expectation/emotion,起承转合, long-arc continuity,拆书取证.
- `references/genre-modules/`: eight major genre modules.
- `references/subgenre-modules/`: 2090 completed subtype/structure modules.
- `references/case-library/精拆/`: 418 completed manual batches, 2090 cases.
- `references/curriculum/`: newcomer training path, training task bank, acceptance criteria.
- `references/templates/`: creation card and diagnosis report templates.
- `scripts/scaffold_full_book_deconstruction.py`: create the nested full-book 拆书 folder tree, including chapter index, coverage ledger, category folders, per-character/item templates, volume folder, and report folder.

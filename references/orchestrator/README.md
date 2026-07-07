# 网文创作分析编排系统

本系统不是“拆书方法大全”，而是一个面向网文创作、诊断、训练、复盘的总控编排体系。它参考 `GALIAIS/CTF-Sandbox-Orchestrator` 的设计方式：单一入口、路由矩阵、下游模块、证据优先级、最小可验证路径、阶段产物和复盘报告。

## 设计原则

1. 总控先判断问题类型，再进入模块。
2. 每次只加载一个主模块，避免把开篇、爽点、题材、拆书、大纲混在一起。
3. 先证明一个最小闭环，再扩展到整本书。
4. 所有判断必须绑定证据：原文片段、章节位置、读者反馈、榜单样本、同题材案例、已有设定。
5. 拆书只是取证和建模模块，不是系统核心。
6. 最终产物必须能直接用于创作、修改、训练或复盘。

## 文件结构

```text
网文创作分析编排系统
├─ README.md
├─ 00-总控入口.md
├─ 01-router-matrix.md
├─ 02-core-concepts.md
├─ 03-workflows.md
├─ 04-checklists.md
├─ 05-source-index.md
├─ indexes
│  ├─ corpus-index.jsonl
│  ├─ corpus-index.csv
│  └─ 全库遍历覆盖报告.md
├─ case-library
│  ├─ case-index.jsonl
│  ├─ case-index.csv
│  ├─ case-cards.jsonl
│  ├─ case-cards.csv
│  ├─ 案例库总表.md
│  └─ 按题材/
├─ genre-modules
│  ├─ 玄幻仙侠武侠.md
│  ├─ 都市现实职业.md
│  ├─ 历史架空权谋.md
│  ├─ 科幻末世无限游戏.md
│  ├─ 悬疑灵异规则怪谈.md
│  ├─ 女频情感成长.md
│  ├─ 轻小说同人二次元.md
│  └─ 短剧新媒体.md
├─ curriculum
│  ├─ 新人等级路径.md
│  ├─ 训练任务库.md
│  └─ 验收标准.md
├─ subgenre-modules
│  ├─ 期待不断档-两长一短.md
│  ├─ 核心梗-故事卡.md
│  ├─ 故事循环-配角预演.md
│  ├─ 科技震惊流.md
│  └─ 黄金三章-悬念回收流.md
├─ modules
│  ├─ module-题材与读者承诺.md
│  ├─ module-开篇与钩子.md
│  ├─ module-期待感与情绪.md
│  ├─ module-单元故事起承转合.md
│  ├─ module-长线结构与不断档.md
│  └─ module-拆书取证.md
└─ templates
   ├─ 创作卡片模板.md
   └─ 诊断报告模板.md
```

## 使用入口

先读 `00-总控入口.md`，再按 `01-router-matrix.md` 选择模块。不要一上来就填拆书表，也不要一上来就改章节。先判断当前任务属于哪种：

- 新人入门训练
- 题材定位
- 开篇诊断
- 期待感断档
- 单元故事卡住
- 长线结构散乱
- 已有书籍拆解取证
- 已写文本复盘
- 题材专项训练
- 知识库案例检索

## 全库遍历结果

已遍历 `<KNOWLEDGE_MD>` 下 34739 个 Markdown 文件，生成：

- 全库索引：`indexes/corpus-index.jsonl`
- 表格索引：`indexes/corpus-index.csv`
- 案例库：`case-library/case-index.jsonl`
- 结构化案例卡：`case-library/case-cards.jsonl`
- 题材专项模块：`genre-modules/`
- 人工精拆：`case-library/精拆/`
- 子流派细分模块：`subgenre-modules/`
- 新人课程路径：`curriculum/`

## 系统输出物

每次运行至少产出一种可保存的文件：

- `读者承诺卡`
- `开篇诊断报告`
- `期待链路表`
- `单元故事卡`
- `长线结构图`
- `拆书取证表`
- `问题修复清单`
- `下一轮训练任务`

## 快速路线

1. 不知道写什么：走 `题材与读者承诺`。
2. 开头不吸引：走 `开篇与钩子`。
3. 爽点弱或读者弃读：走 `期待感与情绪`。
4. 剧情写散：走 `单元故事起承转合`。
5. 写完高潮后追读掉：走 `长线结构与不断档`。
6. 想学习一本书：走 `拆书取证`，只为当前问题取证。
7. 想按题材训练：走 `genre-modules/`，再从 `case-library/按题材/` 取样。
8. 想系统入门：走 `curriculum/新人等级路径.md`。
9. 想查人工精拆：走 `case-library/精拆/manual-ledger.md`。

# 可检索案例库

全库遍历后，系统从 34739 个 Markdown 文件中抽取 12496 条案例记录。

## 文件

- `case-index.jsonl`：机器可读案例库，每行一个案例。
- `case-index.csv`：表格版案例库。
- `case-cards.jsonl`：按案例类型、课程等级、题材、模块拆好的结构化案例卡。
- `case-cards.csv`：表格版结构化案例卡。
- `案例库总表.md`：高权重案例和题材计数。
- `按题材/*.md`：每个题材的前 500 条高权重案例。

## 推荐检索

PowerShell：

```powershell
Import-Csv .\case-library\case-index.csv | Where-Object { $_.topics -like '*开篇*' -and $_.genres -like '*悬疑灵异规则怪谈*' } | Select-Object -First 20 title,relpath
```

ripgrep：

```powershell
rg "规则怪谈|开篇|期待感" .\case-library\case-index.jsonl
```

## 使用规则

先从案例库筛样本，再进入 `modules/module-拆书取证.md`。不要把案例库当阅读清单，它是取证入口。

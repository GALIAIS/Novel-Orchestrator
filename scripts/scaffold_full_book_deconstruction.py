#!/usr/bin/env python3
"""Create a full-book deconstruction workspace from a novel text file."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


HEADING_RE = re.compile(
    r"^\s*(第[零一二三四五六七八九十百千万\d]+[章节回卷][^\n]{0,80}|"
    r"Chapter\s+\d+[^\n]{0,80}|"
    r"\d{1,4}[\.、]\s*[^\n]{2,80})\s*$",
    re.IGNORECASE,
)


@dataclass
class Section:
    number: int
    title: str
    text: str
    start_line: int
    end_line: int

    @property
    def chars(self) -> int:
        return len(self.text)


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def detect_sections(text: str, chunk_chars: int) -> list[Section]:
    lines = text.splitlines()
    headings = [(i, line.strip()) for i, line in enumerate(lines) if HEADING_RE.match(line)]
    if len(headings) >= 3:
        sections: list[Section] = []
        for idx, (start, title) in enumerate(headings):
            end = headings[idx + 1][0] if idx + 1 < len(headings) else len(lines)
            body = "\n".join(lines[start:end]).strip()
            sections.append(Section(idx + 1, title, body, start + 1, end))
        return sections

    sections = []
    for idx, start in enumerate(range(0, len(text), chunk_chars), 1):
        body = text[start : start + chunk_chars]
        sections.append(Section(idx, f"切块{idx:03d}", body, 0, 0))
    return sections


def format_markdown(text: str) -> str:
    blocks = text.split("\n\n")
    formatted: list[str] = []
    for block in blocks:
        lines = block.splitlines()
        field_lines = [line for line in lines if "：" in line and not line.lstrip().startswith(("|", "#", "-"))]
        if len(field_lines) >= 2 and len(field_lines) == len([line for line in lines if line.strip()]):
            rows = ["| 字段 | 内容 |", "|---|---|"]
            for line in lines:
                key, value = line.split("：", 1)
                rows.append(f"| {md_escape(key.strip())} | {md_escape(value.strip())} |")
            formatted.append("\n".join(rows))
        else:
            formatted.append(block)
    return "\n\n".join(formatted)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".md":
        text = format_markdown(text)
    path.write_text(text, encoding="utf-8", newline="\n")


def md_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def build_index(sections: list[Section]) -> str:
    rows = ["# 章节索引", "", "| 卷 | 章号 | 标题 | 字数 | 起止位置 |", "|---|---:|---|---:|---|"]
    for section in sections:
        pos = f"L{section.start_line}-L{section.end_line}" if section.start_line else "chunk"
        rows.append(f"| 待分卷 | {section.number:03d} | {md_escape(section.title)} | {section.chars} | {pos} |")
    return "\n".join(rows) + "\n"


def build_ledger(sections: list[Section], per_volume: int) -> str:
    rows = ["# coverage-ledger", "", "| 范围 | 状态 | 证据文件 | 待回补 |", "|---|---|---|---|"]
    for section in sections:
        volume = ((section.number - 1) // per_volume) + 1
        rows.append(f"| 第{section.number:03d}章 | 待拆 | 16-卷级精拆/vol-{volume:02d}-卷级精拆.md |  |")
    return "\n".join(rows) + "\n"


def character_template(category: str) -> str:
    return f"""# 角色-001-待命名

## 基础档案

角色分类：{category}
姓名/称号：
首次登场：
退场/当前状态：
出场章节清单：
原文证据：
身份定位：
社会身份：
阵营/势力：
职业/能力标签：
读者第一印象：

## 外貌与识别

年龄/阶段：
性别/称谓：
体貌特征：
服装道具：
气质关键词：
标志性动作：
标志性语言：
外貌变化：
他人视角评价：
镜头呈现方式：

## 性格与心理

显性性格：
隐性性格：
核心欲望：
核心恐惧：
价值观：
底线：
软肋：
执念：
自我认知：
外界误判：
性格矛盾：
压力下反应：

## 成长与变化

初始状态：
阶段目标：
关键选择：
成长节点：
性格变化：
能力变化：
地位变化：
关系变化：
代价：
最终状态：
变化是否可信：

## 剧情功能

主线功能：
单元功能：
期待功能：
冲突功能：
伏笔功能：
见证功能：
情绪功能：
爽点功能：
不可替代性：
可合并风险：

## 关系网络

与主角关系：
与主要角色关系：
与配角关系：
与反派关系：
关系推进节点：
关系反转节点：
利益绑定：
情感绑定：
冲突绑定：

## 表演证据

代表行动：
代表台词：
代表选择：
代表失误：
代表高光：
他人反应：
读者期待：
兑现/反转：

## 写作拆解

登场设计：
人物立住的第一场戏：
持续记忆点：
信息揭示顺序：
人物弧线写法：
可迁移写法：
不可迁移原因：
仿写训练：

"""


CATEGORY_TEMPLATES = {
    "03-题材承诺/01-读者承诺/01-读者承诺总表.md": """# 读者承诺

目标读者：
一句话承诺：
核心卖点：
差异化钩子：
同题材参照：
读者禁区：
开篇兑现：
阶段兑现：
长线承诺：
承诺断档风险：
可迁移承诺：

""",
    "04-世界观设定/01-基础规则/规则-001-待命名.md": """# 规则-001-待命名

规则名称：
所属层级：历史/地理/技术/社会/禁忌/常识
首次出现：
原文证据：
规则内容：
限制边界：
例外条件：
代价：
违反后果：
剧情用途：
制造期待：
兑现/破坏位置：
与角色关系：
与主线关系：
与力量体系关系：
可迁移风险：

""",
    "04-世界观设定/02-设定条目/设定-001-待命名.md": """# 设定-001-待命名

设定名称：
首次出现：
原文证据：
读者当时理解：
真实用途：
揭示方式：
使用场景：
后续变化：
风险：
相关角色：
相关事件：
相关伏笔：
可删性：

""",
    "04-世界观设定/99-设定揭示台账.md": """# 设定揭示台账

| 设定 | 首次揭示 | 解决的问题 | 制造的期待 | 兑现位置 | 备注 |
|---|---|---|---|---|---|

""",
    "05-力量金手指/01-力量体系/体系-001-待命名.md": """# 体系-001-待命名

力量来源：
等级/晋升：
消耗代价：
限制：
克制关系：
训练/获取门槛：
失败惩罚：
展示顺序：
展示场景：
与世界观绑定：
与主角弧线绑定：

""",
    "05-力量金手指/02-金手指条目/金手指-001-待命名.md": """# 金手指-001-待命名

获得方式：
可用范围：
升级条件：
奖励：
滥用边界：
主线绑定：
首次爽点：
阶段扩容：
关键破局：
反噬/代价：

""",
    "05-力量金手指/03-技能道具/条目-001-待命名.md": """# 技能/道具-001-待命名

名称：
来源：
首次出现：
原文证据：
能力效果：
限制代价：
使用次数：
使用条件：
克制对象：
关键破局：
后续升级：
是否可替代：

""",
    "05-力量金手指/99-力量金手指总表.md": """# 力量金手指总表

| 条目 | 类型 | 首次出现 | 能力/效果 | 限制 | 关键用途 | 后续变化 |
|---|---|---|---|---|---|---|

""",
    "06-大纲主线/01-全书主线/01-全书主线.md": """# 全书主线

终局想象：
主要矛盾：
主角最终变化：
长期反派/长期问题：
阶段推进：
防烂尾资源：
终局回收池：
可扩展支线：
必须回收支线：
断主线风险：

""",
    "06-大纲主线/02-阶段主线/阶段-001-待命名.md": """# 阶段-001-待命名

章节范围：
阶段目标：
主要矛盾：
主角状态：
敌我格局：
资源变化：
高潮兑现：
下一阶段接档：
未回收问题：
读者期待库存：
风险：

""",
    "06-大纲主线/03-支线源流/支线-001-待命名.md": """# 支线-001-待命名

支线名称：
来源：
首次出现：
原文证据：
功能：
回流主线方式：
删除代价：
当前状态：
关联角色：
关联设定：
回收位置：
拖累风险：

""",
    "06-大纲主线/99-支线源流总表.md": """# 支线源流总表

| 支线 | 来源 | 功能 | 回流主线方式 | 删除代价 | 状态 |
|---|---|---|---|---|---|

""",
    "07-卷章结构/01-卷级结构表/01-卷级结构表.md": """# 卷级结构表

| 卷 | 章节范围 | 卷级承诺 | 核心矛盾 | 高潮 | 收获 | 下一卷接档 |
|---|---|---|---|---|---|---|

""",
    "07-卷章结构/02-单元结构表/单元-001-待命名.md": """# 单元-001-待命名

章节范围：
单元承诺：
起因：
起：
承：
转：
合：
爽点/情绪释放：
主角收获：
代价/新麻烦：
关系变化：
下一扣子：

""",
    "07-卷章结构/03-章节功能/章节-001-待命名.md": """# 章节-001-待命名

章号：
标题：
一句话事件：
章节功能：
主角目标：
阻碍/信息差：
期待：
兑现/压制：
新增信息：
人物关系变化：
伏笔/回收：
章尾钩子：
可迁移写法：

""",
    "07-卷章结构/04-节奏曲线/01-节奏曲线.md": """# 节奏曲线

高压/低压：
解释/行动比例：
爽点密度：
高潮间距：
断档点：
修补方式：
解释密度：
行动密度：
情绪峰谷：
追读风险：

""",
    "08-角色拆解/00-角色总表.md": """# 角色总表

| 角色 | 分类 | 首次登场 | 核心功能 | 与主角关系 | 弧线变化 | 独立文档 |
|---|---|---|---|---|---|---|

""",
    "08-角色拆解/01-主要角色/角色-001-待命名.md": character_template("主要角色"),
    "08-角色拆解/02-重要配角/角色-001-待命名.md": character_template("重要配角"),
    "08-角色拆解/03-反派角色/角色-001-待命名.md": character_template("反派角色"),
    "08-角色拆解/04-功能角色/角色-001-待命名.md": character_template("功能角色"),
    "09-关系势力/01-关系线/关系-001-待命名.md": """# 关系-001-待命名

关系双方：
初始状态：
首次出现：
原文证据：
变化事件：
见证功能：
资源/阻碍：
当前状态：
后续期待：
权力变化：
情感变化：
利益变化：
断裂/修复节点：

""",
    "09-关系势力/02-组织势力/势力-001-待命名.md": """# 势力-001-待命名

名称：
首次出现：
原文证据：
目标：
资源：
行动方式：
与主角关系：
阶段变化：
威胁/帮助：
内部层级：
关键成员：
资源清单：
弱点：
覆灭/升级条件：

""",
    "09-关系势力/03-资源道具/资源-001-待命名.md": """# 资源-001-待命名

资源名称：
类型：
首次出现：
原文证据：
获取方式：
消耗方式：
回收方式：
升级方式：
服务剧情：
绑定角色：
绑定势力：
关键代价：
后续风险：

""",
    "09-关系势力/99-关系势力总表.md": """# 关系势力总表

| 名称 | 目标 | 资源 | 行动方式 | 与主角关系 | 阶段变化 |
|---|---|---|---|---|---|

| 资源/道具 | 获取 | 消耗 | 回收 | 升级 | 证据 |
|---|---|---|---|---|---|

""",
    "10-情节冲突/01-事件链/事件-001-待命名.md": """# 事件-001-待命名

事件范围：
事件源：
主角为何必须处理：
主角行动：
阻碍升级：
转折机制：
结果：
收益/代价：
后续问题：
参与角色：
相关设定：
相关伏笔：
期待变化：
情绪变化：

""",
    "10-情节冲突/02-转折节点/转折-001-待命名.md": """# 转折-001-待命名

位置：
原文证据：
转折类型：新信息/新代价/新误判/新规则/关系变化
转折前期待：
转折后问题：
合理性铺垫：
后续兑现：
影响角色：
影响主线：
风险：

""",
    "10-情节冲突/98-事件源与转折总表.md": """# 事件源与转折总表

| 范围 | 事件源 | 主角为何必须处理 | 主角行动 | 阻碍升级 | 转折机制 | 结果 |
|---|---|---|---|---|---|---|

""",
    "10-情节冲突/99-章节功能总表.md": """# 章节功能总表

| 章 | 事件 | 功能 | 主角行动 | 阻碍/信息差 | 兑现/压制 | 章尾钩子 |
|---|---|---|---|---|---|---|

""",
    "11-期待情绪/01-期待链/期待-001-待命名.md": """# 期待-001-待命名

范围：
期待形成：
压制/延迟：
局部兑现：
大兑现：
见证反应：
新期待：
断档风险：
期待来源：
读者想看的画面：
失败代价：
延迟手段：

""",
    "11-期待情绪/02-爽点链/爽点-001-待命名.md": """# 爽点-001-待命名

铺垫：
欠账/误判：
底牌：
爆发：
见证：
收获：
余波：
后续接法：
铺垫章节：
压制强度：
反派/旁观者反应：
主角状态变化：

""",
    "11-期待情绪/03-情绪线/情绪-001-待命名.md": """# 情绪-001-待命名

范围：
起始情绪：
拉扯方式：
释放点：
余波：
风险：
触发角色：
情绪转换：
读者感受：
回落方式：

""",
    "11-期待情绪/98-期待爽点总表.md": """# 期待爽点总表

| 范围 | 期待形成 | 压制/延迟 | 兑现 | 见证反应 | 新期待 |
|---|---|---|---|---|---|

""",
    "11-期待情绪/99-情绪线总表.md": """# 情绪线总表

| 范围 | 起始情绪 | 拉扯方式 | 释放点 | 余波 | 风险 |
|---|---|---|---|---|---|

""",
    "12-伏笔信息/01-伏笔条目/伏笔-001-待命名.md": """# 伏笔-001-待命名

埋设位置：
原文证据：
当时理解：
真实用途：
回收位置：
回收收益：
是否公平：
后续影响：
埋设方式：
伪装信息：
关联角色：
关联设定：
二次利用：

""",
    "12-伏笔信息/02-信息差条目/信息差-001-待命名.md": """# 信息差-001-待命名

位置：
谁知道：
谁不知道：
读者知道多少：
隐藏方式：
阶段答案：
最终答案：
制造期待：
误导方式：
揭晓节奏：
对角色行动的影响：

""",
    "12-伏笔信息/03-悬念条目/悬念-001-待命名.md": """# 悬念-001-待命名

谜面：
线索：
误导：
阶段答案：
最终答案：
兑现位置：
风险：
误导对象：
答案分层：
回收收益：

""",
    "12-伏笔信息/98-伏笔回收台账.md": """# 伏笔回收台账

| 伏笔 | 埋设位置 | 当时理解 | 真实用途 | 回收位置 | 回收收益 |
|---|---|---|---|---|---|

""",
    "12-伏笔信息/99-信息差与悬念总表.md": """# 信息差与悬念总表

| 位置 | 信息差/悬念 | 谁知道 | 谁不知道 | 阶段答案 | 最终答案 |
|---|---|---|---|---|---|

""",
    "13-叙事技法/01-开篇技法/01-开篇技法.md": """# 开篇技法

开篇钩子：
开篇六要素：
第一章承诺：
第一单元闭合：
两长一短：
信息投放：
读者追问：

""",
    "13-叙事技法/02-场景写法/场景-001-待命名.md": """# 场景-001-待命名

场景目标：
冲突：
反应：
信息展示：
转场：
可迁移写法：
视角：
场景压力：
人物调度：
节奏变化：
结尾落点：

""",
    "13-叙事技法/03-对话写法/对话-001-待命名.md": """# 对话-001-待命名

话外意图：
关系变化：
信息差：
节奏：
角色声口：
可迁移写法：
潜台词：
攻防关系：
信息增量：
情绪变化：
是否可删：

""",
    "13-叙事技法/04-说明镜头/说明-001-待命名.md": """# 说明-001-待命名

设定插入位置：
解释后用途：
视角选择：
信息先后：
特写/反应镜头：
高潮落点：
说明触发点：
说明长度：
行动承接：
读者负担：

""",
    "14-商业包装/01-外部承诺/01-外部承诺.md": """# 外部承诺

书名承诺：
简介承诺：
标签卖点：
平台适配：
开篇兑现：
不可照搬边界：
目标读者：
竞品参照：
卖点排序：
平台风险：
商业化强项：

""",
    "14-商业包装/02-标题与追读/标题-001-待命名.md": """# 标题-001-待命名

位置：
章节标题/外部信息：
制造期待：
正文兑现：
风险：
标题钩子类型：
章末追读：
承诺偏差：

""",
    "14-商业包装/99-标题与追读总表.md": """# 标题与追读总表

| 位置 | 章节标题/外部信息 | 制造的期待 | 正文兑现 | 风险 |
|---|---|---|---|---|

""",
    "15-迁移训练/01-可迁移模板/模板-001-待命名.md": """# 模板-001-待命名

原文功能：
适用条件：
改写步骤：
不可迁移风险：
训练动作：
适用题材：
必备前置条件：
替换变量：
验收标准：

""",
    "15-迁移训练/99-可迁移模板总表.md": """# 可迁移模板总表

| 模板 | 原文功能 | 适用条件 | 改写步骤 | 不可迁移风险 |
|---|---|---|---|---|

""",
    "15-迁移训练/02-仿写任务/任务-001-待命名.md": """# 任务-001-待命名

拆到的结构：
我的题材：
改写桥段：
回写大纲位置：
验收标准：
训练目标：
原文参照：
限制条件：
复盘问题：

""",
}


def chapter_stub(section: Section) -> str:
    return f"""### 第{section.number:03d}章：{section.title}

本章一句话事件：
章节功能：
主角目标：
阻碍或信息差：
读者期待：
压制或拉扯：
兑现或未兑现：
新增信息：
人物关系变化：
章尾钩子：
可迁移写法：

"""


def build_volume(volume_no: int, sections: list[Section]) -> str:
    start = sections[0].number
    end = sections[-1].number
    body = [
        f"# Vol {volume_no:02d} 卷级精拆（第{start:03d}-{end:03d}章）",
        "",
        "## 卷级概览",
        "",
        "卷级承诺：",
        "核心矛盾：",
        "阶段目标：",
        "高潮兑现：",
        "下一卷接档：",
        "",
        "## 章节功能表",
        "",
    ]
    body.extend(chapter_stub(section) for section in sections)
    body.extend(
        [
            "## 单元复盘",
            "",
            "单元范围：",
            "起：",
            "承：",
            "转：",
            "合：",
            "收获：",
            "下一扣子：",
            "",
        ]
    )
    return "\n".join(body)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold full-book deconstruction files.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--chapters-per-volume", type=int, default=30)
    parser.add_argument("--chunk-chars", type=int, default=8000)
    parser.add_argument("--write-source-chunks", action="store_true")
    args = parser.parse_args()

    source = args.source
    out = args.out or source.with_name(f"{source.stem}-拆书")
    sections = detect_sections(read_text(source), args.chunk_chars)
    per_volume = max(args.chapters_per_volume, 1)

    write(
        out / "00-项目说明" / "00-拆书说明.md",
        f"""# 拆书说明

书名：{source.stem}
来源文件：{source.name}
拆书目标：
拆解粒度：章 -> 单元 -> 卷 -> 题材/世界观/力量/大纲/卷章/角色/关系/冲突/期待/伏笔/技法/包装/迁移 -> 全书
章节识别：{len(sections)} 个章节/切块
缺失/乱码/不可读范围：

""",
    )
    write(out / "01-章节索引" / "01-章节索引.md", build_index(sections))
    write(
        out / "02-全书总览" / "01-全书承诺与核心循环.md",
        "# 全书承诺与核心循环\n\n题材承诺：\n主角路线：\n金手指/核心资源：\n主要矛盾：\n重复循环：\n长线期待：\n\n",
    )
    for rel_path, template in CATEGORY_TEMPLATES.items():
        write(out / rel_path, template)
    write(out / "01-章节索引" / "02-coverage-ledger.md", build_ledger(sections, per_volume))

    for idx in range(0, len(sections), per_volume):
        volume = (idx // per_volume) + 1
        write(out / "16-卷级精拆" / f"vol-{volume:02d}-卷级精拆.md", build_volume(volume, sections[idx : idx + per_volume]))

    write(
        out / "99-总报告" / "99-总报告.md",
        "# 总报告\n\n全书承诺：\n核心循环：\n题材承诺：\n世界观设定：\n力量金手指：\n大纲主线：\n卷章结构：\n角色拆解：\n关系势力：\n情节冲突：\n期待情绪：\n伏笔信息：\n叙事技法：\n商业包装：\n迁移训练：\n强项：\n弱点：\n不能照搬的风险：\n仿写训练：\n\n",
    )

    if args.write_source_chunks:
        for section in sections:
            write(out / "17-原文切块" / f"chapter-{section.number:03d}.txt", section.text + "\n")

    print(f"created={out}")
    print(f"sections={len(sections)}")


if __name__ == "__main__":
    main()

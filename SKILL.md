---
name: create-master
description: 基于佛教经典文献，生成特定高僧大德的 AI 教学角色
argument-hint: <法师名称>
version: 1.0.0
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebFetch
---

# Buddha-skill — 佛教法师教学角色生成器

本内容依据历史佛教文献生成，仅供参考学习。如需正式修行指导，请亲近善知识。

## 触发条件

以下方式均可触发：
- `/create-master` 或 `/create-master <法师名>`
- "帮我创建一个印光大师的教学角色"
- "生成阿姜查的 AI Skill"
- "我想和宗喀巴大师学习"

## 预置法师

以下法师可直接使用，无需生成：

**汉传（7位）**
- `/xuanzang` — 玄奘法师（法相唯识宗）
- `/kumarajiva` — 鸠摩罗什（三论宗/中观）
- `/huineng` — 慧能大师（禅宗六祖）
- `/zhiyi` — 智顗大师（天台宗）
- `/fazang` — 法藏大师（华严宗）
- `/yinguang` — 印光大师（净土宗）
- `/ouyi` — 蕅益大师（天台/净土·跨宗派）
- `/xuyun` — 虚云老和尚（禅宗·五宗兼嗣）

**南传（1位）**
- `/ajahn-chah` — 阿姜查（泰国森林传承）

**藏传（1位）**
- `/tsongkhapa` — 宗喀巴大师（格鲁派）

## 主流程

### Step 1：信息录入

加载 `${CLAUDE_SKILL_DIR}/prompts/intake.md`，按照 3 问模式收集信息：
1. 法师名称 → 自动匹配 FoJin 知识图谱
2. 关注方面 → 教义/修行/讲解/全部
3. 语言偏好 → 根据传承自动推荐

### Step 2：数据采集

使用 `${CLAUDE_SKILL_DIR}/tools/sutra_collector.py` 从 FoJin 采集数据：

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/sutra_collector.py --name "<法师名>" --tradition "<传承>"
```

采集内容包括：
- 知识图谱实体和师承关系
- 相关经典列表和内容摘录
- 传承相关术语

### Step 3：分析与生成

**运行时检索规则**：加载 `${CLAUDE_SKILL_DIR}/prompts/rag_instructions.md`，将其中的检索指引嵌入生成的每个法师 SKILL.md 的运行规则中，确保法师回答时调用 FoJin 实时检索而非仅依赖 LLM 自身知识。

**教义分析**：加载 `${CLAUDE_SKILL_DIR}/prompts/sutra_analyzer.md`，填入采集数据，分析教义结构。

**风格分析**：加载 `${CLAUDE_SKILL_DIR}/prompts/voice_analyzer.md`，填入采集数据，分析说法风格。

**教义生成**：加载 `${CLAUDE_SKILL_DIR}/prompts/teaching_builder.md`，基于分析结果生成 teaching.md。

**风格生成**：加载 `${CLAUDE_SKILL_DIR}/prompts/voice_builder.md`，基于分析结果生成 voice.md。

### Step 4：预览与确认

展示生成的 teaching.md 和 voice.md 预览，请用户确认。

### Step 5：写入文件

使用 `${CLAUDE_SKILL_DIR}/tools/skill_writer.py` 写入文件：

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/master_builder.py --name "<法师名>" --output masters/
```

生成目录结构：
```
masters/{slug}/
├── SKILL.md          # /{slug} 触发
├── teaching.md       # 教义体系
├── voice.md          # 说法风格
└── meta.json         # 元数据
```

## 追加材料（进化模式）

用户可以追加新的经文材料来增强已有法师：
- "给印光大师追加《文钞三编》的材料"
- "用这段语录更新阿姜查的说法风格"

加载 `${CLAUDE_SKILL_DIR}/prompts/merger.md` 进行增量合并。

## 管理命令

- `/list-masters` — 列出所有已生成的法师
- `/master-rollback <slug> <version>` — 回滚到指定版本
- `/delete-master <slug>` — 删除一个法师

## 工具路由

| 任务 | 工具 |
|------|------|
| FoJin 数据查询 | `${CLAUDE_SKILL_DIR}/tools/fojin_bridge.py` |
| FoJin 实时检索 | `${CLAUDE_SKILL_DIR}/tools/rag_query.py` |
| 经文采集 | `${CLAUDE_SKILL_DIR}/tools/sutra_collector.py` |
| 角色生成 | `${CLAUDE_SKILL_DIR}/tools/master_builder.py` |
| 文件写入 | `${CLAUDE_SKILL_DIR}/tools/skill_writer.py` |
| 版本管理 | `${CLAUDE_SKILL_DIR}/tools/version_manager.py` |

## 敏感性边界

**不做：**
- 不对宗派优劣进行评判
- 不做个人修行诊断（业力、前世等）
- 不宣称神通感应
- 不涉及政治化宗教议题
- 不给出医疗建议

**要做：**
- 忠实依据经文原文，所有回答附 FoJin 出处链接
- 通过 rag_query.py 实时检索真实经文
- 遇到超出范围的问题坦诚说明
- 鼓励用户亲近善知识、依止真实导师

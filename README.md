# buddha-skill

基于佛教经典文献的法师教学角色生成器，遵循 AgentSkills 标准，由 [FoJin](https://fojin.app) 驱动。

---

## 严肃性声明

本项目本着对佛教传统的尊重而建立。所有角色内容均忠实依据历史文献生成，不做教义评判，不声称代表任何宗派权威。生成内容仅供学习参考，如需正式修行指导，请亲近善知识、依止有德行的真实导师。

本项目不模拟任何在世宗教领袖。

---

## 特性

- **预置三位法师**：涵盖南传（阿姜查）、汉传（印光大师）、藏传（宗喀巴大师），开箱即用
- **FoJin 数据桥**：接入 [fojin.app](https://fojin.app) 的 503 个数据源、10K+ 文本、678K+ 语义向量和 31K 实体知识图谱
- **AgentSkills 标准**：遵循 AgentSkills 规范，可作为子技能被其他 Agent 调用
- **双模输出**：每位法师生成 `teaching.md`（教义体系）和 `voice.md`（说法风格）两份文件
- **增量进化**：已生成的法师可追加新经文材料进行增量合并，角色持续完善
- **版本管理**：内置版本号与时间戳，支持回滚到任意历史版本

---

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 使用预置法师

在支持 AgentSkills 的环境中直接调用：

```
/ajahn-chah     — 阿姜查（南传·泰国森林传承）
/yinguang       — 印光大师（汉传·净土宗）
/tsongkhapa     — 宗喀巴大师（藏传·格鲁派）
```

### 自定义生成

```
/create-teacher 虚云老和尚
```

或自然语言触发：

```
帮我创建一个虚云老和尚的教学角色
```

系统将引导完成三步信息录入，然后自动从 FoJin 采集数据、生成教义分析与风格文件。

---

## 预置法师

### 阿姜查（Ajahn Chah，1918-1992）

泰国森林传承比丘，南传上座部代表人物之一。
以直接、朴实的禅修指导著称，善用日常比喻讲解无常、苦、无我。
主要来源：SuttaCentral 巴利藏，含《大念处经》《法轮转起经》等核心经典。
调用命令：`/ajahn-chah`

### 印光大师（1861-1940）

汉传净土宗第十三代祖师，近代净土复兴的核心人物。
文字平实恳切，戒行严谨，以书信形式广度众生，著有《印光法师文钞》三编。
主要来源：CBETA 汉文大藏经，含文钞正编、续编、三编及净土三经。
调用命令：`/yinguang`

### 宗喀巴大师（ཙོང་ཁ་པ，1357-1419）

藏传佛教格鲁派创立者，佛教史上最具系统性的论师之一。
以《菩提道次第广论》构建完整修行次第，融合显密，判教严密。
主要来源：《菩提道次第广论》《密宗道次第广论》《三主要道》等。
调用命令：`/tsongkhapa`

---

## 架构图

```
用户请求
    │
    ▼
SKILL.md (AgentSkills 入口)
    │
    ├─ 预置法师 ──────────────────────► prebuilt/{slug}/
    │                                        ├── SKILL.md
    │                                        ├── teaching.md
    │                                        ├── voice.md
    │                                        └── meta.json
    │
    └─ 自定义生成
          │
          ├─ prompts/intake.md          (信息录入)
          │
          ├─ tools/sutra_collector.py
          │       │
          │       └──► FoJin API ───► 知识图谱 + 语义检索 + 经文文本
          │
          ├─ prompts/sutra_analyzer.md  (教义分析)
          ├─ prompts/voice_analyzer.md  (风格分析)
          ├─ prompts/teaching_builder.md
          ├─ prompts/voice_builder.md
          │
          ├─ tools/teacher_builder.py   (角色构建)
          ├─ tools/skill_writer.py      (文件写入)
          └─ tools/version_manager.py  (版本管理)
                │
                ▼
          teachers/{slug}/
              ├── SKILL.md
              ├── teaching.md
              ├── voice.md
              └── meta.json
```

---

## 与 FoJin 的关系

[FoJin](https://fojin.app) 是一个佛教文本聚合平台，整合了 503 个数据源、10K+ 篇文本、678K+ 条语义向量嵌入，以及涵盖 31K 实体的知识图谱，覆盖 CBETA 汉文大藏经、SuttaCentral 巴利藏及英译、84000 藏经英译等主要语料库。

buddha-skill 通过 `tools/fojin_bridge.py` 接入 FoJin API，实现：

- 知识图谱实体检索（法师生平、师承、宗派）
- 语义向量相似度搜索（教义相关经文）
- 原文段落提取与出处追踪

所有引用均附带可追溯的 FoJin 链接，确保内容来源透明。

---

## 敏感性边界

**明确不做：**

- 不模拟任何在世宗教领袖
- 不对宗派优劣进行评判
- 不做个人修行诊断（业力、前世等）
- 不声称神通感应或灵验体验
- 不涉及政治化宗教议题
- 不给出任何医疗建议

**明确要做：**

- 忠实引用经文原文，不曲解不发挥
- 每个回答附可追溯出处（FoJin 链接）
- 遇到超出范围的问题坦诚说明
- 鼓励用户亲近善知识、依止真实修行

---

## 贡献指南

欢迎提交新的预置法师（请在 `prebuilt/` 目录下按已有格式创建）、修正文献来源错误，或改进工具链。

提交前请确认：文献来源可追溯，内容忠实于历史文献，无宗派偏见。

---

## 许可证

MIT License

---

## 致谢

- [FoJin](https://fojin.app) — 提供核心数据支撑
- [colleague-skill](https://github.com/xr843/colleague-skill) — AgentSkills 架构设计启发
- [CBETA](https://cbeta.org) — 汉文大藏经数字化
- [SuttaCentral](https://suttacentral.net) — 巴利藏及多语种译本
- [84000](https://84000.co) — 藏经英译项目

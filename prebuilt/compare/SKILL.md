---
name: compare-masters
description: 同一佛学问题，由2-3位汉传祖师分别以各自风格回答，展现宗派视角差异
user-invocable: true
---

# 多法师对比

本内容依据佛教经典文献生成，仅供参考学习。

## 路径约定

本 skill 位于 `prebuilt/compare/`，项目根目录在上两级。本文中提到的工具和数据路径定位方式：

```bash
# 推荐：从 SKILL 路径回溯项目根
SKILL_FILE="$(readlink -f "${CLAUDE_SKILL_DIR}/SKILL.md" 2>/dev/null)"
PROJECT_ROOT="$(dirname "$(dirname "$(dirname "$SKILL_FILE")")")"

# 降级方案（按顺序尝试）：
# 1. $HOME/projects/master-skill       （开发环境）
# 2. $HOME/Master-skill                 （手动 clone）
# 3. $HOME/.openclaw/workspace/skills/create-master  （OpenClaw）
```

后续所有工具路径均以 `$PROJECT_ROOT` 为前缀。

## 触发方式

- `/compare-masters` + 问题 + 可选的法师列表
- "请慧能和印光对比回答..."
- "比较禅宗和净土宗对念佛的看法"

## 工作流程

### Step 1：确定对比法师

**优先级 1 — 用户显式指定**

用户可以通过以下方式显式指定法师：
- `/compare-masters <问题> --masters xuanzang,zhiyi,ouyi`
- "请慧能和印光对比回答..."
- "用玄奘、智顗、蕅益三位对比..."

若用户指定，直接使用（最多取前 3 位），跳过后续选择步骤。

**优先级 2 — 基于关键词智能匹配（无用户指定时）**

读取每位法师的 `meta.json`（路径参考 Step 2 的项目根定位逻辑）中 `search_scope.keywords` 字段，执行以下匹配流程：

1. **提取问题核心概念**：从用户问题中提取 2-4 个佛学关键词（术语、概念、法门）
2. **与 8 位法师的 keywords 字段比对**：记录每位法师的匹配次数和匹配强度
3. **按匹配度排序**：取 top 2-3 位（匹配度相近时，优先选择不同宗派的法师以呈现多元视角）
4. **匹配度判定**：
   - 强匹配（问题关键词直接出现在法师 keywords 中）：权重 3
   - 相关匹配（问题关键词属于该法师传承的核心概念领域）：权重 2
   - 弱匹配（仅部分字面重叠）：权重 1

**优先级 3 — 主题映射兜底（关键词无强匹配时）**

若 top 2 法师匹配度均 ≤ 1（即没有清晰的关键词匹配），则按以下主题映射兜底：

| 问题主题 | 配对法师 | 说明 |
|---------|---------|------|
| 念佛 / 往生 / 净土 | yinguang + ouyi | 净土专精 + 跨宗派视角 |
| 参禅 / 话头 / 开悟 / 见性 | huineng + xuyun | 古今禅宗对比 |
| 唯识 / 中观 / 空有 / 因缘 / 六因 | xuanzang + kumarajiva | 唯识 vs 中观 |
| 判教 / 圆融 / 止观 / 法界 | zhiyi + fazang | 天台 vs 华严 |
| 修行次第 / 综合法门 | ouyi + yinguang | 综合 vs 专修 |
| 戒律 / 行持 / 日常 | xuyun + yinguang | 禅门戒律 vs 净土行持 |
| 般若 / 空性 | kumarajiva + huineng | 中观 vs 禅宗体认 |
| 心识 / 本性 / 阿赖耶 | xuanzang + huineng | 唯识分析 vs 禅宗直指 |
| 其他不明主题 | kumarajiva + yinguang | 代表两大传统（中观/净土） |

**可选法师（8位汉传祖师大德）：**
- xuanzang（玄奘·唯识）
- kumarajiva（鸠摩罗什·中观）
- huineng（慧能·禅宗）
- zhiyi（智顗·天台）
- fazang（法藏·华严）
- yinguang（印光·净土）
- ouyi（蕅益·跨宗派）
- xuyun（虚云·禅宗五宗）

**选择完成后**：输出选择理由，格式如下：

```
法师选择：
- {master_A}：{"关键词强匹配：xxx, yyy" 或 "主题映射：xxx"}
- {master_B}：{"关键词匹配：xxx" 或 "主题互补视角：xxx"}
（可用 --masters xxx,yyy 手动覆盖）
```

**精准反馈示例**：
- 用户问"什么是遍行因" → "xuanzang：强关键词匹配（遍行因、六因、因、唯识、种子），kumarajiva：主题互补（中观视角对比唯识六因）"
- 用户问"念佛" → "yinguang：强关键词匹配（念佛、持名念佛、往生），ouyi：关键词匹配（念佛、持名念佛、信愿）"
- 用户问"如何修行" → "按通用主题映射（修行次第 → ouyi + yinguang）"

### Step 2：对每位法师执行 RAG 检索

对每位选定的法师：

1. **定位项目根目录**（`compare` 是 `prebuilt/compare/`，项目根在上两级）。按以下顺序尝试：
   ```bash
   # 方法 A：从 SKILL 目录回溯（symlink 解析）
   SKILL_FILE="$(readlink -f "${CLAUDE_SKILL_DIR}/SKILL.md" 2>/dev/null || echo "")"
   if [ -n "$SKILL_FILE" ]; then
     PROJECT_ROOT="$(dirname "$(dirname "$(dirname "$SKILL_FILE")")")"
   fi

   # 方法 B：已知的开发路径
   [ -z "$PROJECT_ROOT" ] && PROJECT_ROOT="$HOME/projects/master-skill"
   [ ! -f "$PROJECT_ROOT/tools/rag_query.py" ] && PROJECT_ROOT="$HOME/Master-skill"

   # 方法 C：OpenClaw 默认路径
   [ ! -f "$PROJECT_ROOT/tools/rag_query.py" ] && PROJECT_ROOT="$HOME/.openclaw/workspace/skills/create-master"
   ```

2. **加载法师角色内容**：`$PROJECT_ROOT/prebuilt/{slug}/teaching.md` 和 `voice.md`

3. **⚠️ 必须：为每位法师执行独立的语义检索**（不可合并为一次查询）

   为什么必须独立：不同传承有不同的术语体系。一次合并查询会偏向某一传承的术语，导致另一位法师只能得到**降级的搜索链接**（如 `fojin.app/search?q=...`）而非精准的 text_id 直链。

   **为每位法师构造传承专属查询词**（将用户原问题用该法师的术语体系改写）：

   | 法师 | 查询词改写策略 | 示例（用户问"因缘果"） |
   |------|-------------|---------------------|
   | xuanzang（唯识） | 加入唯识/俱舍术语 | "因缘果 六因 四缘 五果 种子" |
   | kumarajiva（中观） | 加入般若/中观术语 | "因缘所生法 空 中道 无自性 四句" |
   | huineng（禅宗） | 加入禅宗术语 | "自性 本心 见性 顿悟" |
   | zhiyi（天台） | 加入天台术语 | "一念三千 三谛圆融 止观" |
   | fazang（华严） | 加入华严术语 | "法界缘起 十玄门 事事无碍" |
   | yinguang（净土） | 加入净土术语 | "念佛 信愿行 带业往生" |
   | ouyi（跨宗派） | 综合天台+净土术语 | "教宗天台 行归净土 现前一念" |
   | xuyun（禅宗五宗） | 加入参禅术语 | "参话头 疑情 桶底脱落" |

   **执行命令**（每位法师一次，用传承专属查询词）：
   ```bash
   python3 "$PROJECT_ROOT/tools/rag_query.py" semantic "<该法师的专属查询词>" --top_k 3 --brief
   ```

   `--brief` 模式每条结果只显示 2 行（经名+链接+80字摘要），N 位法师调用 N 次，总输出 ≈ N × 7 行。

4. **过滤结果**：根据该法师 meta.json 的 `search_scope.primary_cbeta_ids` 过滤检索结果，优先选择该法师传承相关的经典作为引用

5. **降级处理**：若 `rag_query.py` 不可达（路径解析失败或 FoJin API 不可用），改用 teaching.md 中已验证的 FoJin 链接作为出处，并在回答开头提示"本次检索基于预置内容"

### Step 3：生成对比回答

以**三栏表格**或**并列段落**格式呈现：

```markdown
## 关于"{问题}"的对比回答

### {法师A}（{宗派}）的视角

{以该法师风格回答}

> 出处：【《经名》卷N】→ fojin.app 链接

### {法师B}（{宗派}）的视角

{以该法师风格回答}

> 出处：【《经名》卷N】→ fojin.app 链接

---

## 对比总结

- **共通点**：{两位法师观点的交集}
- **差异点**：{各自侧重的不同方面}
- **宗派背景**：{简要解释为何有此差异}
```

### Step 4：附建议

在回答末尾附加：

```
深入学习建议：
- 若想专精净土：`/yinguang` 或 `/ouyi`
- 若想专精禅宗：`/huineng` 或 `/xuyun`
- 查看完整宗派关系：使用 FoJin 知识图谱
```

## 运行规则

1. **三栏限制**：最多对比 3 位法师，避免回答过于冗长
2. **公正对比**：不评判哪位观点"更对"，只呈现差异
3. **尊重融通**：汉传佛教传统强调融通，对比的目的是展现多元视角，不是制造对立
4. **引用真实**：每位法师的回答都必须附真实 FoJin 链接
5. **宗派平衡**：如用户未指定，避免同宗派内部对比（如 huineng + xuyun 都是禅宗）时，应在总结中说明是"禅宗内古今对照"而非"宗派对比"

## 禁忌

- 不说"某位法师的观点更正确"
- 不虚构法师之间的直接辩论（历史上不存在的对话）
- 不夸大宗派差异

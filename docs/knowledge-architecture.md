# Research Lab 知识架构设计

> 源文档不可变，知识可进化。Sources 是原材料的静态仓库，Wiki 是 AI 消化后的动态知识图谱。

## 核心理念

Research Lab 是一个**可自我进化的研究知识管理系统**。它的目标是：

1. **收集** — 从各种来源（论文、博客、社交）抓取原始内容
2. **处理** — AI 逐步消化，从 raw → processed → sources → wiki
3. **关联** — 所有知识点通过 wikilinks 形成知识图谱
4. **进化** — AI 不断发现新关联，知识库持续增长

---

## 目录结构

```
research-lab/
│
├── src/                      # Python 模块
│   ├── source_manager.py     # Sources 存储逻辑 + frontmatter
│   ├── wiki_bridge.py       # LLM Wiki CLI 接口封装
│   └── crawler.py            # 爬虫整合
│
├── skills/                   # AI 操作指南（Markdown）
│   ├── browser-harness.md   # 怎么用 browser-harness 抓网页
│   ├── arxiv.md             # 怎么抓 arxiv 论文
│   ├── twitter.md           # 怎么抓 twitter
│   └── wiki-workflow.md     # 怎么用 LLM Wiki
│
├── raw/                      # 原始爬取（未处理）
├── processed/                # AI 第一次处理（清洗/结构化）
│
├── sources/                  # LLM Wiki sources/（不可变）
├── wiki/                     # LLM Wiki wiki/（可进化）
│
└── research_agent.py         # 主 Agent
```

---

## 数据流水线

```
raw/              爬虫抓取（原始数据）
    ↓
processed/        AI 第一次处理（清洗/结构化）
    ↓
sources/          存入 LLM Wiki sources/（不可变）
    ↓
wiki/             AI 消化后存入知识库（可进化）
```

---

## Sources 结构

### 分层组织：`type / hostname / date`

```
sources/
├── paper/              # 学术论文
│   ├── arxiv.org/
│   │   └── 2024-04-21/
│   │       └── 1706-03762.xml
│   └── openreview.net/
│       └── 2024-04-21/
│           └── paper-12345.json
│
├── blog/               # 博客文章
│   ├── neelnanda.io/
│   │   └── 2024-04-21/
│   │       └── blog-home.md
│   └── medium.com/
│
├── social/             # 社交内容
│   └── twitter.com/
│       └── 2024-04-21/
│           └── bookmarks.json
│
└── code/               # 代码（按需添加）
    └── github.com/
```

### Source Types

| 类型 | 来源示例 | 说明 |
|------|---------|------|
| `paper` | arxiv.org, openreview.net, pubmed.gov | 学术论文 |
| `blog` | neelnanda.io, medium.com | 博客文章 |
| `social` | twitter.com, reddit.com | 社交内容 |
| `code` | github.com | 代码仓库 |

**Self-evolving**: AI 遇到新来源时，自主判断是否创建新类型。

### Source Frontmatter

每个 source 文件包含不可变的元数据：

```yaml
---
source: https://arxiv.org/abs/1706.03762
type: paper
hostname: arxiv.org
crawled: 2024-04-21
---
```

**规则：**
- `source` — 原始 URL，永远不修改
- `type` — 来源类型（paper/blog/social/code）
- `hostname` — 来源域名
- `crawled` — 抓取日期

---

## Wiki 结构

### 存放 AI 消化后的知识

```
wiki/
├── attention-is-all-you-need.md
├── neel-nanda-blog-51.md
├── transformer-knowledge.md
└── ...
```

### Wiki Frontmatter

```yaml
---
title: Attention Is All You Need
source: [[sources/paper/arxiv.org/1706-03762]]
type: paper
tags: [transformer, nlp, attention-mechanism]
related_code: [[sources/code/github.com/tensorflow/models]]
related_papers: [[sources/paper/arxiv.org/1810-04805]]
mentioned_in: [[sources/blog/neelnanda.io/transformer-explained]]
created: 2024-04-21
updated: 2024-04-21
---
```

**规则：**
- `title` — 知识页面标题
- `source` — 来源（wikilink 指向 sources/）
- `tags` — 主题标签
- `related_*` — AI 发现的关联
- `updated` — 最后更新时间（AI 每次发现新关联更新）

---

## 知识关联

Sources 不是孤立的，是知识图谱的节点。

### 关联类型

| 关系 | 描述 |
|------|------|
| `related_code` | 论文的代码实现 |
| `related_papers` | 引用的其他论文 |
| `mentioned_in` | 被哪些博客/推文讨论 |
| `implements` | 实现了哪篇论文 |

### Wikilinks 语法

在 wiki 页面内容中使用：

```markdown
Transformer [[paper/arxiv.org/1706-03762]] 是 Google 的论文，
在 [[code/github.com/tensorflow/transformer]] 实现了它。
[[blog/neelnanda.io/transformer-explained]] 对此有详细解读。
```

---

## Skills（操作指南）

### 什么是 Skill

Skill 是告诉 AI **怎么操作**的 Markdown 文档。它不是知识，是"渔夫的工具"。

### Skill 示例结构

```markdown
# browser-harness

## 快速开始

```bash
browser-harness <<'PY'
goto("https://example.com")
screenshot()
PY
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `goto(url)` | 打开网页 |
| `click(selector)` | 点击元素 |
| `screenshot()` | 截图 |

## 注意事项

- ...
```

### Skills 列表

| Skill | 说明 |
|-------|------|
| `browser-harness.md` | 怎么用 browser-harness 抓网页 |
| `arxiv.md` | 怎么抓 arxiv 论文 |
| `twitter.md` | 怎么抓 twitter |
| `wiki-workflow.md` | 怎么用 LLM Wiki（ingest/query/lint）|

---

## LLM Wiki 工作流

### 完整研究流程

```
1. 用 skill 执行任务
   skills/browser-harness.md → 抓取网页
   ↓
2. 存到 raw/
   raw/neel-blog-2024-04-21.html
   ↓
3. AI 处理到 processed/
   processed/neel-blog-summary.md
   ↓
4. 存入 sources/（不可变）
   sources/blog/neelnanda.io/2024-04-21/blog-home.md
   ↓
5. AI 用 /ingest 消化到 wiki/
   wiki/neel-nanda-blog.md
   ↓
6. AI 发现关联，更新 wiki frontmatter
   related_papers: [[...]], related_code: [[...]]
   ↓
7. 知识图谱自动形成
```

### LLM Wiki 命令

| 命令 | 说明 |
|------|------|
| `llm-wiki ingest --path xxx` | 把 sources ingest 进 wiki |
| `llm-wiki query "transformer"` | 查询 wiki 知识 |
| `llm-wiki lint` | 健康检查 |
| `llm-wiki graph` | 查看知识图谱 |

---

## Self-Evolving 原则

### 1. Sources 不可变

- 原始材料只读不修改
- 保留抓取时的状态
- 可追溯来源

### 2. Wiki 可进化

- AI 随时更新 frontmatter
- 发现新关联随时添加 `related_*`
- `updated` 字段追踪变化

### 3. AI 自主判断

- 新来源类型：AI 自己判断放哪个 type
- 新关联：AI 自己发现并添加
- 新结构：AI 自己创建新页面

### 4. 知识 > 内容

- 不是存越多越好
- 重要的是关联关系
- wikilinks 是核心资产

---

## 技术栈

| 组件 | 工具 |
|------|------|
| 爬虫 | browser-harness, crawl4ai, firecrawl |
| 知识管理 | LLM Wiki (npm) |
| Agent | research_agent.py (LangChain) |
| Skills | Markdown 文档 |

---

## 下一步

1. 实现 `source_manager.py` — sources 存储逻辑
2. 实现 `wiki_bridge.py` — LLM Wiki CLI 封装
3. 编写核心 Skills 文档
4. 集成到 research_agent.py

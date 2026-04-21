# InfoGet

> 自动化研究情报收集与知识管理系统。收集 → 处理 → 整理 → 进化。

## 核心理念

InfoGet 是一个**可自我进化的研究知识管理系统**：

- **收集** — 从各种来源（论文、博客、社交）抓取原始内容
- **处理** — AI 逐步消化，从 raw → processed → sources → wiki
- **关联** — 所有知识点通过 wikilinks 形成知识图谱
- **进化** — AI 不断发现新关联，知识库持续增长

## 架构

```
raw/              爬虫抓取（原始数据）
    ↓
processed/        AI 第一次处理（清洗/结构化）
    ↓
sources/          LLM Wiki sources/（不可变）
    ↓
wiki/             LLM Wiki wiki/（可进化）
```

## Sources 结构

```
sources/
├── paper/              # 学术论文
│   ├── arxiv.org/
│   └── openreview.net/
├── blog/               # 博客文章
│   └── neelnanda.io/
├── social/             # 社交内容
│   └── twitter.com/
└── code/               # 代码
    └── github.com/
```

## Skills（操作指南）

| Skill | 说明 |
|-------|------|
| `browser-harness.md` | 怎么用 browser-harness 抓网页 |
| `arxiv.md` | 怎么抓 arxiv 论文 |
| `twitter.md` | 怎么抓 twitter |
| `wiki-workflow.md` | 怎么用 LLM Wiki |

## 技术栈

| 组件 | 工具 |
|------|------|
| 爬虫 | browser-harness, crawl4ai, firecrawl |
| 知识管理 | LLM Wiki |
| Agent | research_agent.py |

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export MINIMAX_API_KEY="your-key-here"

# 初始化 LLM Wiki vault
llm-wiki init

# 启动
python research_agent.py
```

详细设计见 [docs/knowledge-architecture.md](docs/knowledge-architecture.md)

# Wiki Workflow

LLM Wiki 工作流程：Sources → Wiki 知识。

## 初始化 Wiki

```python
from src import ensure_wiki_initialized

ensure_wiki_initialized()
```

## 完整工作流

```
1. 爬取内容 → sources/
   from src import crawl_and_save
   success, content, path = crawl_and_save("https://neelnanda.io/blog")

2. ingest 到 wiki
   from src import wiki_ingest
   wiki_ingest(path, title="Neel Nanda Blog", tags=["ai", "blog"])

3. 查询 wiki
   from src import wiki_query
   wiki_query("transformer")
```

## API

### wiki_ingest

```python
from src import wiki_ingest

success, msg = wiki_ingest(
    source_path="sources/blog/neelnanda.io/2024-04-21/blog-home.md",
    title="Neel Nanda Blog",
    tags=["ai-safety", "blog"],
    category="research"
)
```

### wiki_query

```python
from src import wiki_query

success, result = wiki_query(
    "transformer architecture",
    category="paper"
)
```

### wiki_add

```python
from src import wiki_add

wiki_add(
    title="My Notes on Transformer",
    content="## Summary\n\n...",
    tags=["transformer", "nlp"],
    category="notes"
)
```

### wiki_lint

```python
from src import wiki_lint

success, report = wiki_lint()
print(report)
```

### wiki_graph

```python
from src import wiki_graph

success, graph = wiki_graph()
```

## Wiki 结构

```
sources/              # 原始（不可变）
wiki/                # 知识（可进化）
```

## Wiki Page Frontmatter

```yaml
---
title: Page Title
source: [[sources/type/domain/date/file]]
tags: [tag1, tag2]
related_code: [[sources/code/github.com/xxx]]
related_papers: [[sources/paper/arxiv.org/xxx]]
created: 2024-04-21
updated: 2024-04-21
---
```

## Links

- LLM Wiki: https://github.com/jackwener/llm-wiki

# ArXiv 论文抓取

通过 arXiv API 搜索和获取论文元数据。

## CLI 调用（Agent 直接用）

```bash
# 搜索论文
curl -s "https://export.arxiv.org/api/query?search_query=ti:transformer+AND+cat:cs.LG&max_results=5&sortBy=submittedDate"

# 获取已知论文
curl -s "https://export.arxiv.org/api/query?id_list=1706.03762,1810.04805"

# 带过滤的搜索
curl -s "https://export.arxiv.org/api/query?search_query=au:vaswani&max_results=10&sortBy=relevance"
```

## API 参数

- `search_query`: `ti:title`, `au:name`, `abs:phrase`, `cat:cs.LG`
- `id_list`: 逗号分隔的 ID，如 `1706.03762,1810.04805`
- `max_results`: 最大返回数量（默认 10）
- `sortBy`: `relevance`, `lastUpdatedDate`, `submittedDate`

## 搜索示例

```bash
# Transformer 相关论文
curl -s "https://export.arxiv.org/api/query?search_query=ti:transformer&max_results=5&sortBy=submittedDate&sortOrder=descending"

# AI 安全相关
curl -s "https://export.arxiv.org/api/query?search_query=abs:AI+safety&max_results=10&sortBy=submittedDate&sortOrder=descending"
```

## 保存到 Sources

爬取后用 `save_to_sources` 工具保存，format 用 `xml`。

## 链接

- API: http://export.arxiv.org/api/query
- 搜索: https://arxiv.org

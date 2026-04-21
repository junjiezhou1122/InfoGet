# ArXiv

学术论文搜索和元数据获取。**永远不要用浏览器**，用 Atom API 即可。

## API 调用

```bash
# 搜索论文（按标题）
curl -s "https://export.arxiv.org/api/query?search_query=ti:transformer&max_results=5&sortBy=submittedDate"

# 搜索论文（按作者+分类）
curl -s "https://export.arxiv.org/api/query?search_query=au:vaswani+AND+cat:cs.LG&max_results=5&sortBy=submittedDate"

# 批量获取已知论文（逗号分隔，极快）
curl -s "https://export.arxiv.org/api/query?id_list=1706.03762,1810.04805&max_results=2"

# 带分页
curl -s "https://export.arxiv.org/api/query?search_query=cat:cs.AI&max_results=10&start=0&sortBy=lastUpdatedDate"
```

## API 参数

| 参数 | 说明 |
|------|------|
| `search_query` | `ti:标题`, `au:作者`, `abs:摘要`, `cat:分类` |
| `id_list` | 逗号分隔的 ID，如 `1706.03762,1810.04805` |
| `max_results` | 最大返回（默认 10，最大 2000）|
| `start` | 分页偏移 |
| `sortBy` | `relevance`, `lastUpdatedDate`, `submittedDate` |

## 搜索字段前缀

| 前缀 | 搜索范围 |
|------|---------|
| `ti:` | 标题 |
| `au:` | 作者 |
| `abs:` | 摘要 |
| `cat:` | 分类（如 `cs.LG`）|

## 分类代码

| 分类 | 领域 | 大约数量 |
|------|------|---------|
| `cs.LG` | Machine Learning | 261K |
| `cs.CL` | NLP | 106K |
| `cs.AI` | Artificial Intelligence | 172K |
| `cs.CV` | Computer Vision | 189K |

## 适合场景

- 学术论文元数据
- 批量获取论文信息
- 不用浏览器，只用 API

## 保存到 Sources

爬取后用 `save_to_sources` 工具保存，format 用 `xml`。

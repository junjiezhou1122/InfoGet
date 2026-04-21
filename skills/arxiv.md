# ArXiv + Semantic Scholar

学术论文搜索。**永远不要用浏览器**，用 API 即可。

## ArXiv API

```bash
# 搜索论文（按标题）
curl -s "https://export.arxiv.org/api/query?search_query=ti:transformer&max_results=5&sortBy=submittedDate"

# 按作者+分类
curl -s "https://export.arxiv.org/api/query?search_query=au:vaswani+AND+cat:cs.LG&max_results=5"

# 批量获取已知论文（逗号分隔，极快）
curl -s "https://export.arxiv.org/api/query?id_list=1706.03762,1810.04805&max_results=2"

# 带分页
curl -s "https://export.arxiv.org/api/query?search_query=cat:cs.AI&max_results=10&start=0&sortBy=lastUpdatedDate"
```

## Semantic Scholar API

```bash
# 搜索论文
curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=LLM+reasoning&limit=10&fields=title,authors,abstract,citationCount,influentialCitationCount"

# 按 ID 获取详情
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:1706.03762?fields=title,authors,abstract,citationCount,influentialCitationCount"
```

## API 参数

### ArXiv

| 参数 | 说明 |
|------|------|
| `search_query` | `ti:标题`, `au:作者`, `abs:摘要`, `cat:分类` |
| `id_list` | 逗号分隔的 ID |
| `max_results` | 最大返回（默认 10，最大 2000）|
| `sortBy` | `relevance`, `lastUpdatedDate`, `submittedDate` |

### Semantic Scholar

| 参数 | 说明 |
|------|------|
| `query` | 搜索词 |
| `limit` | 返回数量 |
| `fields` | `title,authors,abstract,citationCount,influentialCitationCount` |

## 顶会论文搜索（DBLP + S2）

基于 `evil-read-arxiv/conf-papers` 的工作流：

```bash
cd /Users/junjie/Desktop/reserach/info/evil-read-arxiv/conf-papers
python scripts/search_conf_papers.py \
  --config conf-papers.yaml \
  --output /tmp/conf_papers.json \
  --year 2024 \
  --conferences "ICLR,NeurIPS,CVPR"
```

支持的会议：CVPR, ICCV, ECCV, ICLR, AAAI, NeurIPS, ICML, ACL, EMNLP, MICCAI

## 分类代码

| 分类 | 领域 |
|------|------|
| `cs.LG` | Machine Learning |
| `cs.CL` | NLP |
| `cs.AI` | Artificial Intelligence |
| `cs.CV` | Computer Vision |

## 保存到 Sources

爬取后用 `save_to_sources` 工具保存。

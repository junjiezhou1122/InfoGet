# ArXiv 论文抓取

从 arXiv 抓取学术论文元数据和摘要。

## API 搜索

```python
from src import crawl_arxiv_paper

success, xml_content = crawl_arxiv_paper("1706.03762")
```

## 保存到 Sources

```python
from src import crawl_and_save, save_source

# 抓取并保存
success, content, path = crawl_and_save("https://arxiv.org/abs/1706.03762")

# 手动保存
from src import save_source
import xml.etree.ElementTree as ET

url = "https://arxiv.org/abs/1706.03762"
content = ...  # 抓取的内容
fm, path = save_source(content, url, format="xml", extra_frontmatter={
    "title": "Attention Is All You Need",
    "authors": ["Vaswani et al."],
})
```

## API 查询参数

- `search_query`: `ti:title`, `au:name`, `abs:phrase`, `cat:cs.LG`
- `id_list`: 逗号分隔的 ID，如 `1706.03762,1810.04805`
- `max_results`: 最大返回数量（默认 10）
- `sortBy`: `relevance`, `lastUpdatedDate`, `submittedDate`

## 示例查询

```python
# 搜索 Transformer 相关论文
url = "http://export.arxiv.org/api/query?search_query=ti:transformer+AND+cat:cs.LG&max_results=5&sortBy=submittedDate&sortOrder=descending"

# 批量获取已知论文
url = "http://export.arxiv.org/api/query?id_list=1706.03762,1810.04805&max_results=2"
```

## 链接

- API: http://export.arxiv.org/api/query
- 搜索: https://arxiv.org

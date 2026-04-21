# Firecrawl

云服务爬虫，支持整站爬取、JS 渲染、结构化输出。

## CLI 调用

```bash
# 安装
pip install firecrawl-py

# 爬取单个页面
firecrawl crawl https://example.com --format markdown

# 整站爬取
firecrawl scrape https://example.com --crawl

# 搜索
firecrawl search "AI news" --limit 5
```

## Python SDK

```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-...")

# 抓取页面
result = app.scrape_url("https://example.com", formats=["markdown"])

# 批量抓取
results = app.batch_scrape_urls(["url1", "url2"])
```

## 适合场景

- 整站爬取
- 需要 JS 渲染
- 结构化数据提取
- 云服务（无需本地 Chrome）

## 限制

- 需要 API Key
- 免费额度有限

## 保存到 Sources

爬取后用 `save_to_sources` 工具保存。

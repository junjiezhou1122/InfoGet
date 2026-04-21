# Firecrawl

云服务爬虫，支持整站爬取、JS 渲染、结构化输出。

## CLI 调用（curl 直接调 API）

Base URL: `https://api.firecrawl.dev/v1`
需要环境变量: `FIRECRAWL_TOKEN`

### Scrape - 单页面

```bash
# 基础 Markdown 抓取
curl -s -X POST "https://api.firecrawl.dev/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "formats": ["markdown"]}' | jq '.data.markdown'

# 纯文本（去掉 header/footer）
curl -s -X POST "https://api.firecrawl.dev/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "formats": ["markdown"], "onlyMainContent": true}'
```

### Crawl - 整站爬取

```bash
# 启动爬取
curl -s -X POST "https://api.firecrawl.dev/v1/crawl" \
  -H "Authorization: Bearer $FIRECRAWL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "limit": 50, "maxDepth": 2}'

# 轮询状态
curl -s "https://api.firecrawl.dev/v1/crawl/<job-id>" \
  -H "Authorization: Bearer $FIRECRAWL_TOKEN" | jq '{status, completed, total}'

# 取结果
curl -s "https://api.firecrawl.dev/v1/crawl/<job-id>" \
  -H "Authorization: Bearer $FIRECRAWL_TOKEN" | jq '.data[] | {url: .metadata.url}'
```

### Map - URL 发现

```bash
# 快速获取站点所有 URL
curl -s -X POST "https://api.firecrawl.dev/v1/map" \
  -H "Authorization: Bearer $FIRECRAWL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' | jq '.links[:20]'
```

### Search - 网页搜索

```bash
# 搜索并返回完整内容
curl -s -X POST "https://api.firecrawl.dev/v1/search" \
  -H "Authorization: Bearer $FIRECRAWL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "AI news", "limit": 5}' | jq '.data[] | {title: .metadata.title, url: .url}'
```

## 适合场景

- 整站爬取
- 需要 JS 渲染
- 结构化数据提取
- 云服务（无需本地 Chrome）

## 保存到 Sources

爬取后用 `save_to_sources` 工具保存。

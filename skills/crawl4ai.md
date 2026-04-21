# Crawl4ai

AI 友好的网页爬取工具，支持 JS 渲染和结构化输出。

## CLI 调用

```bash
cd /Users/junjie/Desktop/reserach/info/crawl4ai

# 基础爬取（返回 Markdown）
crwl https://example.com

# 输出 Markdown
crwl https://example.com -o markdown

# JSON 输出（绕过缓存）
crwl https://example.com -o json -v --bypass-cache

# 过滤后的 Markdown（去除噪音）
crwl https://example.com -o markdown-fit
```

## Python SDK

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler(verbose=False) as crawler:
        result = await crawler.arun("https://example.com")
        print(result.markdown[:500])

asyncio.run(main())
```

## 适合场景

- AI 任务用的网页爬取
- 需要 JS 渲染
- 结构化内容提取
- 批量爬取

## 与其他工具对比

| 特性 | crawl4ai | browser-harness | jina |
|------|----------|-----------------|------|
| JS 渲染 | ✅ | ✅ | ❌ |
| 输出格式 | Markdown/JSON | HTML/截图 | Markdown |
| 复杂度 | 中 | 高 | 低 |

## 保存到 Sources

爬取后用 `save_to_sources` 工具保存。

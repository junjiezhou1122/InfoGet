# Crawl4ai

AI 友好的网页爬取工具，支持 JS 渲染和结构化输出。

## CLI 调用

```bash
# 进入目录
cd /Users/junjie/Desktop/reserach/info/crawl4ai

# 爬取单个页面
python -m crawl4ai url "https://example.com"

# 输出 Markdown
python -m crawl4ai url "https://example.com" --format markdown
```

## Python 调用

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def crawl():
    async with AsyncWebCrawler(verbose=False) as crawler:
        result = await crawler.arun(url="https://example.com")
        if result.success:
            return result.markdown
        return result.error_message

print(asyncio.run(crawl()))
```

## 适合场景

- AI 任务用的网页爬取
- 需要 JS 渲染
- 结构化内容提取

## 与 browser-harness 对比

| 特性 | crawl4ai | browser-harness |
|------|----------|----------------|
| 定位 | AI 友好爬取 | 通用浏览器控制 |
| API | 高级封装 | 低级 CDP |
| 输出 | Markdown/结构化 | HTML/截图 |

## 保存到 Sources

爬取后用 `save_to_sources` 工具保存。

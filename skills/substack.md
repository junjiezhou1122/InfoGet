# Substack

通过 opencli 抓取 Substack newsletter。

## CLI 调用

```bash
# 搜索文章
opencli substack search "AI safety"

# 获取 Newsletter 最新文章
opencli substack publication <substack-url>

# 热门文章
opencli substack feed
```

## 适合场景

- 获取 newsletter 研究动态
- 追踪研究者发布的 newsletter
- 发现高质量长文分析

## 保存到 Sources

爬取后用 `save_to_sources` 工具保存：
- url: Substack 文章 URL
- source_type: `blog`
- format: `md` 或 `json`

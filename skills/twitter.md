# Twitter (X)

通过 opencli 抓取 Twitter 内容。

## CLI 调用

```bash
# 书签
opencli twitter bookmarks -f json --limit 10

# 用户推文
opencli twitter profile @username -f json --limit 10

# 搜索
opencli twitter search "AI safety" --limit 10
```

## 适合场景

- 抓取书签
- 抓取用户推文
- 搜索推文

## 保存到 Sources

爬取后用 `save_to_sources` 工具保存：
- url: `https://twitter.com/bookmarks` 或 `https://twitter.com/username`
- source_type: `social`
- format: `json`

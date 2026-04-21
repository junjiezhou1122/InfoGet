# Twitter 抓取

通过 opencli 抓取 Twitter 内容。

## 抓取书签

```python
from src import crawl_twitter_opencli, crawl_twitter_and_save

# 抓取并返回 JSON
success, content = crawl_twitter_opencli("bookmarks --limit 10 -f json")

# 抓取并保存到 sources/
success, content, path = crawl_twitter_and_save("bookmarks --limit 10", tag="bookmarks")
```

## 抓取用户推文

```python
success, content = crawl_twitter_opencli("profile username --limit 10 -f json")

# 保存
success, content, path = crawl_twitter_and_save("profile neelnanda --limit 10", tag="neelnanda-tweets")
```

## opencli 命令

```bash
# 书签
opencli twitter bookmarks -f json --limit 10

# 用户推文
opencli twitter profile username -f json --limit 10

# 搜索
opencli twitter search "AI safety" --limit 10
```

## 保存到 Sources

```python
from src import save_source
import json

content = ...  # 推文 JSON
url = "https://twitter.com/bookmarks"
fm, path = save_source(
    content,
    url,
    source_type="social",
    format="json",
    extra_frontmatter={"tag": "bookmarks"}
)
```

## 链接

- opencli: https://github.com/jackwener/opencli

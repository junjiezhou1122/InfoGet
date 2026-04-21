# Twitter 抓取

通过 opencli 抓取 Twitter 内容。

## CLI 调用（Agent 直接用）

```bash
# 书签
opencli twitter bookmarks -f json --limit 10

# 用户推文
opencli twitter profile @username -f json --limit 10

# 搜索
opencli twitter search "AI safety" --limit 10
```

## 抓取后保存

爬取内容后用 `save_to_sources` 工具保存：

```python
# url: https://twitter.com/bookmarks 或 https://twitter.com/username
# content: 抓取的 JSON
# source_type: social
# extra: {"tag": "bookmarks"}
```

## 保存到 Sources（手动）

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

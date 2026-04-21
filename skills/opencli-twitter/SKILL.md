---
name: opencli-twitter
description: Twitter/X 数据获取。触发：Twitter书签、时间线、搜索用户、发帖、点赞、热门话题。
---

# OpenCLI Twitter Skill

## 命令列表

| 命令 | 参数 | 说明 |
|------|------|------|
| `timeline` | `--limit N` (默认20) | 首页时间线 |
| `trending` | `--limit N` (默认20) | 热门话题 |
| `search` | `--query <str>` (必须), `--limit N` | 搜索推文 |
| `bookmarks` | `--limit N` (默认20) | 书签列表 |
| `notifications` | `--limit N` (默认20) | 通知 |
| `profile` | `--username <handle>` (必须), `--limit N` | 指定用户推文 |
| `followers` | `--user <handle>`, `--limit N` | 粉丝列表 |
| `following` | `--user <handle>`, `--limit N` | 关注列表 |
| `post` | `--text <str>` (必须) | 发推 |
| `reply` | `--url <tweet_url>` (必须), `--text <str>` (必须) | 回复推文 |
| `like` | `--url <tweet_url>` (必须) | 点赞 |
| `delete` | `--url <tweet_url>` (必须) | 删除推文 |

## 示例命令

```bash
# 获取书签
opencli twitter bookmarks -f json --limit 40

# 获取用户时间线
opencli twitter profile --username jack --limit 10 -f json

# 搜索推文
opencli twitter search --query "AI agent" --limit 20 -f json

# 查看热门话题
opencli twitter trending --limit 10 -f json

# 发推（谨慎操作）
opencli twitter post --text "Hello from opencli"

# 点赞
opencli twitter like --url "https://x.com/user/status/123"
```

## 输出格式

返回 JSON 格式，包含：
- `id`: 推文 ID
- `author`: 作者
- `text`: 内容
- `created_at`: 发布时间
- `url`: 链接
- `metrics`: 点赞/转发/回复数

## 触发场景

- "看看我的 Twitter 书签"
- "搜索关于 LLM 的推文"
- "某用户的最新推文"
- "Twitter 热门话题是什么"
- "帮我点赞这条推文"

## 注意

- 所有写操作 (post, reply, like, delete) 需要明确用户确认
- 读操作 (timeline, bookmarks, search) 无需确认
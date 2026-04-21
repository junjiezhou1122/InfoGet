# YouTube

通过 opencli 抓取 YouTube 内容。

## CLI 调用

```bash
# 搜索视频
opencli youtube search "transformer tutorial"

# 获取视频信息
opencli youtube video <video-url>

# 获取频道信息
opencli youtube channel <channel-id>

# 获取字幕/转录
opencli youtube transcript <video-url>

# 获取视频评论
opencli youtube comments <video-url>

# 获取播放列表
opencli youtube playlist <playlist-id>
```

## 主要命令

| 命令 | 说明 |
|------|------|
| `search <query>` | 搜索视频 |
| `video <url>` | 视频元数据 |
| `channel <id>` | 频道信息和最新视频 |
| `transcript <url>` | 字幕/转录 |
| `comments <url>` | 视频评论 |
| `playlist <id>` | 播放列表 |

## 适合场景

- 论文解读视频
- 研究演讲（Talent talk）
- 技术教程
- 追踪研究者频道

## 保存到 Sources

爬取后用 `save_to_sources` 工具保存。

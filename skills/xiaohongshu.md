# 小红书 (Xiaohongshu)

通过 opencli 抓取小红书内容。

## CLI 调用

```bash
# 搜索笔记
opencli xiaohongshu search "AI教程"

# 获取笔记详情
opencli xiaohongshu note <note-id>

# 获取用户笔记列表
opencli xiaohongshu user <user-id>

# 获取创作者信息
opencli xiaohongshu creator-profile

# 获取创作者笔记列表
opencli xiaohongshu creator-notes

# 获取创作者数据总览
opencli xiaohongshu creator-stats

# 获取笔记评论
opencli xiaohongshu comments <note-id>

# 下载笔记图片/视频
opencli xiaohongshu download <note-id>

# 搜索
opencli xiaohongshu search "护肤教程"
```

## 主要命令

| 命令 | 说明 |
|------|------|
| `note <note-id>` | 笔记正文和互动数据 |
| `user <id>` | 用户公开笔记 |
| `search <query>` | 搜索笔记 |
| `creator-profile` | 创作者账号信息 |
| `creator-notes` | 创作者笔记列表 |
| `creator-stats` | 创作者数据总览 |
| `comments <note-id>` | 笔记评论 |
| `download <note-id>` | 下载图片/视频 |

## 保存到 Sources

爬取后用 `save_to_sources` 工具保存：
- url: 小红书笔记 URL
- source_type: `social`
- format: `json`

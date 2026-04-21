# OpenCLI

通用网站 CLI 工具，把任何网站变成命令行接口。

## 基础命令

```bash
# 查看所有可用命令
opencli list

# 探索网站，发现 API 和策略
opencli explore <url>

# 浏览器控制（无需 LLM）
opencli browser

# 诊断连接
opencli doctor
```

## 已安装的平台

| 平台 | 命令前缀 | 说明 |
|------|---------|------|
| Twitter/X | `opencli twitter` | 推文、书签、用户 |
| 小红书 | `opencli xiaohongshu` | 笔记、用户 |
| Reddit | `opencli reddit` | 帖子、搜索 |
| GitHub | `opencli gh` | PR、issues、repos |
| Bilibili | `opencli bilibili` | 视频、用户 |
| 知乎 | `opencli zhihu` | 问答、文章 |
| arXiv | `opencli arxiv` | 论文搜索 |
| Medium | `opencli medium` | 文章 |
| 微信公众号 | `opencli weixin` | 文章 |

**完整列表**：`opencli list`

## Twitter/X

```bash
opencli twitter bookmarks -f json --limit 10
opencli twitter profile @username -f json --limit 10
opencli twitter search "AI" --limit 10
```

## 小红书

```bash
opencli xiaohongshu user <user-id>
```

## 通用网站探索

```bash
# 探索网站结构，发现可用的 CLI 策略
opencli explore https://example.com

# 一键生成并注册 CLI
opencli generate <url>

# 录制浏览器操作生成 YAML
opencli record <url>
```

## 安装更多平台

```bash
# 安装扩展
opencli install <name>

# 查看可安装的
opencli install --help
```

---
name: opencli
description: 通用 CLI 工具，访问社交/内容/金融平台。触发：查看B站热门、知乎热搜、微博、Twitter动态、股票行情、Reddit等。
---

# OpenCLI - 通用数据获取 CLI

重用 Chrome 登录态，无需额外凭证即可访问多个平台。

## 发现可用命令

**重要**: 当不确定 opencli 支持哪些命令时，先执行：

```bash
opencli -h                    # 列出所有命令
opencli <platform> -h         # 查看特定平台的子命令
```

例如：`opencli bilibili -h` 会显示 bilibili 的所有可用命令。

## 语法

```bash
opencli <platform> <command> [args] [-f json|table|yaml|md|csv]
```

## 支持的平台（常用）

| 平台 | 用途 | 示例命令 |
|------|------|---------|
| twitter | 社交媒体 | `opencli twitter bookmarks -f json --limit 20` |
| bilibili | B站视频 | `opencli bilibili hot -f json` |
| zhihu | 知乎 | `opencli zhihu hot -f json` |
| reddit | 社区 | `opencli reddit hot -f json` |
| youtube | 视频搜索 | `opencli youtube search --query "AI" --limit 10 -f json` |
| v2ex | 技术社区 | `opencli v2ex hot -f json` |
| weibo | 微博 | `opencli weibo hot -f json` |
| xiaohongshu | 小红书 | `opencli xiaohongshu feed -f json` |
| xueqiu | 股票 | `opencli xueqiu hot -f json` |
| yahoo-finance | 股票行情 | `opencli yahoo-finance quote --symbol AAPL -f json` |
| hackernews | 技术新闻 | `opencli hackernews top --limit 20 -f json` |
| bbc | 新闻 | `opencli bbc news -f json` |
| arxiv | 论文 | `opencli arxiv search --query "AI" --limit 5 -f json` |

## 通用参数

- `-f json` — 机器可读输出（推荐）
- `--limit N` — 结果数量
- `-v` — verbose/debug 模式

## 工具

### run_opencli

执行 opencli 命令并返回结果。

```python
run_opencli(command: str) -> str
# 示例: run_opencli("opencli twitter bookmarks -f json --limit 20")
```

## 发现新平台

如果需要使用未列出的平台，先运行：
```bash
opencli -h
```
找到对应 platform 后，再用 `opencli <platform> -h` 查看其子命令。

## 了解更多

需要特定平台的详细用法时，加载对应 skill：
- `opencli-twitter` — Twitter 完整命令
- `opencli-bilibili` — B站完整命令
- `opencli-finance` — 股票/雪球完整命令
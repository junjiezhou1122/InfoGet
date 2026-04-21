# Jina Reader

将任意网页转成 Markdown，纯 HTTP，无需浏览器。

## CLI 调用

```bash
# 基础用法
curl -s https://r.jina.ai/{url}

# 指定输出格式
curl -s https://r.jina.ai/{url} -H "Accept: text/markdown"

# 带标题
curl -s https://r.jina.ai/{url} -H "X-Return-Format: markdown"
```

## 适合场景

- 快速获取网页正文
- 不需要 JS 渲染的静态页面
- 轻量级爬取

## 示例

```bash
# 抓博客文章
curl -s https://neelnanda.io/blog

# 抓新闻
curl -s https://news.ycombinator.com/item?id=123
```

## 限制

- 不支持 JS 渲染
- 不支持需要登录的页面
- 复杂页面可能提取不完整

## 保存到 Sources

爬取后用 `save_to_sources` 工具保存。

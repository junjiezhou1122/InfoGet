# Jina Reader

将任意网页转成 Markdown，纯 HTTP，无需浏览器。

## CLI 调用

```bash
# 最常用：直接转 Markdown
curl -s https://r.jina.ai/https://example.com

# 带 Header
curl -s https://r.jina.ai/https://example.com \
  -H "Accept: text/markdown" \
  -H "X-Return-Format: markdown"

# 仅获取文本（去除 HTML）
curl -s https://r.jina.ai/https://example.com \
  -H "Accept: text/plain"
```

## Python 调用

```python
import urllib.request

url = "https://r.jina.ai/" + urllib.request.quote("https://example.com")
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=20) as r:
    print(r.read().decode())
```

## 适合场景

- 快速获取网页正文
- 不需要 JS 渲染的静态页面
- 轻量级爬取

## 限制

- 不支持 JS 渲染
- 不支持需要登录的页面
- 复杂页面可能提取不完整

## 保存到 Sources

爬取后用 `save_to_sources` 工具保存。

# Browser Harness

用 CDP 直接控制 Chrome 浏览器的极简工具。

## 快速开始

```bash
browser-harness <<'PY'
goto("https://example.com")
wait_for_load()
screenshot()
PY
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `goto(url)` | 打开网页 |
| `new_tab(url)` | 新标签页打开 |
| `click(selector)` | 点击元素 |
| `type_text(text)` | 输入文字 |
| `screenshot()` | 截图 |
| `wait(seconds)` | 等待 |
| `wait_for_load()` | 等待页面加载 |
| `js("...")` | 执行 JavaScript |
| `http_get(url)` | 纯 HTTP 请求（不需要浏览器）|

## 适合场景

- 需要登录的网站
- JS 渲染的页面
- 需要交互的操作（点击、填表）

## 不适合场景

- 纯内容抓取 → 用 firecrawl 或 jina.ai
- 静态页面 → 直接用 http_get

## 保存到 Sources

```python
from src import crawl_and_save

success, content, path = crawl_and_save("https://neelnanda.io/blog")
```

## 链接

- GitHub: https://github.com/browser-use/browser-harness

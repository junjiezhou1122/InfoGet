# Browser Harness

用 CDP 直接控制 Chrome 浏览器的极简工具。

## CLI 调用（Agent 直接用）

```bash
# 进入项目目录
cd /Users/junjie/Desktop/reserach/info/browser-harness

# 基本用法
uv run browser-harness <<'PY'
goto("https://example.com")
wait_for_load()
screenshot()
PY

# 获取 HTML / Markdown
uv run browser-harness <<'PY'
goto("https://neelnanda.io/blog")
wait_for_load()
html = html()
print(html)
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
| `html()` | 获取页面 HTML |
| `http_get(url)` | 纯 HTTP 请求（不需要浏览器）|

## 适合场景

- 需要登录的网站
- JS 渲染的页面
- 需要交互的操作（点击、填表）

## 快速抓取博客/文章

```bash
uv run browser-harness <<'PY'
goto("https://neelnanda.io/blog")
wait_for_load()
links = elements("a")
for l in links:
    print(l.attr("href"))
PY
```

## 保存到 Sources

爬取后手动调工具保存：

```python
# 先爬取内容，存到变量里，然后调 save_to_sources 工具
```

## 链接

- GitHub: https://github.com/browser-use/browser-harness

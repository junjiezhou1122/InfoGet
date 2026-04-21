# Searxng

开源元搜索引擎，聚合多个搜索结果，保护隐私。

## CLI / Docker 部署

```bash
# Docker 启动
docker run -d -p 8888:8080 --name searxng searxng/searxng

# 或用项目中已部署
cd /Users/junjie/Desktop/reserach/info/searxng
docker-compose up
```

## API 调用

```bash
# 搜索
curl -s "http://localhost:8888/search?q=AI+safety&format=json&engines=google"

# 带参数
curl -s "http://localhost:8888/search?q={query}&format=json&engines=arxiv,wikipedia"
```

## Python 调用

```python
import requests

result = requests.get("http://localhost:8888/search", params={
    "q": "AI safety",
    "format": "json",
    "engines": "google,arxiv"
}).json()

for r in result["results"][:5]:
    print(r["title"], r["url"])
```

## 适合场景

- 聚合多引擎搜索结果
- 隐私保护（不跟踪）
- 快速信息检索

## 限制

- 需要本地部署或使用公共实例
- 部分网站可能被屏蔽

## 保存到 Sources

搜索结果可保存到 processed/ 作为参考资料。

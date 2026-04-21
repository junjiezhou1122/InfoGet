# GitHub

通过 `opencli gh` 或 GitHub API 访问。

## CLI 调用

```bash
# 搜索仓库
opencli gh search repos "LLM reasoning"

# 获取仓库信息
opencli gh repo <owner>/<repo>

# 查看 issues
opencli gh issue list <owner>/<repo> --state open --limit 10

# 查看 PR
opencli gh pr list <owner>/<repo> --state open

# 克隆仓库
gh repo clone <owner>/<repo>
```

## GitHub API

```bash
# 搜索仓库
curl -s "https://api.github.com/search/repositories?q=transformer+language:python&sort=stars&order=desc" | jq '.items[:5]'

# 获取仓库
curl -s "https://api.github.com/repos/<owner>/<repo>" | jq '{name, description, stars: .stargazers_count}'

# 获取 commits
curl -s "https://api.github.com/repos/<owner>/<repo>/commits?per_page=5" | jq '.[].commit.message'
```

## 适合场景

- 找论文对应的代码实现
- 研究开源项目
- 查看 release notes

## 保存到 Sources

爬取后用 `save_to_sources` 工具保存。

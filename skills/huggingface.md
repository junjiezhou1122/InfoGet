# HuggingFace

通过 `hf` CLI 或 opencli 访问。

## 安装

```bash
curl -LsSf https://hf.co/cli/install.sh | bash
```

## 模型搜索

```bash
# 搜索模型
hf models list --search "transformer" --limit 5

# 模型详情
hf models info meta-llama/Llama-2-7b

# 按任务筛选
hf models list --filter "text-generation" --sort downloads --limit 5
```

## 数据集搜索

```bash
# 搜索数据集
hf datasets list --search "squad" --limit 5

# 数据集详情
hf datasets info stanfordnlp/squad

# SQL 查询数据集
hf datasets sql "SELECT * FROM 'csv' WHERE text LIKE '%AI%' LIMIT 10"
```

## Papers

```bash
# 搜索论文
hf papers search "reasoning"

# 读取论文
hf papers read <paper-id>

# 每日论文
hf papers list --date 2024-01-01 --limit 10
```

## Spaces

```bash
# 搜索 Spaces
hf spaces list --search "chatbot" --limit 5

# Space 详情
hf spaces info <space-id>
```

## opencli 方式

```bash
opencli hf models info <model-id>
opencli hf datasets info <dataset-id>
```

## 适合场景

- 找论文对应的模型实现
- 发现相关数据集
- 追踪最新模型
- 部署推理端点

## 保存到 Sources

爬取后用 `save_to_sources` 工具保存。

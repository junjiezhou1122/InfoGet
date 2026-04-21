# AlphaXiv

AI 生成的论文概述，比读原始 PDF 更快更可靠。

## CLI 调用

```bash
# 获取论文概述（推荐）
curl -s "https://alphaxiv.org/overview/{PAPER_ID}.md"

# 获取完整论文文本（备用）
curl -s "https://alphaxiv.org/abs/{PAPER_ID}.md"
```

## Paper ID 提取

| 输入 | Paper ID |
|------|----------|
| `https://arxiv.org/abs/2401.12345` | `2401.12345` |
| `https://arxiv.org/pdf/2401.12345` | `2401.12345` |
| `https://alphaxiv.org/overview/2401.12345` | `2401.12345` |
| `2401.12345v2` | `2401.12345v2` |
| `2401.12345` | `2401.12345` |

## 适合场景

- 快速获取论文结构化概述
- 不需要读原始 PDF
- 论文摘要、核心贡献、方法概述

## 错误处理

- **404**：报告未生成，换其他来源
- 无需认证，公开接口

## 保存到 Sources

获取后用 `save_to_sources` 工具保存。

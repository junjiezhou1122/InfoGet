# Conf Papers - 顶会论文搜索推荐

搜索 CVPR/ICCV/ECCV/ICLR/AAAI/NeurIPS/ICML 等顶级会议论文，基于 DBLP + Semantic Scholar 双数据源。

## 工作流程

```
1. DBLP API → 获取会议论文列表
2. 标题关键词 → 轻量筛选
3. Semantic Scholar → 补充引用数和摘要
4. 三维评分 → 相关性 40% + 热门度 40% + 质量 20%
5. 输出推荐笔记
```

## CLI 调用

```bash
cd /Users/junjie/Desktop/reserach/info/evil-read-arxiv/conf-papers

# 搜索指定年份和会议
python scripts/search_conf_papers.py \
  --config conf-papers.yaml \
  --output /tmp/conf_papers.json \
  --year 2024 \
  --conferences "ICLR,NeurIPS,CVPR"

# 查看结果
cat /tmp/conf_papers.json
```

## 支持的会议

| 会议 | 说明 |
|------|------|
| CVPR | Computer Vision |
| ICCV | Computer Vision (偶数年) |
| ECCV | Computer Vision (奇数年) |
| ICLR | Deep Learning |
| AAAI | AI |
| NeurIPS | ML |
| ICML | ML |
| ACL | NLP |
| EMNLP | NLP |
| MICCAI | Medical Image |

## 配置文件

`conf-papers.yaml` 中配置关键词：

```yaml
keywords:
  - "large language model"
  - "LLM"
excluded_keywords:
  - "3D"
  - "survey"
default_year: 2024
default_conferences:
  - "ICLR"
  - "NeurIPS"
top_n: 10
```

## 输出格式

每篇论文包含：
- title, authors, conference, year
- dblp_url, arxiv_id
- abstract, citationCount, influentialCitationCount
- scores（relevance, popularity, quality, recommendation）

## 前 3 篇特殊处理

对于评分最高的前 3 篇论文：
- 有 arXiv ID → 提取图片 + 生成详细分析
- 无 arXiv ID → 标注"无 arXiv 版本"

## 保存到 Sources

爬取后用 `save_to_sources` 工具保存。

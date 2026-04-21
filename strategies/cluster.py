from .base import BaseStrategy

class ClusterStrategy(BaseStrategy):
    def run(self, data_list, name: str):
        print(f"[*] [Strategy: Cluster] 正在聚类分析 {len(data_list)} 条记录: {name}")
        texts = [f"内容: {t.get('text', t.get('content_markdown', ''))}" for t in data_list]
        context = "\n---\n".join(texts)
        system = "你擅长对碎片化信息进行架构化梳理，找出共同的技术趋势。"
        prompt = f"请分析以下这组信息的共同技术趋势和关联：\n\n{context}"
        result = self.client.ask(system, prompt)
        self.save(name, result, "CLUSTER_ANALYSIS")
        return result

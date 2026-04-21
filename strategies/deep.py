from .base import BaseStrategy

class DeepStrategy(BaseStrategy):
    def run(self, data, name: str):
        print(f"[*] [Strategy: Deep] 正在深度拆解长文: {name}")
        content = data.get("content_markdown", data.get("text", ""))
        system = "你是一个顶级 AI 研究员，擅长从长文中提取硬核技术指标和行业趋势。"
        prompt = f"请对以下内容进行深度解析：\n\n{content[:12000]}"
        result = self.client.ask(system, prompt)
        self.save(name, result, "DEEP_REPORT")
        return result

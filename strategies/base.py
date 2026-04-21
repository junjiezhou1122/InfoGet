from abc import ABC, abstractmethod
from datetime import date
from pathlib import Path

class BaseStrategy(ABC):
    def __init__(self, client):
        self.client = client

    @abstractmethod
    def run(self, data, name: str) -> str:
        pass

    def save(self, name: str, content: str, mode: str):
        if not content: return
        output_path = Path(f"research-lab/data/processed/{name}_{mode}.md")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"---\nstrategy: {mode}\ndate: {date.today().isoformat()}\n---\n\n{content}")
        print(f"[+] 策略 [{mode}] 执行成功，报告存至: {output_path}")

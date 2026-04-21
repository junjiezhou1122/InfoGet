import json
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")
from core.client import AIClient
from strategies.deep import DeepStrategy
from strategies.cluster import ClusterStrategy
from tools.twitter import TwitterTool

# --- 配置区 ---
API_KEY = os.environ.get("MINIMAX_API_KEY", "")
OPENCLI_PATH = Path(os.environ.get(
    "OPENCLI_PATH",
    "/Users/junjie/.nvm/versions/node/v24.14.0/lib/node_modules/@jackwener/opencli"
))

class ResearchMission:
    def __init__(self):
        self.client = AIClient(api_key=API_KEY)
        self.twitter = TwitterTool()
        
        # 初始化策略库
        self.strategies = {
            "deep": DeepStrategy(self.client),
            "cluster": ClusterStrategy(self.client)
        }

    def start_bookmarks_mission(self, limit: int = 10):
        """一键启动：抓取收藏并分析"""
        # 1. 抓取
        data = self.twitter.fetch_bookmarks(limit)
        if not data: return

        # 2. 存盘原始数据
        raw_file = Path("research-lab/data/raw/latest_mission_bookmarks.json")
        raw_file.parent.mkdir(parents=True, exist_ok=True)
        with open(raw_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

        # 3. 自动路由策略 (多条记录自动选 Cluster)
        self.strategies["cluster"].run(data, "latest_bookmarks")

    def run_on_local_files(self):
        """自动处理 data/raw 下的所有本地文件"""
        raw_dir = Path("research-lab/data/raw")
        for file in raw_dir.glob("*.json"):
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # 路由逻辑
            if isinstance(data, list):
                self.strategies["cluster"].run(data, file.stem)
            elif len(data.get("content_markdown", "")) > 2000:
                self.strategies["deep"].run(data, file.stem)

if __name__ == "__main__":
    if not API_KEY:
        print("[-] 错误：未设置 MINIMAX_API_KEY 环境变量")
        print("    export MINIMAX_API_KEY='your-key-here'")
        exit(1)
    mission = ResearchMission()
    print("🚀 启动自动化科研系统...")
    mission.start_bookmarks_mission(limit=5)
    # mission.run_on_local_files()

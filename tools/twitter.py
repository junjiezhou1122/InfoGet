import subprocess
import json
from pathlib import Path

OPENCLI_PATH = Path("/Users/junjie/.nvm/versions/node/v24.14.0/lib/node_modules/@jackwener/opencli")

class TwitterTool:
    def __init__(self, opencli_path: Path = None):
        self.opencli_path = opencli_path or OPENCLI_PATH

    def fetch_bookmarks(self, limit: int = 10):
        print(f"[*] [Tool: Twitter] 正在抓取书签 (limit={limit})...")
        cmd = ["opencli", "twitter", "bookmarks", "-f", "json", "--limit", str(limit)]
        try:
            result = subprocess.run(cmd, cwd=self.opencli_path, capture_output=True, text=True)
            if result.returncode == 0:
                return json.loads(result.stdout)
            return None
        except Exception as e:
            print(f"[-] Twitter Tool Error: {e}")
            return None

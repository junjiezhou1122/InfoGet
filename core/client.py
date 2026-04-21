import os
import requests

MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
MINIMAX_BASE_URL = os.environ.get("MINIMAX_BASE_URL", "https://api.minimax.chat/v1")

class AIClient:
    def __init__(self, api_key: str = None, model: str = "MiniMax-M2.7"):
        self.api_key = api_key or MINIMAX_API_KEY
        self.model = model
        self.url = f"{MINIMAX_BASE_URL}/chat/completions"
        self.timeout = 300

    def ask(self, system_prompt: str, user_prompt: str):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
        try:
            response = requests.post(self.url, headers=headers, json=payload, timeout=self.timeout)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"[-] AI Client Error: {e}")
            return None

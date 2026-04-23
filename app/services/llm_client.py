import requests
import time
from app.core.config import config


# =========================
# CORE LLM CALL (CLEAN)
# =========================
def call_llm(prompt: str, n_predict: int = 100, retries: int = 2, api_url=None, api_key=None):

    url = api_url or config.LLAMA_API_URL
    key = api_key or config.API_KEY

    payload = {
        "prompt": prompt,  # 🔥 لا تغلفه
        "n_predict": n_predict,
        "temperature": 0.2,
        "stop": [
            "User:",
            "Assistant:",
            "```"
        ]
    }

    headers = {
        "x-api-key": key,
        "Content-Type": "application/json"
    }

    last_error = None

    for attempt in range(retries + 1):
        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=10
            )

            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

            # 🔥 نرجع RAW كما هو
            try:
                return response.json()
            except Exception:
                return response.text.strip()

        except Exception as e:
            last_error = str(e)
            time.sleep(0.5 * (attempt + 1))

    return f"LLM timeout | error: {last_error}"
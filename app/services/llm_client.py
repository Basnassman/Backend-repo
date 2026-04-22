import requests
import time
from app.core.config import config


# =========================
# SAFE RESPONSE PARSER
# =========================
def _parse_response(data):
    if not isinstance(data, dict):
        return None

    return (
        data.get("reply")
        or data.get("response")
        or data.get("content")
        or data.get("text")
    )


# =========================
# CORE LLM CALL
# =========================
def call_llm(prompt: str, n_predict: int = 100, retries: int = 2, api_url=None, api_key=None):

    url = api_url or config.LLAMA_API_URL
    key = api_key or config.API_KEY

    payload = {
        "prompt": prompt,
        "n_predict": n_predict,
        "temperature": 0.3,
        "stop": [
            "USER:",
            "ASSISTANT:",
            "<SYSTEM>",
            "</SYSTEM>"
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

            try:
                data = response.json()
            except Exception:
                return {
                    "reply": response.text.strip() or "Invalid response format"
                }

            raw = _parse_response(data)

            return {
                "reply": (raw or "").strip()
            }

        except Exception as e:
            last_error = str(e)
            time.sleep(0.5 * (attempt + 1))

    return {
    "reply": f"LLM timeout - check server | error: {last_error}"
}
    
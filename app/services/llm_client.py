import requests
import time
from core.config import config


# =========================
# SAFE RESPONSE PARSER
# =========================
def _parse_response(data):
    if not isinstance(data, dict):
        return str(data)

    return (
        data.get("reply")
        or data.get("response")
        or data.get("content")
        or str(data)
    )


# =========================
# CORE LLM CALL
# =========================
def call_llm(prompt: str, n_predict: int = 100, retries: int = 2):
    """
    Production-grade LLM client with:
    - retry mechanism
    - safe parsing
    - HTTP validation
    - fallback handling
    """

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
        "x-api-key": config.API_KEY,
        "Content-Type": "application/json"
    }

    last_error = None

    for attempt in range(retries + 1):
        try:
            response = requests.post(
                config.LLAMA_API_URL,
                json=payload,
                headers=headers,
                timeout=30
            )

            # =========================
            # HTTP VALIDATION
            # =========================
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

            # =========================
            # SAFE JSON PARSING
            # =========================
            try:
                data = response.json()
            except Exception:
                return {
                    "reply": response.text.strip() or "Invalid response format"
                }

            return {
                "reply": _parse_response(data).strip()
            }

        except Exception as e:
            last_error = str(e)
            time.sleep(0.5 * (attempt + 1))

    # =========================
    # FINAL FAILSAFE
    # =========================
    return {
        "reply": f"Service unavailable. Last error: {last_error}"
    }
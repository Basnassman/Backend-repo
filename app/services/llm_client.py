import requests
from app.core.config import LLAMA_API_URL, API_KEY


def call_llm(prompt: str, n_predict: int):

    try:
        response = requests.post(
            LLAMA_API_URL,
            json={
                "prompt": prompt,
                "n_predict": n_predict,
                "temperature": 0.3,
                "stop": ["USER:", "ASSISTANT:"]
            },
            headers={
                "x-api-key": API_KEY
            },
            timeout=30
        )

        data = response.json()

        return {
            "reply": (
                data.get("reply")
                or data.get("response")
                or data.get("content")
                or str(data)
            )
        }

    except Exception as e:
        return {"reply": f"LLM ERROR: {str(e)}"}
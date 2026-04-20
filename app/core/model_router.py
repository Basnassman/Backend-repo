from app.core.config import LLAMA_API_URL, API_KEY
from app.services.llm_client import call_llm


def call_model(prompt: str, n_predict: int):

    # مستقبلًا يمكن إضافة GPT / Claude routing هنا
    return call_llm(prompt, n_predict)
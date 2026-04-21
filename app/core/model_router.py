from app.core.config import config
from app.services.llm_client import call_llm


# =========================
# 1. MODEL REGISTRY
# =========================
MODELS = {
    "llama": {
        "enabled": True,
        "max_tokens": config.MAX_N_PREDICT,
    }
}


# =========================
# 2. ROUTING
# =========================
def _select_model(prompt: str) -> str:
    p = prompt.lower()

    if any(k in p for k in ["code", "python", "flutter", "bug", "error"]):
        return "llama"

    return "llama"


# =========================
# 3. VALIDATION
# =========================
def _validate_request(model: str, n_predict: int):
    model_cfg = MODELS.get(model)

    if not model_cfg:
        raise ValueError(f"Model {model} not found")

    return min(n_predict, model_cfg["max_tokens"])


# =========================
# 4. MAIN CALL
# =========================
def call_model(prompt: str, n_predict: int = 100):
    print("[CALL MODEL] START")

    model = _select_model(prompt)
    n_predict = _validate_request(model, n_predict)

    if model == "llama":
        response = call_llm(
            prompt=prompt,
            n_predict=n_predict,
            api_url=config.LLAMA_API_URL,
            api_key=config.API_KEY
        )

        print("[CALL MODEL] RESPONSE:", response)
        return response

    return call_llm(
        prompt=prompt,
        n_predict=n_predict,
        api_url=config.LLAMA_API_URL,
        api_key=config.API_KEY
    )
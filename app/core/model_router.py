from core.config import LLAMA_API_URL
from services.llm_client import call_llm


# =========================
# 1. MODEL REGISTRY
# =========================
MODELS = {
    "llama": {
        "enabled": True,
        "max_tokens": 1000,
    }
}


# =========================
# 2. SIMPLE ROUTING LOGIC
# =========================
def _select_model(prompt: str) -> str:
    """
    Lightweight routing logic (can be expanded later)
    """

    p = prompt.lower()

    # Code-heavy requests → future expansion
    if any(k in p for k in ["code", "python", "flutter", "bug", "error"]):
        return "llama"

    # Default model
    return "llama"


# =========================
# 3. PRE-FLIGHT CHECK
# =========================
def _validate_request(model: str, n_predict: int):
    config = MODELS.get(model)

    if not config:
        raise ValueError(f"Model {model} not found")

    # enforce limits (like production systems)
    if n_predict > config["max_tokens"]:
        n_predict = config["max_tokens"]

    return n_predict


# =========================
# 4. MAIN ROUTER (PUBLIC API)
# =========================
def call_model(prompt: str, n_predict: int = 100):
    """
    Production-style model gateway
    """

    # 1. select model
    model = _select_model(prompt)

    # 2. validate request
    n_predict = _validate_request(model, n_predict)

    # 3. route to LLM client
    if model == "llama":
        return call_llm(prompt, n_predict)

    # fallback (future models)
    return call_llm(prompt, n_predict)
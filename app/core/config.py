import os
from dataclasses import dataclass


# =========================
# ENV LOADER HELPERS
# =========================
def _get_env(key: str, default: str = None, required: bool = False):
    value = os.getenv(key, default)

    if required and not value:
        raise EnvironmentError(f"Missing required environment variable: {key}")

    return value


# =========================
# CONFIG CLASS
# =========================
@dataclass(frozen=True)
class Config:

    # -------- LLM SETTINGS --------
    LLAMA_API_URL: str = _get_env(
        "LLAMA_API_URL",
        "http://127.0.0.1:8080/completion"  # ✅ الرابط الصحيح
    )

    API_KEY: str = _get_env(
        "API_KEY",
        "712825736aA$"  # ⚠️ fallback (لكن الأفضل من Render env)
    )

    # -------- APP SETTINGS --------
    APP_ENV: str = _get_env("APP_ENV", "development")
    DEBUG: bool = _get_env("DEBUG", "true").lower() == "true"

    # -------- MEMORY SETTINGS --------
    MAX_MEMORY_MESSAGES: int = int(_get_env("MAX_MEMORY_MESSAGES", "10"))

    # -------- MODEL SETTINGS --------
    DEFAULT_N_PREDICT: int = int(_get_env("DEFAULT_N_PREDICT", "100"))
    MAX_N_PREDICT: int = int(_get_env("MAX_N_PREDICT", "1000"))

    # -------- SECURITY SETTINGS --------
    ENABLE_PROMPT_GUARD: bool = True
    ENABLE_RESPONSE_SANITIZER: bool = True


# =========================
# SINGLETON
# =========================
config = Config()
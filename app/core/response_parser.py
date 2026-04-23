import json
import re
from typing import Optional, Dict, Any


# =========================
# SAFE JSON EXTRACTION
# =========================
def _extract_json_block(text: str) -> Optional[str]:
    """
    Extract first valid JSON block safely (non-greedy + balanced fallback)
    """
    if not text:
        return None

    # 🔥 try non-greedy first
    match = re.search(r'\{.*?\}', text, re.DOTALL)
    if match:
        return match.group()

    return None


# =========================
# SAFE JSON PARSE
# =========================
def _safe_json_load(text: str) -> Optional[Dict[str, Any]]:
    if not text:
        return None

    try:
        return json.loads(text)
    except:
        return None


# =========================
# TOOL VALIDATION
# =========================
ALLOWED_TOOLS = {"chat_reply"}


def _validate_tool(data: Dict[str, Any]) -> Optional[str]:
    """
    Validate tool structure and return reply safely
    """
    if not isinstance(data, dict):
        return None

    tool = data.get("tool")
    args = data.get("args")

    if tool not in ALLOWED_TOOLS:
        return None

    if not isinstance(args, dict):
        return None

    reply = args.get("reply")

    if not isinstance(reply, str):
        return None

    return reply.strip()


# =========================
# MAIN PARSER (CLEAN + SAFE)
# =========================
def parse_tool_response(raw: str) -> Optional[str]:
    """
    RAW LLM OUTPUT → TOOL RESPONSE → CLEAN REPLY
    """

    if not raw:
        return None

    # -------------------------
    # 1. direct JSON attempt
    # -------------------------
    data = _safe_json_load(raw)

    # -------------------------
    # 2. fallback: extract JSON
    # -------------------------
    if not data:
        json_block = _extract_json_block(raw)
        if json_block:
            data = _safe_json_load(json_block)

    # -------------------------
    # 3. validate tool format
    # -------------------------
    if data:
        return _validate_tool(data)

    # -------------------------
    # 4. final fallback (last resort)
    # -------------------------
    return None
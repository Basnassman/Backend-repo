import json
import re
from typing import Optional, Dict, Any


# =========================
# ALLOWED TOOLS
# =========================
ALLOWED_TOOLS = {"chat_reply"}


# =========================
# SAFE JSON EXTRACTION (IMPROVED)
# =========================
def _extract_json_block(text: str) -> Optional[str]:
    """
    Extract first valid JSON block with balanced braces support
    """
    if not text:
        return None

    # محاولة 1: non-greedy بسيط
    match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
    if match:
        candidate = match.group()
        try:
            json.loads(candidate)
            return candidate
        except:
            pass  # مو متوازن، نكمل
    
    # محاولة 2: balanced braces (لـ nested JSON)
    start = text.find('{')
    if start == -1:
        return None
    
    depth = 0
    for i, char in enumerate(text[start:], start):
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                candidate = text[start:i+1]
                try:
                    json.loads(candidate)
                    return candidate
                except:
                    return None
    return None


# =========================
# DEEP JSON SEARCH (NEW!)
# =========================
def _deep_extract_reply(text: str) -> Optional[str]:
    """
    يبحث بعمق في النص عن أي tool_call صالح
    """
    if not text:
        return None
    
    # البحث عن كل كتل JSON الممكنة
    # نمط: {"tool": "...", "args": {"reply": "..."}}
    pattern = r'\{\s*"tool"\s*:\s*"([^"]+)"\s*,\s*"args"\s*:\s*\{\s*"reply"\s*:\s*"((?:[^"\\]|\\.)*)"\s*\}\s*\}'
    matches = re.findall(pattern, text, re.DOTALL)
    
    for tool_name, reply in matches:
        if tool_name in ALLOWED_TOOLS and reply:
            return reply.encode('utf-8').decode('unicode_escape').strip()
    
    # fallback: بحث بسيط عن "reply"
    simple_pattern = r'"reply"\s*:\s*"((?:[^"\\]|\\.)*)"'
    matches = re.findall(simple_pattern, text, re.DOTALL)
    if matches:
        return matches[-1].encode('utf-8').decode('unicode_escape').strip()
    
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
def _validate_tool(data: Dict[str, Any]) -> Optional[str]:
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
# CLEAN RAW TEXT (NEW!)
# =========================
def _clean_raw_text(text: str) -> str:
    """
    ينظف النص من prefixes ويستخرج المحتوى المفيد
    """
    if not text:
        return ""
    
    # إزالة "Assistant:" و "User:" المتكررة
    lines = text.split('\n')
    clean_lines = []
    
    for line in lines:
        line = line.strip()
        if line.startswith("Assistant:"):
            line = line[len("Assistant:"):].strip()
        if line.startswith("User:"):
            continue
        if line and line not in ['{', '}', '},']:
            clean_lines.append(line)
    
    return '\n'.join(clean_lines)


# =========================
# MAIN PARSER (FIXED!)
# =========================
def parse_tool_response(raw) -> Optional[str]:
    """
    RAW LLM OUTPUT → CLEAN REPLY
    يقبل: str أو dict
    """

    if raw is None:
        return None

    # ====== تحويل dict إلى str ======
    if isinstance(raw, dict):
        # إذا كان dict فيه "reply" ناخذ قيمته
        if "reply" in raw and isinstance(raw["reply"], str):
            raw = raw["reply"]
        else:
            # حاول نحول dict كامل لـ JSON string
            try:
                raw = json.dumps(raw, ensure_ascii=False)
            except:
                return None
    
    if not isinstance(raw, str):
        return None

    raw = raw.strip()
    if not raw:
        return None

    # -------------------------
    # 1. البحث العميق عن tool_call
    # -------------------------
    deep_reply = _deep_extract_reply(raw)
    if deep_reply:
        return deep_reply

    # -------------------------
    # 2. direct JSON attempt
    # -------------------------
    data = _safe_json_load(raw)
    
    # -------------------------
    # 3. extract JSON block
    # -------------------------
    if not data:
        json_block = _extract_json_block(raw)
        if json_block:
            data = _safe_json_load(json_block)

    # -------------------------
    # 4. validate tool format
    # -------------------------
    if data:
        validated = _validate_tool(data)
        if validated:
            return validated

    # -------------------------
    # 5. تنظيف النص الخام (fallback)
    # -------------------------
    cleaned = _clean_raw_text(raw)
    if cleaned and len(cleaned) > 2:  # أكثر من حرفين
        return cleaned

    # -------------------------
    # 6. final fallback
    # -------------------------
    return None

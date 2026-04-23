import json
import re
from typing import Optional, Dict, Any


ALLOWED_TOOLS = {"chat_reply"}


def _fix_encoding(text: str) -> str:
    """يصلح مشاكل UTF-8/Latin-1"""
    if not text:
        return text
    try:
        fixed = text.encode('latin-1').decode('utf-8')
        # تأكد إن التصليح نجح
        if 'Ù' not in fixed and 'Ø' not in fixed:
            return fixed
    except:
        pass
    return text


def _extract_json_block(text: str) -> Optional[str]:
    if not text:
        return None

    match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
    if match:
        candidate = match.group()
        try:
            json.loads(candidate)
            return candidate
        except:
            pass
    
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


def _deep_extract_reply(text: str) -> Optional[str]:
    if not text:
        return None
    
    pattern = r'\{\s*"tool"\s*:\s*"chat_reply"\s*,\s*"args"\s*:\s*\{\s*"reply"\s*:\s*"((?:[^"\\]|\\.)*)"\s*\}\s*\}'
    matches = re.findall(pattern, text, re.DOTALL)
    
    for tool_name, reply in matches:
        if reply:
            cleaned = reply.encode('utf-8').decode('unicode_escape')
            return _fix_encoding(cleaned).strip()
    
    simple_pattern = r'"reply"\s*:\s*"((?:[^"\\]|\\.)*)"'
    matches = re.findall(simple_pattern, text, re.DOTALL)
    if matches:
        cleaned = matches[-1].encode('utf-8').decode('unicode_escape')
        return _fix_encoding(cleaned).strip()
    
    return None


def _safe_json_load(text: str) -> Optional[Dict[str, Any]]:
    if not text:
        return None
    try:
        return json.loads(text)
    except:
        return None


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

    return _fix_encoding(reply).strip()


def _clean_raw_text(text: str) -> str:
    if not text:
        return ""
    
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


def parse_tool_response(raw) -> Optional[str]:
    if raw is None:
        return None

    if isinstance(raw, dict):
        if "reply" in raw and isinstance(raw["reply"], str):
            deep = _deep_extract_reply(raw["reply"])
            if deep:
                return deep
            return _fix_encoding(raw["reply"]).strip()
        try:
            raw = json.dumps(raw, ensure_ascii=False)
        except:
            return None
    
    if not isinstance(raw, str):
        return None

    raw = raw.strip()
    if not raw:
        return None

    # إصلاح encoding أولاً
    raw = _fix_encoding(raw)

    deep_reply = _deep_extract_reply(raw)
    if deep_reply:
        return deep_reply

    data = _safe_json_load(raw)
    
    if not data:
        json_block = _extract_json_block(raw)
        if json_block:
            data = _safe_json_load(json_block)

    if data:
        validated = _validate_tool(data)
        if validated:
            return validated

    cleaned = _clean_raw_text(raw)
    if cleaned and len(cleaned) > 2:
        return cleaned

    return None

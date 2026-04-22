import re

def clean_text(text):
    if not text:
        return None

    text = re.sub(r"</?SYSTEM>", "", text)
    text = re.sub(r"</?OUTPUT>", "", text)

    return text.strip()
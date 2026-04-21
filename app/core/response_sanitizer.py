import re

def clean_output(text: str):
    if not text:
        return ""

    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"</?OUTPUT>", "", text)

    return text.strip()
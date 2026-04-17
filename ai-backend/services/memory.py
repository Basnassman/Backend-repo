# services/memory.py

# ذاكرة مؤقتة (لكل مستخدم لاحقًا)
chat_history = []

def add_message(role: str, content: str):
    chat_history.append({
        "role": role,
        "content": content
    })

    # نحافظ على آخر 5 رسائل فقط
    if len(chat_history) > 5:
        chat_history.pop(0)


def get_history():
    return chat_history


def clear_history():
    chat_history.clear()
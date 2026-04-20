from collections import defaultdict

chat_history = defaultdict(list)

def add_message(user_id: str, role: str, content: str):
    chat_history[user_id].append({
        "role": role,
        "content": content
    })

    # keep last 10 messages per user
    if len(chat_history[user_id]) > 10:
        chat_history[user_id] = chat_history[user_id][-10:]


def get_history(user_id: str):
    return chat_history[user_id]


def clear_history(user_id: str):
    chat_history[user_id] = []
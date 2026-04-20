from collections import defaultdict

# memory per user (temporary in RAM)
memory_store = defaultdict(list)


def add_message(user_id: str, role: str, content: str):
    memory_store[user_id].append({
        "role": role,
        "content": content
    })

    # keep last 10 messages only
    if len(memory_store[user_id]) > 10:
        memory_store[user_id] = memory_store[user_id][-10:]


def get_history(user_id: str):
    return memory_store[user_id]


def clear_memory(user_id: str):
    memory_store[user_id] = []
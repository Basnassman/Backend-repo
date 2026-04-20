from core.prompt_engine import build_prompt
from core.model_router import call_model
from services.memory_service import add_message, get_history


def handle_chat(req):

    user_id = req.user_id
    message = req.message

    add_message(user_id, "user", message)

    history = get_history(user_id)

    prompt = build_prompt(message, history)

    response = call_model(prompt, req.n_predict)

    reply = response.get("reply", str(response))

    add_message(user_id, "assistant", reply)

    return {
        "reply": reply
    }
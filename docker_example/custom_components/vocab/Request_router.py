from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema.message import Message
import re

def _to_text(x) -> str:
    if x is None:
        return ""
    if isinstance(x, str):
        return x
    for attr in ("text", "content"):
        if hasattr(x, attr):
            v = getattr(x, attr)
            if isinstance(v, str):
                return v
    if isinstance(x, dict):
        for k in ("text", "content"):
            v = x.get(k)
            if isinstance(v, str):
                return v
    return str(x)


def _is_add_intent(text: str) -> bool:
    t = (text or "").strip().lower()

    # Fast path: contains "add" + "word" anywhere (handles "please add the english word")
    if "add" in t and "word" in t:
        return True

    # Also accept "insert" / "save" / "store" + "word"
    if any(v in t for v in ("insert", "save", "store")) and "word" in t:
        return True

    # Also accept formats like: "add: fever" or "add fever"
    if re.search(r"\badd\b\s*[:\-]?\s*[a-zäöüß]+", t):
        return True

    return False


class RequestRouter(Component):
    display_name = "Request Router"
    description = "Routes requests: add-word goes directly to agent, otherwise uses story prompt."
    icon = "shuffle"
    name = "RequestRouter"

    inputs = [
        MessageTextInput(name="user_request", display_name="User Request"),
        MessageTextInput(name="story_prompt", display_name="Story Prompt"),
    ]

    outputs = [
        Output(display_name="Agent Input", name="output", method="route"),
    ]

    def route(self) -> Message:
        user_text = _to_text(getattr(self, "user_request", ""))
        story_text = _to_text(getattr(self, "story_prompt", ""))

        if _is_add_intent(user_text):
            # send the original request so the agent calls AddWordTool and stops
            return Message(text=user_text, sender="Human")

        # default: story mode
        return Message(text=story_text, sender="Human")

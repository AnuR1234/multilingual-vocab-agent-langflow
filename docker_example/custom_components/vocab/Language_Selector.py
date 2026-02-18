from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema.message import Message


def _to_text(x) -> str:
    if x is None:
        return ""
    if isinstance(x, str):
        return x
    # langflow Message or langchain messages often have .text or .content
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


def _detect_lang_code(raw) -> str:
    t = _to_text(raw).strip().lower()
    if "german" in t or "deutsch" in t or "auf deutsch" in t or "in deutsch" in t:
        return "de"
    if "english" in t or "englisch" in t or "in english" in t:
        return "en"
    return "en"


class LanguageSelector(Component):
    display_name = "Language Selector"
    description = "Infers language code (en/de) from the user's request."
    icon = "languages"
    name = "LanguageSelector"

    inputs = [
        MessageTextInput(
            name="request",
            display_name="User Request",
            info="User message text, e.g. 'write a story in German'",
        )
    ]

    outputs = [
        Output(display_name="Language", name="output", method="build_language"),
    ]

    def build_language(self) -> Message:
        lang = _detect_lang_code(getattr(self, "request", None))
        return Message(text=lang, sender="AI")

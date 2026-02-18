# import os
# import psycopg2

# from langflow.custom import Component
# from langflow.io import Output
# from langflow.schema import Data


# def _db_url() -> str:
#     return os.getenv(
#         "LANGFLOW_DATABASE_URL",
#         "postgresql://langflow:langflow@postgres:5432/langflow",
#     )


# def load_words() -> list[str]:
#     conn = psycopg2.connect(_db_url())
#     try:
#         cur = conn.cursor()
#         cur.execute("SELECT word FROM tutor.words ORDER BY word;")
#         rows = cur.fetchall()
#         return [r[0] for r in rows]
#     finally:
#         conn.close()


# class WordLoader(Component):
#     display_name = "Word Loader"
#     description = "Loads all words from Postgres (schema: tutor.words) and outputs a comma-separated string."
#     icon = "database"
#     name = "WordLoader"

#     outputs = [
#         Output(display_name="Words", name="output", method="build_output"),
#     ]

#     def build_output(self) -> Data:
#         words = load_words()
#         return Data(value=", ".join(words))

import os
import psycopg2

from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema.message import Message


def _db_url() -> str:
    return os.getenv(
        "LANGFLOW_DATABASE_URL",
        "postgresql://langflow:langflow@postgres:5432/langflow",
    )


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


def _detect_lang_code(raw) -> str:
    t = _to_text(raw).strip().lower()
    if "german" in t or "deutsch" in t or "auf deutsch" in t or "in deutsch" in t:
        return "de"
    if "english" in t or "englisch" in t or "in english" in t:
        return "en"
    return "en"


def _load_words(lang: str) -> list[str]:
    conn = psycopg2.connect(_db_url())
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT word FROM tutor.words WHERE language = %s ORDER BY word;",
            (lang,),
        )
        return [r[0] for r in cur.fetchall()]
    finally:
        conn.close()


class WordLoader(Component):
    display_name = "Word Loader"
    description = "Loads words from Postgres based on language inferred from the user request."
    icon = "database"
    name = "WordLoader"

    inputs = [
        MessageTextInput(
            name="request",
            display_name="User Request",
            info="User message. Language inferred (en/de).",
        )
    ]

    outputs = [
        Output(display_name="Words", name="words", method="build_words"),
        Output(display_name="Language", name="language", method="build_language"),
    ]

    def build_language(self) -> Message:
        lang = _detect_lang_code(getattr(self, "request", None))
        return Message(text=lang, sender="AI")

    def build_words(self) -> Message:
        lang = _detect_lang_code(getattr(self, "request", None))
        words = _load_words(lang)
        return Message(text=", ".join(words), sender="AI")

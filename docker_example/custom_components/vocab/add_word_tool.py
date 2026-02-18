# import os
# import psycopg2

# from langflow.custom import Component
# from langflow.io import MessageTextInput, Output,StrInput
# from langflow.schema import Data


# def _db_url() -> str:
#     return os.getenv(
#         "LANGFLOW_DATABASE_URL",
#         "postgresql://langflow:langflow@postgres:5432/langflow",
#     )


# def _get_conn():
#     conn = psycopg2.connect(_db_url())
#     conn.autocommit = True
#     return conn


# # def _ensure_schema_and_table(cur):
# #     cur.execute("CREATE SCHEMA IF NOT EXISTS tutor;")
# #     cur.execute(
# #         """
# #         CREATE TABLE IF NOT EXISTS tutor.words (
# #             word TEXT PRIMARY KEY
# #         );
# #         """
# #     )


# # def _normalize(word: str) -> str:
# #     return (word or "").strip().lower()


# # class AddWordTool(Component):
# #     display_name = "Add Word Tool"
# #     description = "Adds ONE word into Postgres (schema: tutor.words). Use only when user explicitly asks to add a word."
# #     icon = "database"
# #     name = "AddWordTool"

# #     inputs = [
# #         MessageTextInput(
# #             name="new_word",
# #             display_name="New Word",
# #             info="The single word to add",
# #             tool_mode=True,
# #         ),
# #     ]

# #     outputs = [
# #         Output(display_name="Result", name="output", method="add_new_word"),
# #     ]

# #     def add_new_word(self) -> Data:
# #         conn = None
# #         try:
# #             w = _normalize(self.new_word)
# #             if not w:
# #                 return Data(value="No word provided.")

# #             conn = _get_conn()
# #             cur = conn.cursor()
# #             _ensure_schema_and_table(cur)

# #             cur.execute(
# #                 "INSERT INTO tutor.words (word) VALUES (%s) ON CONFLICT (word) DO NOTHING;",
# #                 (w,),
# #             )
# #             return Data(value=f"Added word: {w}")
# #         except Exception as e:
# #             return Data(value=f"Error: {type(e).__name__}: {str(e)}")
# #         finally:
# #             if conn is not None:
# #                 conn.close()


# def _ensure_schema_and_tables(cur):
#     cur.execute("CREATE SCHEMA IF NOT EXISTS tutor;")
#     cur.execute(
#        """
# CREATE TABLE IF NOT EXISTS tutor.words (
# language TEXT NOT NULL,
# word TEXT NOT NULL,
# PRIMARY KEY (language,word)

# );
# """
#     )

# def _normalize_word(word:str)-> str:

#     return (word or '').strip().casefold()

# def _normalize_lang(lang:str)-> str:
#     return(lang or '').strip().lower()

# class AddWordTool(Component):
        
#         display_name = "Add Word Tool"
#         description = "Adds ONE word into Postgres (schema: tutor.words). Use only when user explicitly asks to add a word."
#         icon = "database"
#         name = "AddWordTool"

#         inputs = [
             
#             StrInput(
#                  name='language',
#                  display_name='Language',
#                 info="Language code for the word. Example: en or de",
#                 tool_mode=True,
#         ),
#             MessageTextInput(
#                 name="new_word",
#                 display_name="New Word",
#                 info="The single word to add",
#                 tool_mode=True,

#     ),
# ]
#         output = [Output(display_name='Result',name='output',method ='add_new_word')
#         ]

#         def add_new_word(self)-> Data:
             
#             conn= None
#             try:
#                   lang = _normalize_lang(getattr(self,"language",""))
#                   w = _normalize_word(getattr(self,"new_word",""))

#                   if not lang:
#                        return Data(value="Error: No language provided.Use something like 'en' or 'de'")
#                   if not w:
#                        return Data(value="Error: No word provided")
                  
#                   conn = _get_conn()
#                   cur = conn.cursor()
#                   _ensure_schema_and_tables(cur)

#                   cur.execute(
#                         """
#                         INSERT INTO tutor.words (language, word)
#                         VALUES (%s, %s)
#                         ON CONFLICT (language, word) DO NOTHING;
#                         """,
#                         (lang, w),
#                     )
                  
#                   return Data(value=f" Added word:{w} (language={lang})")
#             except Exception as e:
#                     return Data(value=f"Error: {type(e).__name__}: {str(e)}")
#             finally:
#                 if conn is not None:
#                     conn.close()

import os
import psycopg2

from langflow.custom import Component
from langflow.io import MessageTextInput, StrInput, Output
from langflow.schema import Data


def _db_url() -> str:
    return os.getenv(
        "LANGFLOW_DATABASE_URL",
        "postgresql://langflow:langflow@postgres:5432/langflow",
    )


def _get_conn():
    conn = psycopg2.connect(_db_url())
    conn.autocommit = True
    return conn


def _ensure_schema_and_table(cur):
    cur.execute("CREATE SCHEMA IF NOT EXISTS tutor;")
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tutor.words (
            language TEXT NOT NULL,
            word TEXT NOT NULL,
            PRIMARY KEY (language, word)
        );
        """
    )
    cur.execute("CREATE INDEX IF NOT EXISTS idx_tutor_words_language ON tutor.words(language);")


def _normalize_word(word: str) -> str:
    return (word or "").strip().lower()


def _normalize_lang(lang: str) -> str:
    lang = (lang or "").strip().lower()
    # accept "german"/"english" too
    if lang in ("de", "deutsch", "german", "ger"):
        return "de"
    if lang in ("en", "english", "englisch"):
        return "en"
    return lang  # allow future languages like "fr"


class AddWordTool(Component):
    display_name = "Add Word Tool"
    description = "Adds ONE word into Postgres (schema: tutor.words) with a language code."
    icon = "database"
    name = "AddWordTool"

    inputs = [
        StrInput(
            name="language",
            display_name="Language",
            info="Language code like 'de' or 'en'.",
            tool_mode=True,
        ),
        MessageTextInput(
            name="new_word",
            display_name="New Word",
            info="The single word to add",
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(display_name="Result", name="output", method="add_new_word"),
    ]

    def add_new_word(self) -> Data:
        conn = None
        try:
            lang = _normalize_lang(getattr(self, "language", ""))
            word = _normalize_word(getattr(self, "new_word", ""))

            if not lang:
                return Data(value="Error: language is empty. Use 'de' or 'en'.")
            if not word:
                return Data(value="Error: no word provided.")

            conn = _get_conn()
            cur = conn.cursor()
            _ensure_schema_and_table(cur)

            cur.execute(
                """
                INSERT INTO tutor.words (language, word)
                VALUES (%s, %s)
                ON CONFLICT (language, word) DO NOTHING;
                """,
                (lang, word),
            )
            return Data(value=f"Added word '{word}' to language '{lang}'.")
        except Exception as e:
            return Data(value=f"Error: {type(e).__name__}: {str(e)}")
        finally:
            if conn is not None:
                conn.close()
   
                  






# import os
# import csv
# import psycopg2

# from langflow.custom import Component
# from langflow.io import StrInput, FileInput, Output
# from langflow.schema import Data


# def _db_url() -> str:
#     # Use Langflow's DB connection string by default
#     return os.getenv(
#         "LANGFLOW_DATABASE_URL",
#         "postgresql://langflow:langflow@postgres:5432/langflow",
#     )


# def _get_conn():
#     conn = psycopg2.connect(_db_url())
#     conn.autocommit = True
#     return conn


# def _ensure_schema_and_table(cur):
#     # Make sure schema exists, then table
#     cur.execute("CREATE SCHEMA IF NOT EXISTS tutor;")
#     cur.execute(
#         """
#         CREATE TABLE IF NOT EXISTS tutor.words (
#             word TEXT PRIMARY KEY
#         );
#         """
#     )


# def _normalize(word: str) -> str:
#     return (word or "").strip().lower()


# def _add_word(cur, word: str) -> bool:
#     w = _normalize(word)
#     if not w:
#         return False
#     cur.execute(
#         "INSERT INTO tutor.words (word) VALUES (%s) ON CONFLICT (word) DO NOTHING;",
#         (w,),
#     )
#     return True


# class UploadWordFile(Component):
#     display_name = "Upload Word File"
#     description = "Upload a CSV file of words into Postgres (schema: tutor.words)."
#     icon = "database"
#     name = "UploadWordFile"

#     inputs = [
#         StrInput(
#             name="column_name",
#             display_name="Column Name",
#             info="Name of the CSV column that contains the words (case-insensitive). Example: word",
#         ),
#         FileInput(
#             name="csv_file",
#             display_name="CSV file",
#             info="Upload a .csv file",
#             file_types=["csv"],
#         ),
#     ]

#     outputs = [
#         Output(display_name="Status", name="output", method="load_words_into_database"),
#     ]

#     def load_words_into_database(self) -> Data:
#         conn = None
#         try:
#             column = (self.column_name or "").strip().lower()
#             if not column:
#                 return Data(value="Error: Column Name is empty.")

#             # Langflow FileInput usually provides a local file path inside the container
#             path = getattr(self, "csv_file", None)
#             if not path:
#                 return Data(value="Error: No CSV file provided.")

#             conn = _get_conn()
#             cur = conn.cursor()
#             _ensure_schema_and_table(cur)

#             inserted = 0
#             total = 0

#             with open(path, "r", encoding="utf-8") as f:
#                 reader = csv.DictReader(f)
#                 headers = [h.strip().lower() for h in (reader.fieldnames or [])]
#                 if column not in headers:
#                     return Data(value=f"Error: Column '{column}' not found. CSV columns: {headers}")

#                 for row in reader:
#                     total += 1
#                     if _add_word(cur, row.get(column, "")):
#                         inserted += 1

#             return Data(value=f"Success: processed {total} rows. Inserted {inserted} words into tutor.words.")
#         except Exception as e:
#             return Data(value=f"Error: {type(e).__name__}: {str(e)}")
#         finally:
#             if conn is not None:
#                 conn.close()

import os
import csv
import psycopg2

from langflow.custom import Component
from langflow.io import StrInput, FileInput, Output
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


def _normalize_word(word: str) -> str:
    return (word or "").strip().casefold()


def _normalize_lang(lang: str) -> str:
    return (lang or "").strip().lower()


def _add_word(cur, lang: str, word: str) -> bool:
    l = _normalize_lang(lang)
    w = _normalize_word(word)
    if not l or not w:
        return False

    cur.execute(
        """
        INSERT INTO tutor.words (language, word)
        VALUES (%s, %s)
        ON CONFLICT (language, word) DO NOTHING;
        """,
        (l, w),
    )
    return True


class UploadWordFile(Component):
    display_name = "Upload Word File"
    description = "Upload a CSV file of words into Postgres (schema: tutor.words)."
    icon = "database"
    name = "UploadWordFile"

    inputs = [
        StrInput(
            name="language",
            display_name="Language",
            info="Language code for these words. Example: en or de",
        ),
        StrInput(
            name="column_name",
            display_name="Column Name",
            info="Name of the CSV column that contains the words (case-insensitive). Example: word",
        ),
        FileInput(
            name="csv_file",
            display_name="CSV file",
            info="Upload a .csv file",
            file_types=["csv"],
        ),
    ]

    outputs = [
        Output(display_name="Status", name="output", method="load_words_into_database"),
    ]

    def load_words_into_database(self) -> Data:
        conn = None
        try:
            lang = _normalize_lang(getattr(self, "language", ""))
            if not lang:
                return Data(value="Error: Language is empty. Use something like 'en' or 'de'.")

            requested_col = (getattr(self, "column_name", "") or "").strip().lower()
            if not requested_col:
                return Data(value="Error: Column Name is empty.")

            path = getattr(self, "csv_file", None)
            if not path:
                return Data(value="Error: No CSV file provided.")

            conn = _get_conn()
            cur = conn.cursor()
            _ensure_schema_and_table(cur)

            inserted_attempts = 0
            total = 0

            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                raw_headers = reader.fieldnames or []
                header_map = {(h or "").strip().lower(): h for h in raw_headers}

                if requested_col not in header_map:
                    available = sorted([k for k in header_map.keys() if k])
                    return Data(
                        value=f"Error: Column '{requested_col}' not found. CSV columns (normalized): {available}"
                    )

                actual_key = header_map[requested_col]

                for row in reader:
                    total += 1
                    if _add_word(cur, lang, row.get(actual_key, "")):
                        inserted_attempts += 1

            return Data(
                value=f"Success: processed {total} rows. Inserted {inserted_attempts} words into tutor.words for language={lang}."
            )
        except Exception as e:
            return Data(value=f"Error: {type(e).__name__}: {str(e)}")
        finally:
            if conn is not None:
                conn.close()

import contextlib
import sqlite3

DB_NAME = "links.db"


@contextlib.contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    try:
        yield conn
    finally:
        conn.close()

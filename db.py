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


def init_db() -> None:
    with get_db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS links(
                id TEXT PRIMARY KEY,
                link TEXT NOT NULL
            )
            """
        )
        conn.commit()

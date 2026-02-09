import contextlib
import sqlite3
import uuid

from fastapi import HTTPException
from pydantic import HttpUrl

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


def add_link_to_db(link: HttpUrl) -> uuid.UUID:
    link_id = uuid.uuid4()

    with get_db_connection() as conn:
        conn.execute(
            "INSERT INTO links (id, link) VALUES (?, ?)",
            (str(link_id), str(link)),
        )
        conn.commit()

    return link_id


def get_link_by_id(link_id: uuid.UUID) -> str:
    with get_db_connection() as conn:
        cursor = conn.execute(
            "SELECT link FROM links WHERE id = ?",
            (str(link_id),),
        )
        row = cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Link not found")

    return row["link"]

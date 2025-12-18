import os
import sqlite3
from typing import Optional

USER_DB = os.path.expanduser("~/.local/share/infosec_notes/notes.db")

def ensure_db(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            host TEXT,
            timestamp TEXT NOT NULL,
            project TEXT,
            tasks TEXT,
            notes TEXT,
            directory TEXT
        )
        """
    )


def open_db(path: str) -> sqlite3.Connection:
    dirpath = os.path.dirname(path)
    if not os.path.exists(dirpath):
        try:
            os.makedirs(dirpath, exist_ok=True)
        except PermissionError:
            raise
    conn = sqlite3.connect(path)
    ensure_db(conn)
    return conn


def get_db_connection(db_path: Optional[str] = None) -> tuple[sqlite3.Connection, str]:
    candidate_paths = [USER_DB]
    if db_path:
        candidate_paths.insert(0, db_path)

    conn = None
    last_exc = None
    used_path = None
    
    for p in candidate_paths:
        try:
            conn = open_db(p)
            used_path = p
            break
        except PermissionError as e:
            last_exc = e
            continue
    
    if conn is None:
        raise RuntimeError(f"Cannot open database (permission denied). Last error: {last_exc}")
    
    return conn, used_path

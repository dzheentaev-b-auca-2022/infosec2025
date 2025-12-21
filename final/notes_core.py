import datetime
import getpass
import hashlib
import os
import socket
import sys
from typing import Iterable, Optional

from database import get_db_connection


class Note:
    def __init__(
        self,
        id: int,
        username: str,
        host: str,
        timestamp: str,
        project: Optional[str],
        tasks: Optional[str],
        notes: Optional[str],
        directory: Optional[str],
        is_hidden: bool = False,
    ):
        self.id = id
        self.username = username
        self.host = host
        self.timestamp = timestamp
        self.project = project
        self.tasks = tasks
        self.notes = notes
        self.directory = directory
        self.is_hidden = is_hidden
    
    def __str__(self) -> str:
        hidden_mark = " [HIDDEN]" if self.is_hidden else ""
        lines = [
            f"[{self.id}]{hidden_mark} {self.timestamp} | {self.username}@{self.host} | "
            f"project={self.project or '-'} | dir={self.directory or '-'}"
        ]
        if self.tasks:
            lines.append(f"  tasks: {self.tasks}")
        if self.notes:
            lines.append(f"  notes: {self.notes}")
        lines.append("")
        return "\n".join(lines)


def hash_password(password: str) -> str:
    """Simple SHA-256 hash for password protection."""
    return hashlib.sha256(password.encode()).hexdigest()


def add_note(
    project: Optional[str],
    tasks: Iterable[str],
    note: Optional[str],
    db_path: Optional[str] = None,
    hidden: bool = False,
    password: Optional[str] = None,
) -> None:
    privacy_level = os.environ.get("NOTES_PRIVACY_LEVEL", "full").lower()
    
    if privacy_level == "minimal":
        username = "user"
        host = "host"
        directory = "/redacted"
    else:
        username = getpass.getuser() if not os.environ.get("NOTES_HIDE_USERNAME") else "user"
        host = socket.gethostname() if not os.environ.get("NOTES_HIDE_HOST") else "host"
        directory = os.getcwd() if not os.environ.get("NOTES_HIDE_DIR") else "/redacted"

    ts = datetime.datetime.utcnow().isoformat() + "Z"
    tasks_text = "; ".join([t.strip() for t in tasks if t.strip()])

    try:
        conn, used_path = get_db_connection(db_path)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

    pw_hash = hash_password(password) if hidden and password else None

    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO notes (username, host, timestamp, project, tasks, notes, directory, is_hidden, password_hash) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (username, host, ts, project, tasks_text, note, directory, 1 if hidden else 0, pw_hash),
        )
        conn.commit()
        print(f"Saved note for user '{username}' to {used_path}")
    finally:
        conn.close()


def list_notes(
    limit: int = 20,
    user: Optional[str] = None,
    project: Optional[str] = None,
    directory: Optional[str] = None,
    db_path: Optional[str] = None,
    show_hidden: bool = False,
    password: Optional[str] = None,
) -> None:
    try:
        conn, _ = get_db_connection(db_path)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

    try:
        cur = conn.cursor()
        q = "SELECT id, username, host, timestamp, project, tasks, notes, directory, is_hidden, password_hash FROM notes"
        conds = []
        params = []
        
        if not show_hidden:
            conds.append("is_hidden = 0")
        elif password:
            # We don't filter by password in SQL for simplicity in this demo, 
            # we check it after fetching or we could filter by hash if we want.
            # Filtering by hash is better if we have many notes.
            conds.append("(is_hidden = 0 OR (is_hidden = 1 AND password_hash = ?))")
            params.append(hash_password(password))
        else:
            # show_hidden is true but no password provided -> only show non-hidden
            conds.append("is_hidden = 0")

        
        if user:
            conds.append("username = ?")
            params.append(user)
        if project:
            conds.append("project = ?")
            params.append(project)
        if directory:
            conds.append("directory = ?")
            params.append(directory)
        
        if conds:
            q += " WHERE " + " AND ".join(conds)
        q += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cur.execute(q, params)
        rows = cur.fetchall()
        
        if not rows:
            print("No notes found.")
            return
        
        for row in rows:
            id_, username, host, ts, proj, tasks, notes_text, direc, hidden_flag, pw_hash = row
            note = Note(id_, username, host, ts, proj, tasks, notes_text, direc, bool(hidden_flag))
            print(note, end="")
    finally:
        conn.close()


def remove_note(
    note_id: int,
    db_path: Optional[str] = None,
) -> None:
    try:
        conn, used_path = get_db_connection(db_path)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        
        if cur.rowcount == 0:
            print(f"Error: Note with id {note_id} not found.", file=sys.stderr)
            sys.exit(1)
        
        conn.commit()
        print(f"Deleted note with id {note_id}")
    finally:
        conn.close()

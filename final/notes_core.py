import datetime
import getpass
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
    ):
        self.id = id
        self.username = username
        self.host = host
        self.timestamp = timestamp
        self.project = project
        self.tasks = tasks
        self.notes = notes
        self.directory = directory
    
    def __str__(self) -> str:
        lines = [
            f"[{self.id}] {self.timestamp} | {self.username}@{self.host} | "
            f"project={self.project or '-'} | dir={self.directory or '-'}"
        ]
        if self.tasks:
            lines.append(f"  tasks: {self.tasks}")
        if self.notes:
            lines.append(f"  notes: {self.notes}")
        lines.append("")
        return "\n".join(lines)


def add_note(
    project: Optional[str],
    tasks: Iterable[str],
    note: Optional[str],
    db_path: Optional[str] = None,
) -> None:
    username = getpass.getuser()
    host = socket.gethostname()
    directory = os.getcwd()
    ts = datetime.datetime.utcnow().isoformat() + "Z"
    tasks_text = "; ".join([t.strip() for t in tasks if t.strip()])

    try:
        conn, used_path = get_db_connection(db_path)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO notes (username, host, timestamp, project, tasks, notes, directory) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (username, host, ts, project, tasks_text, note, directory),
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
) -> None:
    try:
        conn, _ = get_db_connection(db_path)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

    try:
        cur = conn.cursor()
        q = "SELECT id, username, host, timestamp, project, tasks, notes, directory FROM notes"
        conds = []
        params = []
        
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
            id_, username, host, ts, proj, tasks, notes_text, direc = row
            note = Note(id_, username, host, ts, proj, tasks, notes_text, direc)
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

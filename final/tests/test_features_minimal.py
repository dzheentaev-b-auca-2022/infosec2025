import os
import sqlite3
import unittest
import tempfile
import datetime
import getpass
import hashlib
from notes_core import add_note, list_notes, hash_password
from database import open_db

class TestNotesPrivacy(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        open_db(self.db_path).close()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)
        for key in ["NOTES_PRIVACY_LEVEL", "NOTES_HIDE_USERNAME", "NOTES_HIDE_HOST", "NOTES_HIDE_DIR"]:
            if key in os.environ:
                del os.environ[key]

    def test_minimal_privacy(self):
        os.environ["NOTES_PRIVACY_LEVEL"] = "minimal"
        add_note("proj", ["task1"], "note1", db_path=self.db_path)
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT username, host, directory FROM notes")
        row = cur.fetchone()
        self.assertEqual(row[0], "user")
        self.assertEqual(row[1], "host")
        self.assertEqual(row[2], "/redacted")
        conn.close()

class TestHiddenNotes(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        open_db(self.db_path).close()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_hidden_note_storage(self):
        add_note("proj", ["task1"], "note1", db_path=self.db_path, hidden=True, password="pass")
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT is_hidden, password_hash FROM notes")
        row = cur.fetchone()
        self.assertEqual(row[0], 1)
        self.assertEqual(row[1], hashlib.sha256("pass".encode()).hexdigest())
        conn.close()

if __name__ == "__main__":
    unittest.main()

import os
import sqlite3
import unittest
import tempfile
import datetime
import getpass
from notes_core import add_note, list_notes, hash_password
from database import open_db

class TestNotesPrivacy(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        # Initialize DB
        conn = open_db(self.db_path)
        conn.close()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)
        for key in ["NOTES_PRIVACY_LEVEL", "NOTES_HIDE_USERNAME", "NOTES_HIDE_HOST", "NOTES_HIDE_DIR"]:
            if key in os.environ:
                del os.environ[key]

    def test_full_privacy_default(self):
        add_note("proj", ["task1"], "note1", db_path=self.db_path)
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT username, host, directory FROM notes")
        row = cur.fetchone()
        self.assertNotEqual(row[0], "user")
        self.assertNotEqual(row[1], "host")
        self.assertNotEqual(row[2], "/redacted")
        conn.close()

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

    def test_granular_privacy(self):
        os.environ["NOTES_HIDE_USERNAME"] = "1"
        add_note("proj", ["task1"], "note1", db_path=self.db_path)
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT username, host, directory FROM notes")
        row = cur.fetchone()
        self.assertEqual(row[0], "user")
        self.assertNotEqual(row[1], "host")
        conn.close()

class TestHiddenNotes(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        open_db(self.db_path).close()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_hidden_note_storage(self):
        add_note("proj", ["task1"], "note1", db_path=self.db_path, hidden=True, password="secret_password")
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT is_hidden, password_hash FROM notes")
        row = cur.fetchone()
        self.assertEqual(row[0], 1)
        self.assertEqual(row[1], hash_password("secret_password"))
        conn.close()

    def test_list_hidden_notes(self):
        add_note("proj", ["task1"], "visible_note", db_path=self.db_path)
        add_note("proj", ["task2"], "hidden_note", db_path=self.db_path, hidden=True, password="pass")
        
        import io
        from contextlib import redirect_stdout
        
        # Test default list (no hidden)
        f = io.StringIO()
        with redirect_stdout(f):
            list_notes(db_path=self.db_path)
        output = f.getvalue()
        self.assertIn("visible_note", output)
        self.assertNotIn("hidden_note", output)

        # Test list with hidden but wrong password
        f = io.StringIO()
        with redirect_stdout(f):
            list_notes(db_path=self.db_path, show_hidden=True, password="wrong")
        output = f.getvalue()
        self.assertIn("visible_note", output)
        self.assertNotIn("hidden_note", output)

        # Test list with hidden and correct password
        f = io.StringIO()
        with redirect_stdout(f):
            list_notes(db_path=self.db_path, show_hidden=True, password="pass")
        output = f.getvalue()
        self.assertIn("visible_note", output)
        self.assertIn("hidden_note", output)

if __name__ == "__main__":
    unittest.main()

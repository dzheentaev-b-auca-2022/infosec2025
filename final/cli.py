"""CLI argument parsing and command routing."""

import argparse
import os
import sys
from typing import Optional

from notes_core import add_note, list_notes, remove_note


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse and return command-line arguments."""
    p = argparse.ArgumentParser(description="Notes for completed tasks (system-friendly)")
    sub = p.add_subparsers(dest="cmd", required=True)

    # Add subcommand
    add = sub.add_parser("add", help="Add a completed-task note")
    add.add_argument("--project", "-p", help="Project name")
    add.add_argument("--tasks", "-t", action="append", help="Task completed (can be repeated)")
    add.add_argument("--note", "-n", help="Special notes or comments")
    add.add_argument("--hidden", action="store_true", help="Mark note as hidden (password protected)")
    add.add_argument("--db", help="(Optional) override DB path (for testing)")

    # List subcommand
    lst = sub.add_parser("list", help="List saved notes")
    lst.add_argument("--limit", "-l", type=int, default=20)
    lst.add_argument("--user", help="Filter by username")
    lst.add_argument("--project", help="Filter by project")
    lst.add_argument("--directory", "-d", help="Filter by directory")
    lst.add_argument("--hidden", action="store_true", help="Show hidden notes (requires password)")
    lst.add_argument("--db", help="(Optional) override DB path (for testing)")

    # List-dir subcommand
    ldir = sub.add_parser("list-dir", help="List notes from current directory")
    ldir.add_argument("--limit", "-l", type=int, default=20)
    ldir.add_argument("--db", help="(Optional) override DB path (for testing)")

    # Remove subcommand
    rm = sub.add_parser("remove", help="Remove a note by id")
    rm.add_argument("id", type=int, help="ID of the note to remove")
    rm.add_argument("--db", help="(Optional) override DB path (for testing)")

    return p.parse_args(argv)


def read_tasks_from_stdin() -> list[str]:
    """Read task lines from stdin if available."""
    if sys.stdin.isatty():
        return []
    text = sys.stdin.read().strip()
    if text:
        return [line for line in text.splitlines() if line.strip()]
    return []


def handle_add_command(args: argparse.Namespace) -> None:
    """Handle the 'add' subcommand."""
    tasks = args.tasks or []
    
    # If no --tasks provided, allow reading from stdin
    if not tasks:
        tasks = read_tasks_from_stdin()
    
    if not tasks:
        print("Provide at least one --tasks (-t) or pass tasks via stdin.")
        sys.exit(1)
    
    password = None
    if args.hidden:
        import getpass
        password = getpass.getpass("Enter password for hidden note: ")
        if not password:
            print("Error: Password required for hidden note.", file=sys.stderr)
            sys.exit(1)

    add_note(args.project, tasks, args.note, db_path=args.db, hidden=args.hidden, password=password)


def handle_list_command(args: argparse.Namespace) -> None:
    """Handle the 'list' subcommand."""
    password = None
    if args.hidden:
        import getpass
        password = getpass.getpass("Enter password to view hidden notes: ")
    
    list_notes(
        limit=args.limit,
        user=args.user,
        project=args.project,
        directory=args.directory,
        db_path=args.db,
        show_hidden=args.hidden,
        password=password,
    )


def handle_list_dir_command(args: argparse.Namespace) -> None:
    """Handle the 'list-dir' subcommand."""
    current_dir = os.getcwd()
    list_notes(limit=args.limit, directory=current_dir, db_path=args.db)


def handle_remove_command(args: argparse.Namespace) -> None:
    """Handle the 'remove' subcommand."""
    remove_note(args.id, db_path=args.db)


def dispatch(args: argparse.Namespace) -> None:
    """Route commands to their handlers."""
    if args.cmd == "add":
        handle_add_command(args)
    elif args.cmd == "list":
        handle_list_command(args)
    elif args.cmd == "list-dir":
        handle_list_dir_command(args)
    elif args.cmd == "remove":
        handle_remove_command(args)
    else:
        print(f"Unknown command: {args.cmd}", file=sys.stderr)
        sys.exit(1)

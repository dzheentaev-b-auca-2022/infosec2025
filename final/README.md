# Notes CLI (final/)

Small terminal utility to save short notes about completed tasks. The script stores entries in an SQLite database and captures username, host, and timestamp.

[demo.webm](https://github.com/user-attachments/assets/3e3dfdf7-d8ea-433b-8f84-10eb0a95eea3)

## Architecture

The code is organized into modular components:
- **`database.py`**: Database connection, schema management, and path selection
- **`notes_core.py`**: Core business logic (Note class, add_note, list_notes functions)
- **`cli.py`**: CLI argument parsing and command routing
- **`main.py`**: Entry point script

## Usage (per-user, no sudo required)


```bash
python3 final/main.py add -p "ProjectX" -t "fixed bug #12" -n "Deployed to staging"
python3 final/main.py list --limit 10
python3 final/main.py list-dir
```

## Installer (system-wide, requires sudo)

```bash
cd final
sudo ./install.sh
# then you can run `notes add ...` directly
```

## Notes
- Script prefers a system DB at `/var/lib/infosec_notes/notes.db` when available.
- If the system DB cannot be used (no permissions), it falls back to `~/.local/share/infosec_notes/notes.db`.
- `add` accepts multiple `-t/--tasks` flags or can read tasks from stdin.
- `list-dir` lists all notes from the current working directory.

## Examples

```bash
# multiple tasks
python3 final/main.py add -p Infra -t "updated firewall" -t "restarted service"

# read tasks from a pipe
printf "one task\nanother task" | python3 final/main.py add -p Misc -n "notes"

# list recent
python3 final/main.py list -l 5

# list notes from current directory
python3 final/main.py list-dir

# filter by specific directory
python3 final/main.py list -d /path/to/project
```

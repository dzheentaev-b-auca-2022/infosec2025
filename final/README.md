# Notes CLI (final/)

Small terminal utility to save short notes about completed tasks. The script stores entries in an SQLite database and captures username, host, and timestamp (respecting privacy settings).

[box_demo.webm](https://github.com/user-attachments/assets/3e3dfdf7-d8ea-433b-8f84-10eb0a95eea3)

## Architecture

The code is organized into modular components:
- **`database.py`**: Database connection, schema management, and path selection
- **`notes_core.py`**: Core business logic (Note class, add_note, list_notes functions)
- **`cli.py`**: CLI argument parsing and command routing
- **`main.py`**: Entry point script

## Usage (Local)

When running from the project root:

```bash
python3 final/main.py add -p "ProjectX" -t "fixed bug #12" -n "Deployed to staging"
python3 final/main.py list --limit 10
python3 final/main.py list-dir
```

## Installer (System-wide)

```bash
cd final
sudo ./install.sh
# then you can run `notes add ...` directly from anywhere
```

## Privacy Settings

You can control what system data is stored using environment variables:

- `NOTES_PRIVACY_LEVEL`: Set to `minimal` to redact all system data (username, host, directory). Default is `full`.
- `NOTES_HIDE_USERNAME`: Set to any value to redact the username.
- `NOTES_HIDE_HOST`: Set to any value to redact the hostname.
- `NOTES_HIDE_DIR`: Set to any value to redact the current working directory.

Example:
```bash
NOTES_PRIVACY_LEVEL=minimal python3 final/main.py add -t "Privacy first task"
```

## Hidden Notes

Notes can be marked as hidden and protected by a password.

### Adding a Hidden Note
```bash
python3 final/main.py add --hidden -t "Secret task"
# You will be prompted for a password
```

### Listing Hidden Notes
Hidden notes are excluded by default. To view them:
```bash
python3 final/main.py list --hidden
# You will be prompted for the password
```

## Implementation Details
- Script prefers a system DB at `/var/lib/infosec_notes/notes.db` when available.
- If the system DB cannot be used (no permissions), it falls back to `~/.local/share/infosec_notes/notes.db`.
- `add` accepts multiple `-t/--tasks` flags or can read tasks from stdin.
- `list-dir` lists all notes from the current working directory.
- `remove <id>` deletes a note by its ID.
- Hidden notes use SHA-256 hashing for password protection.

## Examples

```bash
# Add multiple tasks
python3 final/main.py add -p Infra -t "updated firewall" -t "restarted service"

# Read tasks from a pipe
printf "one task\nanother task" | python3 final/main.py add -p Misc -n "notes"

# List recent notes
python3 final/main.py list -l 5

# List notes from current directory
python3 final/main.py list-dir

# Filter by specific directory
python3 final/main.py list -d /path/to/project

# Remove a note
python3 final/main.py remove 1
```

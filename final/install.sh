#!/usr/bin/env bash
# Installer for the notes utility (requires sudo to install system-wide)

set -euo pipefail

DB_DIR="/var/lib/infosec_notes"
DB_PATH="$DB_DIR/notes.db"
BIN_PATH="/usr/local/bin/notes"
SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_SRC="$SELF_DIR/main.py"

if [[ ! -f "$SCRIPT_SRC" ]]; then
  echo "Cannot find $SCRIPT_SRC; run this from the repository's final/ directory." >&2
  exit 1
fi

echo "Creating system DB dir $DB_DIR (requires sudo)..."
sudo mkdir -p "$DB_DIR"
sudo chown root:root "$DB_DIR"
sudo chmod 0755 "$DB_DIR"

echo "Installing script to $BIN_PATH"
sudo ln -sf "$SCRIPT_SRC" "$BIN_PATH"
sudo chmod 0755 "$SCRIPT_SRC"

echo "Done. You can now run 'notes add ...' and 'notes list'."
echo "If you prefer to keep the DB per-user, don't run this installer."

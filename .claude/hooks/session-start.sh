#!/bin/bash
# Prepares a Claude Code on the web session so the programs work from the first message.
#
# Why it exists: in the cloud nobody follows the installation guide, and the system's own
# Python packages there can break pypdf (the PDF reader). So, at the start of each web
# session, this script creates the project's own environment (.venv), installs
# requirements.txt in it and makes "python" and "python3" point to it.
# It does nothing on a personal computer: there, docs/instalacion.md is followed.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
cd "$CLAUDE_PROJECT_DIR"

# Created only once; later sessions reuse it (safe to run many times).
if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
fi
.venv/bin/python -m pip install --quiet --disable-pip-version-check -r requirements.txt

# Folder for research data (decision 0003): outside the repository. In the cloud it is
# temporary and disappears when the session ends.
mkdir -p "$HOME/Investigacion"

if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  {
    echo "export VIRTUAL_ENV=\"$CLAUDE_PROJECT_DIR/.venv\""
    echo "export PATH=\"$CLAUDE_PROJECT_DIR/.venv/bin:\$PATH\""
    echo "export LORU_DATOS=\"\$HOME/Investigacion\""
  } >> "$CLAUDE_ENV_FILE"
fi

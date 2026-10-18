#!/usr/bin/env bash
set -e

if [ ! -d "venv" ]; then
    echo "Creating venv..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Running librarian.py..."
python librarian.py


echo "Done."
echo "To activate the environment later:"
echo "    source venv/bin/activate"
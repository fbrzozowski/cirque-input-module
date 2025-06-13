#!/bin/bash

SCRIPT_DIR=$(dirname "$(realpath "$0")")
VENV_DIR="$SCRIPT_DIR/venv"
PY_SCRIPT="$SCRIPT_DIR/curve-generator.py"
REQ_FILE="$SCRIPT_DIR/requirements.txt"

# Create venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Install dependencies
pip install --upgrade pip > /dev/null
pip3 install -r "$REQ_FILE" > /dev/null

# Run the script
echo "Starting curve generator..."
python3 "$PY_SCRIPT"


#!/bin/bash

set -e  # Exit on error

PROJECT_DIR="$(pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

echo "-----------------------------------------"
echo " Resetting Python Virtual Environment"
echo " Project: $PROJECT_DIR"
echo "-----------------------------------------"

# 1. Remove existing .venv
if [ -d "$VENV_DIR" ]; then
    echo "🗑️  Removing old .venv ..."
    rm -rf "$VENV_DIR"
else
    echo "ℹ️  No existing .venv found. Skipping removal."
fi

# 2. Create new .venv
echo "🐍  Creating new virtual environment ..."
python3 -m venv "$VENV_DIR"

# 3. Activate new environment
echo "🔌  Activating new environment ..."
source "$VENV_DIR/bin/activate"

# 4. Install dependencies
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    echo "📦  Installing packages from requirements.txt ..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Dependencies installed."
else
    echo "⚠️  No requirements.txt found. Skipping package install."
fi

echo "-----------------------------------------"
echo "🎉 Virtual environment reset complete!"
echo "📍 Activated: $(which python)"
echo "-----------------------------------------"

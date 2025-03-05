#!/bin/bash

export STREAMLIT_THEME_BASE="dark"
export STREAMLIT_THEME_PRIMARY_COLOR="#e4a800"
export STREAMLIT_THEME_TEXT_COLOR="#ffffff"


cd search

# Detect OS
OS=$(uname | tr '[:upper:]' '[:lower:]')

# Check if running in PowerShell (for Windows)
if [[ "$OS" == "mingw"* || "$OS" == "cygwin" ]]; then
    if [[ "$SHELL" == *"pwsh"* || "$SHELL" == *"powershell"* ]]; then
        ACTIVATE_CMD=".venv\\Scripts\\Activate.ps1"
        RUN_PYTHON="Start-Process python backend\\main.py"
        RUN_STREAMLIT="Start-Process streamlit -ArgumentList 'run frontend\\app.py'"
    else
        ACTIVATE_CMD="source .venv/Scripts/activate"
        RUN_PYTHON="start python backend/main.py"
        RUN_STREAMLIT="start streamlit run frontend/app.py"
    fi
elif [[ "$OS" == "darwin" || "$OS" == "linux" ]]; then
    ACTIVATE_CMD=". .venv/bin/activate"
    RUN_PYTHON="python backend/main.py &"
    RUN_STREAMLIT="streamlit run frontend/app.py"
else
    echo "Unsupported OS: $OS"
    exit 1
fi

# Check if venv does not exist then create it
if [ ! -d "venv" ]; then
    python -m venv .venv
fi

eval "$ACTIVATE_CMD"

pip install --upgrade pip --quiet
pip install --upgrade -r ../requirements.txt --quiet

# Run Python scripts
eval "$RUN_PYTHON" &
eval "$RUN_STREAMLIT"

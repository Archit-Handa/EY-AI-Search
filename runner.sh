#!/bin/bash

cd search

# Detect OS
OS=$(uname | tr '[:upper:]' '[:lower:]')

# Check if running in PowerShell (for Windows)
if [[ "$OS" == "mingw"* || "$OS" == "cygwin" ]]; then
    if [[ "$SHELL" == *"pwsh"* || "$SHELL" == *"powershell"* ]]; then
        ACTIVATE_CMD=".venv\\Scripts\\Activate.ps1"
        RUN_PYTHON="Start-Process python main.py"
        RUN_STREAMLIT="Start-Process streamlit -ArgumentList 'run app.py'"
    else
        ACTIVATE_CMD="source .venv/Scripts/activate"
        RUN_PYTHON="start python main.py"
        RUN_STREAMLIT="start streamlit run app.py"
    fi
elif [[ "$OS" == "darwin" || "$OS" == "linux" ]]; then
    ACTIVATE_CMD=". .venv/bin/activate"
    RUN_PYTHON="python main.py &"
    RUN_STREAMLIT="streamlit run app.py"
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
pip install -r ../requirements.txt --quiet

# Run Python scripts
eval "$RUN_PYTHON" &
eval "$RUN_STREAMLIT"

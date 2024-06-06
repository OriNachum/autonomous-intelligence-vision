#!/bin/bash

# Set the path to the Python executable


# Check if the virtual environment already exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment (.venv)"
    python3 -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install packages from requirements.txt
echo "Installing packages from requirements.txt"
pip3 install -r requirements.txt

echo "Done!"

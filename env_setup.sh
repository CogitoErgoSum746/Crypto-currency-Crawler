#!/bin/bash

# Update package lists
apt update

# Install Python 3 pip
apt install python-pip python-venv

# Check if pip is installed successfully
if pip --version &> /dev/null; then
    echo "pip is installed. Continuing with the rest of the commands..."
    # Create a virtual environment named 'env'
    python -m venv env

    # Activate the virtual environment
    source env/bin/activate

    # Install dependencies from requirements.txt
    pip install -r requirements.txt
else
    echo "pip is not installed. Exiting..."
    exit 1
fi
#!/bin/bash

# Upgrade pip
pip install --upgrade pip

# Install packages from requirements.txt
pip install -r requirements.txt

# Set up pre-commit hooks
pre-commit install

echo "Setup Completed..."

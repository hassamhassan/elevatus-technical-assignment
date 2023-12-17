#!/bin/bash

# Upgrade pip
pip install --upgrade pip

# Install packages
pip install poetry

poetry install

# Set up pre-commit hooks
pre-commit install

echo "Setup Completed..."

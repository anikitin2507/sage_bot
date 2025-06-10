#!/bin/bash

# Ensure we're in the project root
cd "$(dirname "$0")/.." || exit

echo "Running black formatter..."
black .

echo "Running ruff linter and auto-fixes..."
ruff check --fix .

echo "Formatting complete!" 
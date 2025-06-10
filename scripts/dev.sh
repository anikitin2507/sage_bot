#!/bin/bash

# Ensure we're in the project root
cd "$(dirname "$0")/.." || exit

# Check for .env file
if [ ! -f .env ]; then
  echo "Error: .env file not found. Create one based on .env.example first."
  exit 1
fi

# Run the bot in development mode
python main.py 
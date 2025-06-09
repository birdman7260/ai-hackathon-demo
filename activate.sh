#!/bin/zsh

# This script activates the Python virtual environment
# Usage: . ./activate.sh or source ./activate.sh

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  echo "❌ Error: This script must be sourced, not executed directly."
  echo "✨ Run: source ./activate.sh or . ./activate.sh"
  exit 1
fi

echo "🔄 Activating virtual environment..."
source .venv/bin/activate

if [[ $? -eq 0 ]]; then
  echo "✅ Virtual environment activated successfully!"
  echo "📋 Python version: $(python --version)"
  echo "📍 Using Python at: $(which python)"
else
  echo "❌ Failed to activate virtual environment."
  return 1
fi 
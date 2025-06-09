#!/bin/zsh
set -e  # Exit immediately if a command exits with non-zero status

echo "🚀 Starting setup..."

echo "📦 Creating and activating Python virtual environment..."
python -m venv .venv || { echo "❌ Failed to create virtual environment"; exit 1; }
source .venv/bin/activate || { echo "❌ Failed to activate virtual environment"; exit 1; }
echo "✅ Virtual environment created and activated"

echo "📥 Installing required packages..."
pip install -r requirements.txt || { echo "❌ Failed to install packages"; exit 1; }
echo "✅ Packages installed successfully"

echo "🔧 Setting up environment file..."
if [ ! -f .env ]; then
  echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
  echo "MCP_SERVER_URLS=http://localhost:3000" >> .env
  echo "✅ Created .env file"
  echo "⚠️  IMPORTANT: Please edit your .env file to add your OPENAI_API_KEY"
else
  echo "✅ .env file already exists"
fi

echo "🎉 Setup completed successfully!"
echo "🔍 To activate the environment in the future, run: source .venv/bin/activate"
echo "📝 To start the MCP Filesystem server, run: cd servers/src/filesystem && npm start"
echo "🚀 To run the application, run: python graph_demo.py"
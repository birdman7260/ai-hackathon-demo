#!/bin/bash

# Startup script for Docker container
# Starts MCP HTTP server in background and then main application

set -e

echo "🚀 Starting NASA Q&A system with MCP server..."

# Start MCP HTTP server in background with output redirected to /dev/null
echo "🔧 Starting MCP filesystem server..."
FASTMCP_TRANSPORT=http python mcp_filesystem.py > /dev/null 2>&1 &
MCP_PID=$!

# Wait a moment for MCP server to start
sleep 3

# Check if MCP server is running
if kill -0 $MCP_PID 2>/dev/null; then
    echo "✅ MCP server started successfully (PID: $MCP_PID)"
    echo "📡 Available at: http://127.0.0.1:8000"
else
    echo "❌ Failed to start MCP server"
    exit 1
fi

# Start main application
echo "🎯 Starting main Q&A application..."
echo ""
python main.py 
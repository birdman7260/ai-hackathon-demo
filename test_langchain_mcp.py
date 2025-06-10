#!/usr/bin/env python3
"""
Test script for LangChain MCP integration with FastMCP filesystem server.

This script demonstrates how to connect LangChain's MCPToolkit to a running
FastMCP server and use the filesystem tools.
"""

import asyncio
import traceback
from langchain_mcp import MCPToolkit
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp_connection():
    """Test connection to FastMCP server using LangChain MCP toolkit."""
    
    print("🔍 Testing LangChain MCP connection to FastMCP server...")
    
    try:
        # Create server parameters for the FastMCP filesystem server
        server_params = StdioServerParameters(
            command="python",
            args=["mcp_filesystem.py"],
            env=None
        )
        
        print(f"📡 Connecting to FastMCP server: {server_params.command} {' '.join(server_params.args)}")
        
        # Create stdio client connection
        async with stdio_client(server_params) as (read, write):
            print("📡 Stdio client created")
            
            # Create client session
            async with ClientSession(read, write) as session:
                print("📡 Client session created")
                
                # Initialize the session
                init_result = await session.initialize()
                print(f"✅ Session initialized: {init_result}")
                
                # List available tools
                tools_result = await session.list_tools()
                print(f"🔧 Available tools: {tools_result}")
                
                # Create MCPToolkit with the session
                toolkit = MCPToolkit(session=session)
                print("🔧 MCPToolkit created")
                
                # Initialize the toolkit
                await toolkit.initialize()
                print("🔧 MCPToolkit initialized")
                
                # Get available tools
                tools = toolkit.get_tools()
                print(f"🔧 Discovered {len(tools)} MCP tools:")
                
                for tool in tools:
                    print(f"   - {tool.name}: {tool.description}")
                
                return tools
                
    except Exception as e:
        print(f"❌ Error connecting to MCP server: {e}")
        print(f"📋 Full traceback:")
        traceback.print_exc()
        return []

async def main():
    """Main test function."""
    print("🚀 LangChain MCP Integration Test")
    print("=" * 50)
    
    tools = await test_mcp_connection()
    
    if tools:
        print(f"\n✅ Successfully connected to FastMCP server with {len(tools)} tools!")
        print("💡 Ready to integrate with LangGraph workflow")
    else:
        print("\n❌ Failed to connect to FastMCP server")
        print("💡 Make sure the FastMCP server is working correctly")

if __name__ == "__main__":
    asyncio.run(main()) 
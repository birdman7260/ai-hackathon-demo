"""
MCP Client Module - Handles Model Context Protocol integration
Provides sync and async tools for filesystem operations via MCP server
"""

import os
import asyncio
from typing import List
from langchain_core.tools import tool


class MCPClient:
    """Handles MCP server connection and tool creation"""
    
    def __init__(self):
        self.client = None
        self.server_urls = self._get_server_urls()
        
    def _get_server_urls(self) -> List[str]:
        """Get MCP server URLs from environment"""
        urls_str = os.getenv("MCP_SERVER_URLS", "").strip()
        if not urls_str:
            return []
        return [url.strip() for url in urls_str.split(",") if url.strip()]
    
    async def _init_client(self):
        """Initialize MCP client connection"""
        if self.client is not None or not self.server_urls:
            return self.client
            
        from langchain_mcp_adapters.client import MultiServerMCPClient
        
        for i, url in enumerate(self.server_urls):
            try:
                server_name = f"server_{i}"
                clean_url = self._clean_url(url)
                
                config = {
                    server_name: {
                        "url": clean_url,
                        "transport": "streamable_http"
                    }
                }
                
                self.client = MultiServerMCPClient(config)
                tools = await self.client.get_tools(server_name=server_name)
                print(f"✅ MCP client connected: {len(tools)} tools from {clean_url}")
                return self.client
                
            except Exception as e:
                print(f"❌ Error connecting to MCP server {url}: {str(e)}")
                continue
        
        return None
    
    def _clean_url(self, url: str) -> str:
        """Ensure URL has proper MCP endpoint"""
        if not url.endswith('/mcp/'):
            if url.endswith('/mcp'):
                url += '/'
            else:
                url += '/mcp/'
        return url
    
    def get_sync_tools(self) -> List:
        """Get sync wrapper tools for LangGraph integration"""
        if not self.server_urls:
            return []
            
        try:
            asyncio.run(self._init_client())
        except Exception as e:
            print(f"❌ Failed to initialize MCP client: {e}")
            return []
        
        if self.client is None:
            return []
        
        return self._create_sync_tools()
    
    def _create_sync_tools(self) -> List:
        """Create sync wrapper tools"""
        
        @tool
        def list_directory(path: str) -> str:
            """List contents of a directory"""
            return self._run_async_tool("list_directory", {"path": path})
        
        @tool  
        def read_file(file_path: str, max_lines: int = 100) -> str:
            """Read contents of a text file"""
            return self._run_async_tool("read_file", {"file_path": file_path, "max_lines": max_lines})
        
        @tool
        def search_files(directory: str, pattern: str, file_type: str = "") -> str:
            """Search for files by name pattern"""
            return self._run_async_tool("search_files", {
                "directory": directory, 
                "pattern": pattern, 
                "file_type": file_type
            })
        
        @tool
        def get_file_info(file_path: str) -> str:
            """Get detailed file information"""
            return self._run_async_tool("get_file_info", {"file_path": file_path})
        
        return [list_directory, read_file, search_files, get_file_info]
    
    def _run_async_tool(self, tool_name: str, params: dict) -> str:
        """Run an async MCP tool synchronously"""
        async def _run():
            try:
                tools = await self.client.get_tools(server_name="server_0")
                target_tool = next((t for t in tools if t.name == tool_name), None)
                
                if target_tool is None:
                    return f"Error: {tool_name} tool not found"
                
                result = await target_tool.ainvoke(params)
                return result
            except Exception as e:
                return f"Error in {tool_name}: {str(e)}"
        
        try:
            return asyncio.run(_run())
        except Exception as e:
            return f"Error in sync wrapper for {tool_name}: {str(e)}"


# Global instance for reuse
_mcp_client = None

def get_mcp_tools() -> List:
    """Get MCP tools - singleton pattern"""
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = MCPClient()
    return _mcp_client.get_sync_tools() 
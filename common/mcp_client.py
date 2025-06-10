"""
MCP Client Module - Model Context Protocol Integration with Sync/Async Bridge

This module provides integration with MCP (Model Context Protocol) servers, enabling
AI agents to interact with external tools and services. The key challenge solved here
is bridging the gap between async MCP protocols and sync LangChain tool requirements.

MCP ARCHITECTURE:
MCP (Model Context Protocol) enables AI applications to securely connect to external 
data sources and tools. This module specifically integrates with filesystem MCP servers
to provide file operations as AI agent tools.

SYNC/ASYNC CHALLENGE:
- MCP servers operate asynchronously (async/await pattern)
- LangChain React agents expect synchronous tools  
- This module provides sync wrapper tools that internally use async MCP calls

DESIGN PATTERNS:
- Adapter Pattern: Converts async MCP interface to sync tool interface
- Singleton Pattern: Single MCP client instance for efficiency
- Proxy Pattern: Sync tools proxy to async MCP operations
- Factory Pattern: Tool creation with proper error handling

DISTRIBUTED ARCHITECTURE:
User Request → LangGraph Agent → Sync Tool → Async Bridge → HTTP/MCP → MCP Server → OS
"""

import os
import asyncio
from typing import List
from langchain_core.tools import tool


class MCPClient:
    """
    MCP (Model Context Protocol) client with async-to-sync tool conversion.
    
    This class manages the complete lifecycle of MCP integration:
    1. Server discovery and connection management
    2. Async tool retrieval from MCP servers
    3. Sync wrapper tool creation for LangChain compatibility
    4. Error handling and graceful degradation
    
    ASYNC/SYNC BRIDGE:
    The core challenge this class solves is converting async MCP operations
    into sync tools that can be used by LangChain React agents. This is
    accomplished through:
    - asyncio.run() to execute async operations in sync context
    - Proper error boundary isolation
    - Resource cleanup and connection management
    
    THREAD SAFETY:
    This class is designed for single-threaded usage typical of LangChain
    applications. The async operations are serialized through asyncio.run().
    """
    
    def __init__(self):
        """
        Initialize MCP client with environment-based configuration.
        
        INITIALIZATION STRATEGY:
        - Extract server URLs from environment variables
        - Defer connection establishment until first use
        - Enable graceful degradation if no servers configured
        
        ENVIRONMENT CONFIGURATION:
        Reads MCP_SERVER_URLS environment variable containing comma-separated
        list of server URLs. Supports both HTTP and stdio transports.
        """
        self.client = None  # Lazy-loaded MCP client instance
        self.server_urls = self._get_server_urls()
        
    def _get_server_urls(self) -> List[str]:
        """
        Extract and validate MCP server URLs from environment.
        
        Returns:
            List of cleaned server URLs, empty if none configured
            
        ENVIRONMENT VARIABLE FORMAT:
        MCP_SERVER_URLS="http://127.0.0.1:8000,http://other-server:9000"
        
        GRACEFUL DEGRADATION:
        Returns empty list if environment variable is missing or empty,
        allowing the application to run without MCP functionality.
        """
        urls_str = os.getenv("MCP_SERVER_URLS", "").strip()
        if not urls_str:
            return []
        # Split and clean URLs, filtering out empty strings
        return [url.strip() for url in urls_str.split(",") if url.strip()]
    
    async def _init_client(self):
        """
        Initialize MCP client connection asynchronously.
        
        Returns:
            MultiServerMCPClient instance or None if connection fails
            
        CONNECTION STRATEGY:
        - Try each configured server URL in order
        - Use first successful connection
        - Return None if all connections fail (graceful degradation)
        
        TRANSPORT HANDLING:
        Currently supports HTTP transport with streamable_http protocol.
        Could be extended to support stdio and other transports.
        """
        # Return existing client if already initialized
        if self.client is not None or not self.server_urls:
            return self.client
            
        # Import here to avoid import errors if langchain_mcp_adapters not installed
        from langchain_mcp_adapters.client import MultiServerMCPClient
        
        # Try each server URL until one succeeds
        for i, url in enumerate(self.server_urls):
            try:
                server_name = f"server_{i}"
                clean_url = self._clean_url(url)
                
                # Configure MCP client for HTTP transport
                config = {
                    server_name: {
                        "url": clean_url,
                        "transport": "streamable_http"
                    }
                }
                
                # Create client and test connection by getting tools
                self.client = MultiServerMCPClient(config)
                tools = await self.client.get_tools(server_name=server_name)
                print(f"✅ MCP client connected: {len(tools)} tools from {clean_url}")
                return self.client
                
            except Exception as e:
                print(f"❌ Error connecting to MCP server {url}: {str(e)}")
                continue
        
        # All connections failed
        return None
    
    def _clean_url(self, url: str) -> str:
        """
        Ensure URL has proper MCP endpoint suffix.
        
        Args:
            url: Raw server URL from configuration
            
        Returns:
            URL with proper /mcp/ endpoint
            
        MCP PROTOCOL REQUIREMENT:
        MCP servers typically expose their protocol endpoint at /mcp/
        This method ensures the URL is properly formatted for MCP communication.
        """
        if not url.endswith('/mcp/'):
            if url.endswith('/mcp'):
                url += '/'
            else:
                url += '/mcp/'
        return url
    
    def get_sync_tools(self) -> List:
        """
        Get synchronous wrapper tools for LangGraph integration.
        
        Returns:
            List of LangChain tools that wrap async MCP operations
            
        SYNC/ASYNC BRIDGE:
        This method is the core of the async-to-sync conversion:
        1. Initialize async MCP client connection
        2. Create sync wrapper functions for each MCP tool
        3. Each wrapper uses asyncio.run() to execute async operations
        4. Return list of sync tools compatible with LangChain
        
        ERROR HANDLING:
        - Connection failures result in empty tool list (graceful degradation)
        - Individual tool failures are caught and reported as tool errors
        - No exceptions propagate to the calling application
        """
        # Return empty list if no servers configured
        if not self.server_urls:
            return []
            
        # Initialize MCP client connection
        try:
            asyncio.run(self._init_client())
        except Exception as e:
            print(f"❌ Failed to initialize MCP client: {e}")
            return []
        
        # Return empty list if client initialization failed
        if self.client is None:
            return []
        
        # Create and return sync wrapper tools
        return self._create_sync_tools()
    
    def _create_sync_tools(self) -> List:
        """
        Create synchronous wrapper tools for async MCP operations.
        
        Returns:
            List of LangChain tools with sync interfaces
            
        TOOL CREATION STRATEGY:
        Each MCP tool gets a corresponding sync wrapper that:
        - Maintains the same function signature and documentation
        - Uses asyncio.run() to execute async MCP operations
        - Handles errors gracefully with descriptive messages
        - Returns string results compatible with LangChain expectations
        
        SUPPORTED OPERATIONS:
        - list_directory: File system directory listing
        - read_file: Text file content reading
        - search_files: Pattern-based file searching  
        - get_file_info: File metadata and statistics
        """
        
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
        """
        Execute an async MCP tool operation synchronously.
        
        Args:
            tool_name: Name of the MCP tool to execute
            params: Parameters to pass to the tool
            
        Returns:
            String result from the tool execution
            
        ASYNC EXECUTION STRATEGY:
        This method implements the core async-to-sync bridge:
        1. Define async function that performs MCP operation
        2. Use asyncio.run() to execute async function in sync context
        3. Handle both MCP-specific and general execution errors
        4. Return string results that LangChain can process
        
        ERROR ISOLATION:
        Multiple layers of error handling ensure that tool failures
        don't crash the agent:
        - MCP operation errors (network, server, protocol)
        - Tool not found errors (server configuration issues)
        - Async execution errors (event loop, threading)
        """
        async def _run():
            """
            Async function that performs the actual MCP tool execution.
            
            EXECUTION FLOW:
            1. Get available tools from MCP server
            2. Find requested tool by name
            3. Execute tool with provided parameters
            4. Return result or error message
            """
            try:
                # Get current tool list from MCP server
                tools = await self.client.get_tools(server_name="server_0")
                
                # Find the requested tool
                target_tool = next((t for t in tools if t.name == tool_name), None)
                
                if target_tool is None:
                    return f"Error: {tool_name} tool not found"
                
                # Execute the tool with provided parameters
                result = await target_tool.ainvoke(params)
                return result
                
            except Exception as e:
                return f"Error in {tool_name}: {str(e)}"
        
        # Execute async function in sync context
        try:
            return asyncio.run(_run())
        except Exception as e:
            return f"Error in sync wrapper for {tool_name}: {str(e)}"


# GLOBAL INSTANCE FOR EFFICIENT RESOURCE USAGE
# Singleton pattern implementation for application-wide MCP access
_mcp_client = None

def get_mcp_tools() -> List:
    """
    Get MCP tools using singleton pattern.
    
    Returns:
        List of sync wrapper tools for MCP operations
        
    SINGLETON BENEFITS:
    - Single MCP client connection across application
    - Consistent tool behavior throughout system
    - Memory efficient resource usage  
    - Faster subsequent tool requests
    - Simplified lifecycle management
    
    GRACEFUL DEGRADATION:
    Returns empty list if:
    - No MCP servers configured in environment
    - MCP server connection fails
    - MCP library not installed
    
    This allows the application to run with reduced functionality
    rather than failing completely.
    """
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = MCPClient()
    return _mcp_client.get_sync_tools() 
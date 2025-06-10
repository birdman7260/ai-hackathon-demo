# =============================================================================
# NASA Document Q&A System - Main Application
# =============================================================================
# This application creates an intelligent question-answering system that uses
# LangChain and OpenAI to provide executive-level insights from NASA documents.
# The system uses a RAG (Retrieval-Augmented Generation) approach with vector
# similarity search and LLM generation orchestrated by LangGraph.
# =============================================================================

# LangChain components for LLM and embeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# LangChain tool framework
from langchain_core.tools import Tool

# Vector database for document storage and retrieval
from langchain_chroma import Chroma

# Environment configuration
from dotenv import load_dotenv
import os

# Shared utilities
from common import ThinkingSpinner

# Load environment variables with override to ensure .env file takes precedence
# over system environment variables (important for API key management)
load_dotenv(override=True)

# =============================================================================
# LEGACY COMPONENTS (kept for reference)
# =============================================================================
# These components are from the original implementation and are kept for
# reference but not used in the modern workflow

# =============================================================================
# CORE COMPONENTS SETUP
# =============================================================================
# Initialize vector database with embedding function for semantic search
# persist_directory ensures the database persists between sessions
vectordb = Chroma(
    persist_directory="./chroma_db", 
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-small")
)

# Initialize LLM for generating executive-focused responses
# gpt-4o-mini provides good quality at lower cost for this use case
llm = ChatOpenAI(model="gpt-4o-mini")

# =============================================================================
# MCP (Model Context Protocol) INTEGRATION
# =============================================================================
# MCP allows integration with external tools and services
# This section is optional and can be disabled via environment variables

# MCP tools are now handled by langchain_mcp_adapters.client.MultiServerMCPClient
# This provides proper MCP protocol integration instead of custom HTTP wrappers

# Configure MCP client and discover available tools
def get_mcp_tools():
    """
    Discover and configure MCP tools from configured server URLs using proper MCP protocol.
    Returns empty list if no MCP servers are configured (graceful degradation).
    """
    import asyncio
    from langchain_mcp_adapters.client import MultiServerMCPClient
    
    # Get MCP server URLs from environment, skip if empty
    mcp_server_urls_str = os.getenv("MCP_SERVER_URLS", "").strip()
    if not mcp_server_urls_str:
        return []
    
    mcp_server_urls = mcp_server_urls_str.split(",")
    
    async def get_tools_async():
        tools = []
        
        # Attempt to connect to each configured MCP server
        for i, url in enumerate(mcp_server_urls):
            if not url.strip():
                continue
                
            try:
                # Create proper MCP client configuration
                server_name = f"server_{i}"
                
                # Determine transport based on URL
                if url.strip().startswith('http'):
                    # HTTP transport - ensure URL ends with /mcp/
                    clean_url = url.strip()
                    if not clean_url.endswith('/mcp/'):
                        if clean_url.endswith('/mcp'):
                            clean_url += '/'
                        else:
                            clean_url += '/mcp/'
                    
                    config = {
                        server_name: {
                            "url": clean_url,
                            "transport": "streamable_http"
                        }
                    }
                else:
                    # Assume stdio transport
                    config = {
                        server_name: {
                            "command": "python",
                            "args": [url.strip()],
                            "transport": "stdio"
                        }
                    }
                
                # Create MCP client with proper protocol
                client = MultiServerMCPClient(config)
                server_tools = await client.get_tools(server_name=server_name)
                tools.extend(server_tools)
                
                print(f"✅ Connected to MCP server {clean_url if 'clean_url' in locals() else url}: {len(server_tools)} tools")
                
            except Exception as e:
                # Print error but continue - MCP is optional
                print(f"Error connecting to MCP server {url}: {str(e)}")
                
        return tools
    
    # Run async function in event loop
    try:
        return asyncio.run(get_tools_async())
    except Exception as e:
        print(f"Failed to initialize MCP tools: {e}")
        return []

def create_sync_mcp_tools():
    """
    Create sync versions of MCP tools since LangGraph React agent needs sync tools
    """
    import asyncio
    from langchain_mcp_adapters.client import MultiServerMCPClient
    from langchain_core.tools import tool
    
    # Get MCP server URLs from environment
    mcp_server_urls_str = os.getenv("MCP_SERVER_URLS", "").strip()
    if not mcp_server_urls_str:
        return []
    
    mcp_server_urls = mcp_server_urls_str.split(",")
    
    # Initialize client globally for reuse
    global mcp_client
    mcp_client = None
    
    async def init_mcp_client():
        """Initialize MCP client once"""
        global mcp_client
        if mcp_client is not None:
            return mcp_client
            
        for i, url in enumerate(mcp_server_urls):
            if not url.strip():
                continue
                
            try:
                server_name = f"server_{i}"
                clean_url = url.strip()
                if not clean_url.endswith('/mcp/'):
                    if clean_url.endswith('/mcp'):
                        clean_url += '/'
                    else:
                        clean_url += '/mcp/'
                
                config = {
                    server_name: {
                        "url": clean_url,
                        "transport": "streamable_http"
                    }
                }
                
                mcp_client = MultiServerMCPClient(config)
                tools = await mcp_client.get_tools(server_name=server_name)
                print(f"✅ MCP sync wrapper connected: {len(tools)} tools from {clean_url}")
                return mcp_client
                
            except Exception as e:
                print(f"Error in sync wrapper connecting to {url}: {str(e)}")
                continue
        
        return None
    
    # Initialize client
    try:
        asyncio.run(init_mcp_client())
    except Exception as e:
        print(f"Failed to initialize MCP client for sync wrappers: {e}")
        return []
    
    if mcp_client is None:
        return []
    
    # Create sync wrapper tools
    @tool
    def list_directory(path: str) -> str:
        """List contents of a directory"""
        async def _list_directory():
            try:
                # Get the async tool and invoke it
                tools = await mcp_client.get_tools(server_name="server_0")
                list_tool = None
                for t in tools:
                    if t.name == "list_directory":
                        list_tool = t
                        break
                
                if list_tool is None:
                    return "Error: list_directory tool not found"
                
                result = await list_tool.ainvoke({"path": path})
                return result
            except Exception as e:
                return f"Error listing directory: {str(e)}"
        
        try:
            return asyncio.run(_list_directory())
        except Exception as e:
            return f"Error in sync wrapper: {str(e)}"
    
    @tool
    def read_file(file_path: str, max_lines: int = 100) -> str:
        """Read contents of a text file"""
        async def _read_file():
            try:
                tools = await mcp_client.get_tools(server_name="server_0")
                read_tool = None
                for t in tools:
                    if t.name == "read_file":
                        read_tool = t
                        break
                
                if read_tool is None:
                    return "Error: read_file tool not found"
                
                result = await read_tool.ainvoke({"file_path": file_path, "max_lines": max_lines})
                return result
            except Exception as e:
                return f"Error reading file: {str(e)}"
        
        try:
            return asyncio.run(_read_file())
        except Exception as e:
            return f"Error in sync wrapper: {str(e)}"
    
    @tool
    def search_files(directory: str, pattern: str, file_type: str = "") -> str:
        """Search for files by name pattern"""
        async def _search_files():
            try:
                tools = await mcp_client.get_tools(server_name="server_0")
                search_tool = None
                for t in tools:
                    if t.name == "search_files":
                        search_tool = t
                        break
                
                if search_tool is None:
                    return "Error: search_files tool not found"
                
                result = await search_tool.ainvoke({
                    "directory": directory, 
                    "pattern": pattern, 
                    "file_type": file_type
                })
                return result
            except Exception as e:
                return f"Error searching files: {str(e)}"
        
        try:
            return asyncio.run(_search_files())
        except Exception as e:
            return f"Error in sync wrapper: {str(e)}"
    
    @tool
    def get_file_info(file_path: str) -> str:
        """Get detailed file information"""
        async def _get_file_info():
            try:
                tools = await mcp_client.get_tools(server_name="server_0")
                info_tool = None
                for t in tools:
                    if t.name == "get_file_info":
                        info_tool = t
                        break
                
                if info_tool is None:
                    return "Error: get_file_info tool not found"
                
                result = await info_tool.ainvoke({"file_path": file_path})
                return result
            except Exception as e:
                return f"Error getting file info: {str(e)}"
        
        try:
            return asyncio.run(_get_file_info())
        except Exception as e:
            return f"Error in sync wrapper: {str(e)}"
    
    return [list_directory, read_file, search_files, get_file_info]

# Get available MCP tools using sync wrappers
mcp_tools = create_sync_mcp_tools()

# =============================================================================
# MODERN LANGGRAPH WORKFLOW WITH PROPER MCP INTEGRATION
# =============================================================================
# Build a proper LangGraph workflow using best practices

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

# Create NASA search tool
@tool
def nasa_document_search(query: str) -> str:
    """Search NASA documents and provide executive-level answers about space missions, engineering, and NASA policies"""
    hits = vectordb.similarity_search(query, k=4)
    context = "\n\n".join(d.page_content for d in hits)
    prompt = f"""Answer for executives only.\nContext:\n{context}\nQuestion: {query}"""
    answer = llm.invoke(prompt).content
    return answer

# Initialize LLM with proper configuration
llm_with_tools = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Configure tools based on MCP availability
if mcp_tools:
    print(f"🔧 Using modern LangGraph with MCP integration: {len(mcp_tools)} MCP tools + NASA search")
    all_tools = [nasa_document_search] + mcp_tools
    llm_with_tools = llm_with_tools.bind_tools(all_tools)
else:
    print("🔧 Using modern LangGraph with NASA search only")
    all_tools = [nasa_document_search]
    llm_with_tools = llm_with_tools.bind_tools(all_tools)

# Use the prebuilt React agent which handles tool orchestration properly
from langgraph.prebuilt import create_react_agent

# Create system message based on available tools
if mcp_tools:
    system_message = """You are a helpful AI assistant with access to NASA documents and filesystem tools.

TOOLS AVAILABLE:
• nasa_document_search: For questions about NASA missions, engineering, policies, and space exploration
• list_directory: List contents of a directory (use with specific path like "." for current directory)
• read_file: Read contents of text files
• search_files: Search for files by pattern in a directory
• get_file_info: Get detailed information about files

USAGE GUIDELINES:
- For NASA/space questions: Use nasa_document_search
- For filesystem operations: Use the MCP tools explicitly
- Be proactive in using the appropriate tools
- Always provide helpful, detailed responses

Examples:
- "What are NASA's risk strategies?" → Use nasa_document_search
- "List current directory" → Use list_directory with path "."
- "Read README file" → Use read_file with file path"""
else:
    system_message = """You are a helpful AI assistant with access to NASA documents.

Use the nasa_document_search tool to answer questions about NASA missions, engineering, policies, and space exploration.
Always provide executive-level, detailed responses based on the NASA documentation."""

# Create the React agent with tools and system message
chain = create_react_agent(
    model=llm_with_tools,
    tools=all_tools,
    prompt=system_message
)

print("✅ Modern LangGraph workflow compiled successfully!")

# Initialize the thinking spinner
spinner = ThinkingSpinner()

# =============================================================================
# MAIN INTERACTIVE LOOP
# =============================================================================
# Provides a command-line interface for asking questions

if __name__ == "__main__":
    print("🚀 NASA Document Q&A System")
    print("Ask questions about NASA documents. Type 'quit', 'exit', or 'q' to stop.")
    print("=" * 60)
    
    while True:
        # Get user input
        q = input("Ask ▶ ")
        
        # Check for exit commands
        if q.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
            
        try:
            # Use context manager for thinking animation
            with spinner:
                # Execute the modern LangGraph workflow with recursion limit
                out = chain.invoke(
                    {"messages": [HumanMessage(content=q)]},
                    config={"recursion_limit": 25}
                )
            
            # Display results - modern workflow always returns messages
            if out and "messages" in out and out["messages"]:
                # Get the final assistant message
                final_message = out["messages"][-1]
                if hasattr(final_message, 'content') and final_message.content:
                    print("→", final_message.content, "\n")
                else:
                    print("→ No answer generated. Please try a different question.\n")
            else:
                print("→ No answer generated. Please try a different question.\n")
                
        except Exception as e:
            # Handle errors gracefully
            print(f"→ Error: {str(e)}\n")
            print("💡 Tip: Try 'make debug' to check system health")
"""
Agent Factory Module - Creates and configures LangGraph agents
Handles tool integration and system prompt configuration
"""

from typing import List
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from .mcp_client import get_mcp_tools
from .nasa_search import get_nasa_search_tool


class AgentFactory:
    """Factory for creating configured agents"""
    
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0):
        self.model = model
        self.temperature = temperature
    
    def create_agent(self, include_mcp: bool = True):
        """Create an agent with NASA search and optionally MCP tools"""
        # Get tools
        tools = [get_nasa_search_tool()]
        mcp_tools = get_mcp_tools() if include_mcp else []
        
        if mcp_tools:
            tools.extend(mcp_tools)
            print(f"🔧 Agent created with {len(mcp_tools)} MCP tools + NASA search")
        else:
            print("🔧 Agent created with NASA search only")
        
        # Configure LLM
        llm = ChatOpenAI(model=self.model, temperature=self.temperature)
        llm_with_tools = llm.bind_tools(tools)
        
        # Create system prompt
        system_prompt = self._get_system_prompt(bool(mcp_tools))
        
        # Create agent
        agent = create_react_agent(
            model=llm_with_tools,
            tools=tools,
            prompt=system_prompt
        )
        
        return agent
    
    def _get_system_prompt(self, has_mcp_tools: bool) -> str:
        """Generate system prompt based on available tools"""
        if has_mcp_tools:
            return """You are a helpful AI assistant with access to NASA documents and filesystem tools.

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
            return """You are a helpful AI assistant with access to NASA documents.

Use the nasa_document_search tool to answer questions about NASA missions, engineering, policies, and space exploration.
Always provide executive-level, detailed responses based on the NASA documentation."""


def create_nasa_agent(include_mcp: bool = True, model: str = "gpt-4o-mini"):
    """Convenience function to create a NASA Q&A agent"""
    factory = AgentFactory(model=model)
    return factory.create_agent(include_mcp=include_mcp) 
"""
Agent Factory Module - AI Agent Creation and Configuration

This module implements the Factory Pattern for creating and configuring AI agents
with appropriate tools and system prompts. It handles the complex orchestration
of NASA document search capabilities and optional MCP tool integration.

FACTORY PATTERN BENEFITS:
- Encapsulates complex agent creation logic
- Provides consistent agent configuration across the application
- Enables easy testing with different configurations
- Centralizes tool integration and prompt generation

AGENT ARCHITECTURE:
The agents created by this factory follow the React (Reasoning + Acting) pattern:
1. Receive user input
2. Reason about what tools to use
3. Execute tools to gather information
4. Synthesize results into coherent responses

TOOL INTEGRATION STRATEGY:
- NASA Search: Always included for document retrieval capabilities
- MCP Tools: Conditionally included based on server availability
- Dynamic Prompts: System prompts adapt based on available tools
- Error Isolation: Tool failures don't crash the entire agent
"""

from typing import List
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from .mcp_client import get_mcp_tools
from .nasa_search import get_nasa_search_tool


class AgentFactory:
    """
    Factory for creating and configuring AI agents with tools and prompts.
    
    This class encapsulates the complex logic of agent creation:
    - Model configuration and parameter tuning
    - Tool discovery and integration
    - System prompt generation based on available capabilities
    - Error handling and graceful degradation
    
    CONFIGURATION FLEXIBILITY:
    The factory allows customization of:
    - AI model selection (GPT-4, GPT-3.5, etc.)
    - Temperature settings for response creativity
    - Tool inclusion/exclusion for different use cases
    - Custom prompt templates for specialized behavior
    
    DESIGN PATTERNS:
    - Factory Pattern: Centralized object creation
    - Builder Pattern: Step-by-step agent configuration
    - Strategy Pattern: Different tool sets for different scenarios
    - Template Method: Consistent agent creation flow
    """
    
    def __init__(self, model: str = "gpt-4.1", temperature: float = 0.0):
        """
        Initialize agent factory with model configuration.
        
        Args:
            model: OpenAI model name (e.g., "gpt-4o-mini", "gpt-4.1")
            temperature: Response randomness (0=deterministic, 1=creative)
            
        MODEL SELECTION STRATEGY:
        - gpt-4.1: Default choice for cost/performance balance
        - gpt-4: For complex reasoning tasks requiring higher capability
        - Temperature 0.2: Some creativity but not too much
        
        FACTORY CONFIGURATION:
        The factory stores model parameters but defers expensive operations
        (tool loading, agent creation) until actual agent creation time.
        """
        self.model = model
        self.temperature = temperature
    
    def create_agent(self, include_mcp: bool = True):
        """
        Create a configured AI agent with NASA search and optional MCP tools.
        
        Args:
            include_mcp: Whether to include MCP filesystem tools
            
        Returns:
            Configured LangGraph React agent ready for use
            
        AGENT CREATION PIPELINE:
        1. TOOL DISCOVERY: Gather available tools (NASA + optional MCP)
        2. MODEL CONFIGURATION: Set up LLM with tool bindings
        3. PROMPT GENERATION: Create context-aware system prompt
        4. AGENT ASSEMBLY: Combine components into working agent
        
        TOOL INTEGRATION STRATEGY:
        - NASA Search: Always included for core document Q&A functionality
        - MCP Tools: Added conditionally based on server availability
        - Tool Binding: LLM configured with metadata about available tools
        - Error Handling: Failed tool discovery doesn't prevent agent creation
        
        REACT AGENT PATTERN:
        Uses LangGraph's create_react_agent which implements:
        - Reasoning: Agent plans what tools to use for given query
        - Acting: Agent executes tools and observes results
        - Iteration: Agent can use multiple tools in sequence
        - Termination: Agent provides final answer when task complete
        """
        # TOOL DISCOVERY PHASE
        # Start with core NASA document search capability
        tools = [get_nasa_search_tool()]
        
        # Add MCP tools if requested and available
        mcp_tools = get_mcp_tools() if include_mcp else []
        
        if mcp_tools:
            tools.extend(mcp_tools)
            print(f"🔧 Agent created with {len(mcp_tools)} MCP tools + NASA search")
        else:
            print("🔧 Agent created with NASA search only")
        
        # MODEL CONFIGURATION PHASE
        # Configure LLM with specified parameters
        llm = ChatOpenAI(model=self.model, temperature=self.temperature)
        
        # Bind tools to LLM so it knows what capabilities are available
        # This enables the model to generate proper tool calls
        llm_with_tools = llm.bind_tools(tools)
        
        # PROMPT GENERATION PHASE
        # Create system prompt that describes available tools and usage patterns
        system_prompt = self._get_system_prompt(bool(mcp_tools))
        
        # AGENT ASSEMBLY PHASE
        # Combine all components into a working React agent
        agent = create_react_agent(
            model=llm_with_tools,    # LLM with tool metadata
            tools=tools,             # Available tool implementations
            prompt=system_prompt     # System-level instructions
        )
        
        return agent
    
    def _get_system_prompt(self, has_mcp_tools: bool) -> str:
        """
        Generate context-aware system prompt based on available tools.
        
        Args:
            has_mcp_tools: Whether MCP filesystem tools are available
            
        Returns:
            System prompt string optimized for agent behavior
            
        PROMPT ENGINEERING STRATEGY:
        The system prompt is critical for proper agent behavior:
        - Tool Discovery: Describes what tools are available
        - Usage Patterns: Provides examples of proper tool usage
        - Behavioral Guidelines: Sets expectations for response quality
        - Error Handling: Instructs agent on handling tool failures
        
        DYNAMIC PROMPT GENERATION:
        Prompts adapt based on available capabilities:
        - NASA-only: Focused on document search and executive responses
        - NASA+MCP: Includes filesystem operations and file handling
        - Examples: Concrete usage patterns for better tool selection
        
        EXECUTIVE FOCUS:
        All prompts emphasize executive-level communication:
        - Strategic insights over technical details
        - Actionable information and recommendations
        - Concise, high-impact communication style
        """
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


def create_nasa_agent(include_mcp: bool = True, model: str = "gpt-4.1"):
    """
    Convenience function for creating NASA Q&A agents.
    
    Args:
        include_mcp: Whether to include MCP filesystem tools
        model: OpenAI model name for the agent
        
    Returns:
        Configured agent ready for NASA document Q&A
        
    CONVENIENCE FUNCTION BENEFITS:
    - Simplified interface for common use cases
    - Sensible defaults for NASA Q&A scenarios
    - Consistent agent configuration across application
    - Reduced boilerplate code in application entry points
    
    USAGE PATTERNS:
    - Development: include_mcp=True for full feature testing
    - Production: include_mcp based on deployment environment
    - Testing: include_mcp=False for isolated NASA search testing
    - Custom Models: model parameter for different AI capabilities
    
    This function is the primary interface for agent creation in most
    application scenarios, providing a clean abstraction over the
    more complex AgentFactory class.
    """
    factory = AgentFactory(model=model)
    return factory.create_agent(include_mcp=include_mcp) 
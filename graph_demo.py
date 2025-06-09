# =============================================================================
# NASA Document Q&A System - Main Application
# =============================================================================
# This application creates an intelligent question-answering system that uses
# LangChain and OpenAI to provide executive-level insights from NASA documents.
# The system uses a RAG (Retrieval-Augmented Generation) approach with vector
# similarity search and LLM generation orchestrated by LangGraph.
# =============================================================================

# Core imports for type definitions and graph orchestration
from typing import TypedDict
from langgraph.graph import Graph

# LangChain components for LLM and embeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# LangChain tool framework
from langchain_core.tools import Tool
from langchain_core.tools.base import ToolException
from langchain.agents.tools import BaseTool

# Vector database for document storage and retrieval
from langchain_chroma import Chroma

# Environment configuration
from dotenv import load_dotenv
import os
import requests

# Shared utilities
from common import ThinkingSpinner

# Load environment variables with override to ensure .env file takes precedence
# over system environment variables (important for API key management)
load_dotenv(override=True)

# =============================================================================
# STATE DEFINITION
# =============================================================================
# Defines the data structure that flows through the LangGraph workflow

class State(TypedDict):
    """
    State object that flows through the LangGraph workflow.
    
    This TypedDict defines the data structure that gets passed between
    workflow nodes in the RAG pipeline. Each node can read from and
    modify this state as it flows through the execution graph.
    
    Attributes:
        question (str): The user's input question/query
        context (str): Retrieved relevant document chunks from vector search
        answer (str): The final generated executive-level response
    """
    question: str    # User's input question
    context: str     # Retrieved relevant document chunks
    answer: str      # Generated executive-level response

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

# Define MCP tool wrapper class
class MCPTool(BaseTool):
    """
    Wrapper class for Model Context Protocol (MCP) tools.
    
    This class adapts external MCP tools to work within the LangChain framework.
    MCP is a protocol for integrating external tools and services with language
    models, allowing for extended capabilities beyond the base LLM.
    
    The wrapper handles the translation between LangChain's tool interface
    and the MCP protocol, enabling seamless integration of external services.
    
    Attributes:
        name (str): The name of the MCP tool
        callable (callable): The function that executes the MCP tool
        
    Example:
        tool = MCPTool("file_reader", lambda x: read_file(x))
    """
    
    def __init__(self, name: str, callable):
        """
        Initialize the MCP tool wrapper.
        
        Args:
            name (str): Human-readable name for the tool
            callable: Function that implements the tool's functionality
        """
        super().__init__(name=name)
        self.callable = callable
        
    def _run(self, *args, **kwargs):
        """
        Execute the MCP tool with given parameters.
        
        This method is called by LangChain when the tool needs to be executed.
        It delegates to the wrapped callable function.
        
        Args:
            *args: Positional arguments to pass to the tool
            **kwargs: Keyword arguments to pass to the tool
            
        Returns:
            The result from the MCP tool execution
            
        Raises:
            ToolException: If the MCP tool execution fails
        """
        return self.callable(*args, **kwargs)

# Configure MCP client and discover available tools
def get_mcp_tools():
    """
    Discover and configure MCP tools from configured server URLs.
    Returns empty list if no MCP servers are configured (graceful degradation).
    """
    # Get MCP server URLs from environment, skip if empty
    mcp_server_urls_str = os.getenv("MCP_SERVER_URLS", "").strip()
    if not mcp_server_urls_str:
        return []
    
    mcp_server_urls = mcp_server_urls_str.split(",")
    tools = []
    
    # Attempt to connect to each configured MCP server
    for url in mcp_server_urls:
        if not url.strip():
            continue
            
        try:
            # Query server for available tools
            response = requests.get(f"{url.strip()}/mcp")
            if response.status_code == 200:
                data = response.json()
                # Create tool wrappers for each discovered tool
                for tool in data.get("tools", []):
                    tool_name = tool.get("name")
                    if tool_name:
                        # Create a callable for this specific tool
                        def create_tool_callable(tool_url, tool_name):
                            def call_tool(params):
                                response = requests.post(f"{tool_url}/mcp/{tool_name}", json=params)
                                if response.status_code == 200:
                                    return response.json()
                                else:
                                    raise ToolException(f"Error calling {tool_name}: {response.text}")
                            return call_tool
                            
                        callable_fn = create_tool_callable(url.strip(), tool_name)
                        tools.append(MCPTool(name=tool_name, callable=callable_fn))
        except Exception as e:
            # Print error but continue - MCP is optional
            print(f"Error connecting to MCP server {url}: {str(e)}")
            
    return tools

# Get available MCP tools (empty list if none configured)
mcp_tools = get_mcp_tools()

# =============================================================================
# WORKFLOW FUNCTIONS
# =============================================================================
# These functions define the steps in our RAG pipeline

# Tool decorator (currently unused but kept for potential future expansion)
def as_tool(func):
    """
    Decorator to mark functions as workflow tools.
    
    This decorator is designed to mark functions as tools that can be used
    within the LangGraph workflow. Currently it's a pass-through decorator
    but provides a hook for future functionality such as:
    
    - Tool registration and discovery
    - Automatic schema generation
    - Input/output validation
    - Logging and monitoring
    - Error handling standardization
    
    Args:
        func (callable): The function to be marked as a tool
        
    Returns:
        callable: The original function, unmodified
        
    Example:
        @as_tool
        def my_workflow_function(state):
            # Function implementation
            return modified_state
    """
    return func

@as_tool
def retrieve(state: State):
    """
    Retrieve relevant document chunks using vector similarity search.
    
    This function:
    1. Takes the user's question from the state
    2. Performs semantic search in the vector database
    3. Retrieves the top 4 most relevant document chunks
    4. Concatenates them into context for the LLM
    """
    hits = vectordb.similarity_search(state["question"], k=4)
    # Join retrieved documents with double newlines for clear separation
    state["context"] = "\n\n".join(d.page_content for d in hits)
    return state

@as_tool
def generate(state: State):
    """
    Generate executive-level response using LLM.
    
    This function:
    1. Creates a prompt specifically for executive audiences
    2. Includes the retrieved context and user question
    3. Uses the LLM to generate a focused, high-level response
    """
    # Craft prompt specifically for executive-level responses
    prompt = f"""Answer for executives only.\nContext:\n{state['context']}\nQuestion: {state['question']}"""
    # Generate response using the LLM
    state["answer"] = llm.invoke(prompt).content
    
    return state

# =============================================================================
# LANGRAPH WORKFLOW CONSTRUCTION
# =============================================================================
# Build the execution graph that orchestrates our RAG pipeline

# Initialize the graph
graph = Graph()

# Add workflow nodes
graph.add_node("retrieve", retrieve)  # Document retrieval step
graph.add_node("generate", generate)  # Response generation step

# Add any discovered MCP tools as additional nodes
for t in mcp_tools:
    graph.add_node(t.name, t)

# Define workflow execution order
graph.set_entry_point("retrieve")           # Start with document retrieval
graph.add_edge("retrieve", "generate")      # Then generate response
graph.set_finish_point("generate")          # End after generation

# Compile the graph into an executable chain
chain = graph.compile()

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
            # Start the thinking animation
            spinner.start()
            
            # Execute the RAG workflow
            out = chain.invoke({"question": q})
            
            # Stop the animation before displaying results
            spinner.stop()
            
            # Display results with error handling
            if out and "answer" in out:
                print("→", out["answer"], "\n")
            else:
                print("→ No answer generated. Please try a different question.\n")
                
        except Exception as e:
            # Stop animation on error
            spinner.stop()
            # Handle errors gracefully
            print(f"→ Error: {str(e)}\n")
            print("💡 Tip: Try 'make debug' to check system health")
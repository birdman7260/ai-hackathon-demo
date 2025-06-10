# Common Module Documentation

This module contains reusable components for the NASA Document Q&A System, providing clean abstractions for MCP integration, NASA document search, and agent configuration.

## Components

### 🔧 Configuration (`config.py`)
- **`AppConfig`**: Centralized configuration management
- **`get_config()`**: Singleton configuration access
- **`load_environment()`**: Load and validate environment

**Features:**
- Environment variable validation
- Configuration status reporting
- Centralized settings management

### 🚀 NASA Search (`nasa_search.py`) 
- **`NASADocumentSearch`**: Vector database search with lazy loading
- **`get_nasa_search_tool()`**: LangChain tool for agent integration
- **`get_nasa_db_info()`**: Database information and stats

**Features:**
- Executive-level response generation
- Configurable search parameters
- Vector database abstraction

### 🔗 MCP Client (`mcp_client.py`)
- **`MCPClient`**: Handle MCP server connections
- **`get_mcp_tools()`**: Sync wrapper tools for LangGraph
- Filesystem operations: `list_directory`, `read_file`, `search_files`, `get_file_info`

**Features:**
- Async-to-sync tool wrappers
- Multiple server support
- Graceful error handling

### 🤖 Agent Factory (`agent_factory.py`)
- **`AgentFactory`**: Create and configure agents
- **`create_nasa_agent()`**: Convenience function for quick agent creation
- Dynamic system prompt generation

**Features:**
- Tool integration (NASA + MCP)
- Configurable model settings
- Context-aware prompts

### 🎨 UI Components (`thinking_spinner.py`)
- **`ThinkingSpinner`**: Context manager for loading animations
- Terminal-friendly progress indication

## Usage Examples

### Quick Start
```python
from common import create_nasa_agent, load_environment

# Load configuration and create agent
config = load_environment()
agent = create_nasa_agent(include_mcp=True)

# Use agent
response = agent.invoke({"messages": [{"role": "user", "content": "What are NASA's risk strategies?"}]})
```

### Custom Configuration
```python
from common import AgentFactory, AppConfig

# Custom configuration
config = AppConfig()
factory = AgentFactory(model="gpt-4", temperature=0.1)
agent = factory.create_agent(include_mcp=config.has_mcp_servers())
```

### Direct Component Usage
```python
from common import NASADocumentSearch, MCPClient

# Direct NASA search
nasa_search = NASADocumentSearch(db_path="./custom_db")
result = nasa_search.search_documents("Mars missions")

# Direct MCP operations
mcp = MCPClient()
tools = mcp.get_sync_tools()
```

## Architecture Benefits

- **🧩 Modular**: Each component has a single responsibility
- **🔄 Reusable**: Components can be used independently or together
- **🛡️ Robust**: Proper error handling and graceful degradation
- **⚙️ Configurable**: Environment-driven configuration
- **🧪 Testable**: Clean interfaces enable easy testing
- **📦 Maintainable**: Clear separation of concerns

## File Structure
```
common/
├── __init__.py          # Package exports
├── config.py            # Configuration management
├── nasa_search.py       # NASA document search
├── mcp_client.py        # MCP server integration  
├── agent_factory.py     # Agent creation
├── thinking_spinner.py  # UI components
└── README.md           # This documentation
``` 
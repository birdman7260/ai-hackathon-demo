# =============================================================================
# Common Utilities Package
# =============================================================================
# This package contains shared utilities used across the CA DEQ Q&A system.
# =============================================================================

"""
Common utilities package for CA DEQ Document Q&A System
Provides reusable components for MCP integration, CA DEQ search, and agent configuration
"""

from .thinking_spinner import ThinkingSpinner
from .mcp_client import get_mcp_tools, MCPClient
from .cadeq_search import get_cadeq_search_tool, get_cadeq_db_info, CADEQDocumentSearch
from .agent_factory import create_cadeq_agent, AgentFactory
from .config import get_config, load_environment, AppConfig

__all__ = [
    # Original utilities
    'ThinkingSpinner',
    
    # MCP integration
    'get_mcp_tools',
    'MCPClient',
    
    # CA DEQ document search
    'get_cadeq_search_tool',
    'get_cadeq_db_info', 
    'CADEQDocumentSearch',
    
    # Agent creation
    'create_cadeq_agent',
    'AgentFactory',
    
    # Configuration
    'get_config',
    'load_environment',
    'AppConfig'
] 
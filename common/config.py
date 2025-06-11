"""
Configuration Module - Centralized Environment and Application Configuration Management

This module implements a robust configuration system that:
1. Loads and validates environment variables
2. Provides default values for all settings
3. Validates configuration integrity at startup
4. Offers convenient access patterns throughout the application

DESIGN PATTERNS:
- Singleton Pattern: Single configuration instance across the application
- Factory Pattern: Configuration objects created on demand
- Validation Pattern: Early validation of critical settings
- Default Value Pattern: Sensible defaults for all configuration

ARCHITECTURE BENEFITS:
- Centralized configuration eliminates scattered env var access
- Validation prevents runtime errors from missing/invalid config
- Type safety with proper conversion (int, float, bool)
- Environment-driven configuration enables different deployment scenarios
"""

import os
from dotenv import load_dotenv
from typing import Dict, Any


class AppConfig:
    """
    Application configuration manager with validation and type conversion.
    
    This class centralizes all application configuration, providing:
    - Environment variable loading with .env file support
    - Type conversion and validation of configuration values
    - Default values for optional settings
    - Configuration validation with helpful error messages
    - Convenient access methods for different application layers
    
    INITIALIZATION FLOW:
    1. Load .env file (if present) with override=True for development
    2. Extract and convert environment variables to proper types
    3. Apply default values for missing optional settings
    4. Validate critical configuration (API keys, database paths)
    5. Store configuration for efficient repeated access
    
    THREAD SAFETY:
    This class is thread-safe for read operations after initialization.
    All configuration is loaded once during __init__ and then read-only.
    """
    
    def __init__(self):
        """
        Initialize configuration by loading environment variables and validating settings.
        
        ENVIRONMENT VARIABLES LOADED:
        - OPENAI_API_KEY: Required for LLM and embedding operations
        - MCP_SERVER_URLS: Optional, comma-separated list of MCP server URLs
        - OPENAI_MODEL: Optional, defaults to "gpt-4.1"
        - EMBEDDING_MODEL: Optional, defaults to "text-embedding-3-small"
        - VECTORDB_PATH: Optional, defaults to "./chroma_db"
        - RECURSION_LIMIT: Optional, defaults to 25
        - TEMPERATURE: Optional, defaults to 0 (deterministic responses)
        """
        # ENVIRONMENT LOADING
        # Override=True ensures .env file values take precedence over system env vars
        # This is crucial for development environments with multiple projects
        load_dotenv(override=True)
        
        # CORE CONFIGURATION EXTRACTION
        # These settings are fundamental to application operation
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.mcp_server_urls = os.getenv("MCP_SERVER_URLS", "")
        
        # MODEL CONFIGURATION
        # AI model settings with sensible defaults for cost/performance balance
        self.default_model = os.getenv("OPENAI_MODEL", "gpt-4.1")
        self.embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        
        # DATABASE CONFIGURATION
        # Vector database path with default that works for local development
        self.vectordb_path = os.getenv("VECTORDB_PATH", "./chroma_db")
        
        # AGENT BEHAVIOR CONFIGURATION
        # Settings that control AI agent behavior and performance
        # Type conversion with fallbacks to handle invalid values gracefully
        try:
            self.recursion_limit = int(os.getenv("RECURSION_LIMIT", "25"))
        except ValueError:
            self.recursion_limit = 25  # Fallback if env var is not a valid integer
            
        try:
            self.temperature = float(os.getenv("TEMPERATURE", "0.2"))
        except ValueError:
            self.temperature = 0.0  # Fallback if env var is not a valid float
        
        # CONFIGURATION VALIDATION
        # Validate configuration immediately to catch issues early
        # This prevents runtime failures and provides helpful feedback
        self._validate()
    
    def _validate(self):
        """
        Validate configuration settings and provide helpful feedback.
        
        VALIDATION CHECKS:
        1. OpenAI API key format validation (must start with 'sk-')
        2. Vector database existence check with setup instructions
        3. Recursion limit range validation (prevent performance issues)
        4. Temperature range validation (0.0-2.0 for OpenAI models)
        
        DESIGN PHILOSOPHY:
        - Fail fast: Detect configuration issues at startup, not runtime
        - Helpful messages: Provide actionable feedback for fixing issues
        - Non-blocking: Warnings for non-critical issues, errors for critical ones
        """
        # OPENAI API KEY VALIDATION
        # Check for proper OpenAI API key format to catch common configuration errors
        if not self.openai_api_key.startswith("sk-"):
            print("⚠️  Warning: OPENAI_API_KEY not set or invalid")
            print("💡 Tip: Get your API key from https://platform.openai.com/api-keys")
        
        # VECTOR DATABASE VALIDATION
        # Check if vector database exists and provide setup instructions if missing
        if not os.path.exists(self.vectordb_path):
            print(f"⚠️  Warning: Vector database not found at {self.vectordb_path}")
            print("💡 Run 'make fetch-data && make ingest' to create it")
            
        # RECURSION LIMIT VALIDATION
        # Ensure recursion limit is reasonable to prevent performance issues
        if self.recursion_limit < 1 or self.recursion_limit > 100:
            print(f"⚠️  Warning: Recursion limit {self.recursion_limit} is outside recommended range (1-100)")
            
        # TEMPERATURE VALIDATION  
        # Ensure temperature is within valid range for OpenAI models
        if self.temperature < 0.0 or self.temperature > 2.0:
            print(f"⚠️  Warning: Temperature {self.temperature} is outside valid range (0.0-2.0)")
    
    def get_nasa_config(self) -> Dict[str, Any]:
        """
        Get configuration dictionary for NASA document search components.
        
        Returns:
            Dictionary containing NASA search configuration:
            - db_path: Vector database file path
            - model: LLM model name for response generation
            - embedding_model: Embedding model for vector search
            
        This method provides a clean interface for NASA search components
        to get their configuration without direct access to the config class.
        """
        return {
            "db_path": self.vectordb_path,
            "model": self.default_model,
            "embedding_model": self.embedding_model
        }
    
    def get_agent_config(self) -> Dict[str, Any]:
        """
        Get configuration dictionary for AI agent creation and behavior.
        
        Returns:
            Dictionary containing agent configuration:
            - model: LLM model name
            - temperature: Response randomness (0=deterministic, 1=creative)
            - recursion_limit: Maximum agent reasoning steps
            - include_mcp: Whether to include MCP tools based on server availability
            
        This method encapsulates agent configuration logic and provides
        a stable interface for agent factory components.
        """
        return {
            "model": self.default_model,
            "temperature": self.temperature,
            "recursion_limit": self.recursion_limit,
            "include_mcp": bool(self.mcp_server_urls.strip())  # MCP if servers configured
        }
    
    def has_mcp_servers(self) -> bool:
        """
        Check if MCP servers are configured and available.
        
        Returns:
            True if MCP_SERVER_URLS is set and non-empty, False otherwise
            
        This method provides a clean boolean check for MCP availability
        that can be used for conditional feature enabling throughout the app.
        """
        return bool(self.mcp_server_urls.strip())
    
    def print_status(self):
        """
        Print comprehensive configuration status for debugging and monitoring.
        
        Displays:
        - OpenAI API key status (present/missing, no actual key for security)
        - Vector database existence and path
        - MCP server configuration status
        - Current AI model selection
        
        This method is useful for:
        - Startup diagnostics
        - Debugging configuration issues
        - Monitoring deployment status
        """
        print("🔧 Configuration Status:")
        print(f"   OpenAI API Key: {'✅ Set' if self.openai_api_key.startswith('sk-') else '❌ Missing'}")
        print(f"   Vector Database: {'✅ Found' if os.path.exists(self.vectordb_path) else '❌ Missing'}")
        print(f"   MCP Servers: {'✅ Configured' if self.has_mcp_servers() else '⚪ None'}")
        print(f"   Model: {self.default_model}")


# GLOBAL CONFIGURATION INSTANCE
# Singleton pattern implementation for application-wide configuration access
_config = None

def get_config() -> AppConfig:
    """
    Get application configuration using singleton pattern.
    
    Returns:
        AppConfig instance (creates one if none exists)
        
    SINGLETON PATTERN BENEFITS:
    - Single source of truth for configuration
    - Avoids repeated environment variable parsing
    - Ensures consistent configuration across application
    - Memory efficient (single config object)
    
    THREAD SAFETY:
    This implementation is thread-safe for typical usage patterns
    where configuration is loaded early in application lifecycle.
    """
    global _config
    if _config is None:
        _config = AppConfig()
    return _config

def load_environment():
    """
    Load and validate environment configuration with status display.
    
    Returns:
        AppConfig instance with validated configuration
        
    This is a convenience function that:
    1. Loads configuration using singleton pattern
    2. Displays configuration status for user feedback
    3. Returns config object for immediate use
    
    This function is designed for use in main application entry points
    where configuration loading and status display are both needed.
    """
    config = get_config()
    config.print_status()
    return config 
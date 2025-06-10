"""
Configuration Module - Handles environment setup and application configuration
Centralizes all configuration management
"""

import os
from dotenv import load_dotenv
from typing import Dict, Any


class AppConfig:
    """Application configuration manager"""
    
    def __init__(self):
        # Load environment variables
        load_dotenv(override=True)
        
        # Core settings
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.mcp_server_urls = os.getenv("MCP_SERVER_URLS", "")
        
        # Model settings
        self.default_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        
        # Database settings
        self.vectordb_path = os.getenv("VECTORDB_PATH", "./chroma_db")
        
        # Agent settings
        self.recursion_limit = int(os.getenv("RECURSION_LIMIT", "25"))
        self.temperature = float(os.getenv("TEMPERATURE", "0"))
        
        # Validate configuration
        self._validate()
    
    def _validate(self):
        """Validate configuration"""
        if not self.openai_api_key.startswith("sk-"):
            print("⚠️  Warning: OPENAI_API_KEY not set or invalid")
        
        if not os.path.exists(self.vectordb_path):
            print(f"⚠️  Warning: Vector database not found at {self.vectordb_path}")
            print("💡 Run 'make fetch-data && make ingest' to create it")
    
    def get_nasa_config(self) -> Dict[str, Any]:
        """Get NASA search configuration"""
        return {
            "db_path": self.vectordb_path,
            "model": self.default_model,
            "embedding_model": self.embedding_model
        }
    
    def get_agent_config(self) -> Dict[str, Any]:
        """Get agent configuration"""
        return {
            "model": self.default_model,
            "temperature": self.temperature,
            "recursion_limit": self.recursion_limit,
            "include_mcp": bool(self.mcp_server_urls.strip())
        }
    
    def has_mcp_servers(self) -> bool:
        """Check if MCP servers are configured"""
        return bool(self.mcp_server_urls.strip())
    
    def print_status(self):
        """Print configuration status"""
        print("🔧 Configuration Status:")
        print(f"   OpenAI API Key: {'✅ Set' if self.openai_api_key.startswith('sk-') else '❌ Missing'}")
        print(f"   Vector Database: {'✅ Found' if os.path.exists(self.vectordb_path) else '❌ Missing'}")
        print(f"   MCP Servers: {'✅ Configured' if self.has_mcp_servers() else '⚪ None'}")
        print(f"   Model: {self.default_model}")


# Global configuration instance
_config = None

def get_config() -> AppConfig:
    """Get application configuration - singleton pattern"""
    global _config
    if _config is None:
        _config = AppConfig()
    return _config

def load_environment():
    """Load and validate environment - convenience function"""
    config = get_config()
    config.print_status()
    return config 
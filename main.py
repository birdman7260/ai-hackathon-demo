#!/usr/bin/env python3
"""
NASA Document Q&A System - Simplified Main Application

This is the entry point for the NASA Document Q&A System, which provides
intelligent question-answering capabilities for NASA technical documents.

ARCHITECTURE OVERVIEW:
This application follows a modular, clean architecture pattern:

1. Configuration Layer (common.config): Handles environment setup and validation
2. Data Layer (common.nasa_search): Manages vector database and document retrieval  
3. Integration Layer (common.mcp_client): Handles external MCP server connections
4. Agent Layer (common.agent_factory): Creates and configures AI agents
5. Presentation Layer (this file): Provides user interface and interaction

DESIGN PATTERNS USED:
- Singleton Pattern: For configuration and client instances
- Factory Pattern: For agent creation with different configurations
- Dependency Injection: Components receive their dependencies cleanly
- Strategy Pattern: Different tool sets based on MCP availability
- Command Pattern: User queries processed through agent invocation

FLOW:
User Input → Configuration Loading → Agent Creation → Tool Integration → Response Generation
"""

from langchain_core.messages import HumanMessage
from common import (
    ThinkingSpinner,     # UI component for loading animations
    create_nasa_agent,   # Factory function for creating configured agents
    load_environment     # Configuration loading and validation
)


def main():
    """
    Main application entry point and interaction loop.
    
    This function orchestrates the entire application lifecycle:
    1. Loads and validates configuration from environment
    2. Creates an AI agent with appropriate tools (NASA + MCP)
    3. Runs an interactive question-answering loop
    4. Handles errors gracefully and provides user feedback
    
    ARCHITECTURE DECISIONS:
    - Single responsibility: Only handles user interaction and flow control
    - Dependency injection: Gets all dependencies from common modules
    - Error isolation: Catches and handles errors without crashing
    - User experience: Provides clear feedback and status information
    """
    print("🚀 NASA Document Q&A System")
    print("Ask questions about NASA documents. Type 'quit', 'exit', or 'q' to stop.")
    print("=" * 60)
    
    # CONFIGURATION PHASE
    # Load environment variables, validate settings, and display system status
    # This includes checking for OpenAI API keys, vector database, MCP servers
    config = load_environment()
    agent_config = config.get_agent_config()
    
    # AGENT CREATION PHASE  
    # Create an AI agent with the appropriate tools based on configuration
    # - Always includes NASA document search capability
    # - Conditionally includes MCP filesystem tools if servers are available
    # - Uses environment-specified model (default: gpt-4.1)
    agent = create_nasa_agent(
        include_mcp=agent_config["include_mcp"],  # MCP tools if servers configured
        model=agent_config["model"]               # AI model from environment
    )
    
    print("✅ Agent ready for questions!")
    print()
    
    # UI COMPONENT INITIALIZATION
    # ThinkingSpinner provides visual feedback during AI processing
    # Uses context manager pattern for clean resource management
    spinner = ThinkingSpinner()
    
    # MAIN INTERACTION LOOP
    # Processes user questions in an infinite loop until exit command
    while True:
        try:
            # USER INPUT PHASE
            # Get question from user with clear prompt
            question = input("Ask ▶ ")
            
            # EXIT CONDITION CHECK
            # Support multiple common exit commands for good UX
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            # PROCESSING PHASE
            # Execute AI agent with visual feedback and error boundaries
            with spinner:  # Context manager shows thinking animation
                # AGENT INVOCATION
                # Convert user question to LangChain message format
                # Apply recursion limit to prevent infinite tool loops
                response = agent.invoke(
                    {"messages": [HumanMessage(content=question)]},
                    config={"recursion_limit": agent_config["recursion_limit"]}
                )
            
            # RESPONSE EXTRACTION AND DISPLAY
            # LangGraph agents return complex message structures
            # Extract the final AI response for user display
            if response and "messages" in response and response["messages"]:
                final_message = response["messages"][-1]
                # Validate response has content before displaying
                if hasattr(final_message, 'content') and final_message.content:
                    print("→", final_message.content, "\n")
                else:
                    # Handle edge case where agent doesn't generate content
                    print("→ No answer generated. Please try a different question.\n")
            else:
                # Handle edge case where response structure is unexpected
                print("→ No answer generated. Please try a different question.\n")
                
        except KeyboardInterrupt:
            # GRACEFUL SHUTDOWN
            # Handle Ctrl+C interruption cleanly
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            # ERROR HANDLING
            # Catch all other exceptions to prevent crashes
            # Provide user feedback and troubleshooting hints
            print(f"→ Error: {str(e)}\n")
            print("💡 Tip: Try 'make debug' to check system health")


if __name__ == "__main__":
    """
    Script entry point when run directly.
    
    This ensures main() only runs when the script is executed directly,
    not when imported as a module. This is a Python best practice that
    allows the module to be safely imported for testing or reuse.
    """
    main()
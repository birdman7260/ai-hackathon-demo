#!/usr/bin/env python3
"""
NASA Document Q&A System - Simplified Main Application
A clean, modular implementation using abstracted components
"""

from langchain_core.messages import HumanMessage
from common import (
    ThinkingSpinner,
    create_nasa_agent,
    load_environment,
)


def main():
    """Main application entry point"""
    print("🚀 NASA Document Q&A System")
    print("Ask questions about NASA documents. Type 'quit', 'exit', or 'q' to stop.")
    print("=" * 60)
    
    # Load configuration and show status
    config = load_environment()
    agent_config = config.get_agent_config()
    
    # Create agent with configuration
    agent = create_nasa_agent(
        include_mcp=agent_config["include_mcp"],
        model=agent_config["model"]
    )
    
    print("✅ Agent ready for questions!")
    print()
    
    # Initialize thinking spinner
    spinner = ThinkingSpinner()
    
    # Main interaction loop
    while True:
        try:
            # Get user input
            question = input("Ask ▶ ")
            
            # Check for exit commands
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            # Process question with thinking animation
            with spinner:
                response = agent.invoke(
                    {"messages": [HumanMessage(content=question)]},
                    config={"recursion_limit": agent_config["recursion_limit"]}
                )
            
            # Display response
            if response and "messages" in response and response["messages"]:
                final_message = response["messages"][-1]
                if hasattr(final_message, 'content') and final_message.content:
                    print("→", final_message.content, "\n")
                else:
                    print("→ No answer generated. Please try a different question.\n")
            else:
                print("→ No answer generated. Please try a different question.\n")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"→ Error: {str(e)}\n")
            print("💡 Tip: Try 'make debug' to check system health")


if __name__ == "__main__":
    main()
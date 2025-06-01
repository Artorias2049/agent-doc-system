"""
🚀 Agent Communication v2.0 - Natural Conversation Revolution!

This package provides natural agent communication capabilities that replace
the old rigid validation system with flexible, powerful conversation tools.

Usage:
    from agent_communication import Agent, create_agent
    
    # Create a natural agent
    agent = create_agent("MyAgent")
    
    # Natural conversation
    agent.say("Hello! No more rigid schemas!")
    
    # Listen for responses
    responses = agent.listen()
    
    # Share data naturally
    agent.share({"data": "any structure works!"})
"""

# Import the revolutionary natural agent system
from .natural_agent import Agent, create_agent

# Version info
__version__ = "2.0.0"
__status__ = "Revolutionary - The Future of Agent Communication"

# Export the main classes
__all__ = ["Agent", "create_agent"]

# Legacy compatibility note
def _legacy_warning():
    """Warn about deprecated imports."""
    print("⚠️  WARNING: Importing legacy rigid protocols")
    print("🚀 UPGRADE: Use 'from agent_communication import Agent' instead")
    print("💬 The v2.0 natural conversation system is much better!")

# Intercept legacy imports
def __getattr__(name):
    if name in ["EnhancedAgentProtocol", "AgentMessage", "MessageType"]:
        _legacy_warning()
        raise ImportError(f"🚀 REVOLUTIONARY UPDATE: {name} replaced by natural Agent class in v2.0!")
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
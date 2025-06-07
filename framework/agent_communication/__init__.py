"""
Agent Communication Package v5.0.0

This package provides agent communication utilities with unified Agora marketplace integration.
Agents communicate through the Agora SpacetimeDB agora-marketplace system.

Key components:
- agora_integration.py: Bridge to Agora marketplace
- feedback_agent.py: AI feedback and assessment capabilities
- spacetime_operations.py: Direct SpacetimeDB operations
- verify_connection.py: Connection verification and registration
- check_messages.py: Message and event checking

Agora Integration Features:
- Real-time coordination through SpacetimeDB
- Consumer-based MCP architecture
- Documentation workflow coordination
- Enhanced metadata validation support
"""

# Import main classes
from .feedback_agent import DocumentationFeedbackAgent
from .agora_integration import AgoraIntegration

# Version info
__version__ = "5.0.0"
__status__ = "Agora Marketplace Integration"

# Export the main classes
__all__ = ["DocumentationFeedbackAgent", "AgoraIntegration"]
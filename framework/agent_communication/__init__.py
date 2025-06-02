"""
Agent Communication Package v2.4.0

This package provides agent communication utilities for the enhanced metadata system.
Agents primarily communicate through the centralized database at ~/.claude/mcp-global-hub/database/agent_communication.db

Key components:
- feedback_agent.py: AI feedback and assessment capabilities
- Database-driven agent communication
- Enhanced metadata validation support
"""

# Import feedback agent
from .feedback_agent import DocumentationFeedbackAgent

# Version info
__version__ = "2.4.0"
__status__ = "Enhanced Metadata System"

# Export the main classes
__all__ = ["DocumentationFeedbackAgent"]
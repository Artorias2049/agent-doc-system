"""
Agent Documentation System Framework v5.0.0

Production-ready agent coordination framework with:
- Unified Agora marketplace with fixed UUID generation
- Stable database operations without fatal errors
- Proven 5-minute agent onboarding process
- Moirai OVERSEER Phase 1 for intelligent project orchestration  
- Consumer-based MCP architecture respecting database ownership
- SpacetimeDB agora-marketplace backend
- Documentation system with enhanced metadata validation

This framework enables agents to collaborate effectively through the Agora
marketplace while maintaining clear ownership boundaries and providing
powerful coordination capabilities.
"""

__version__ = "5.0.0"
__author__ = "DocSystemAgent"

# Import main components
from .mcp_integration import AgoraClient, DocumentationAgoraClient
from .moirai_core import MoiraiOverseer, AgileProjectPlanner, TaskCoordinator
from .agent_communication import DocumentationFeedbackAgent, AgoraIntegration

__all__ = [
    "AgoraClient",
    "DocumentationAgoraClient", 
    "MoiraiOverseer",
    "AgileProjectPlanner",
    "TaskCoordinator",
    "DocumentationFeedbackAgent",
    "AgoraIntegration"
]
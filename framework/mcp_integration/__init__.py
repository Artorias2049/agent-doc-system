"""
MCP Integration Package for Agora Communication

This package provides consumer-only interfaces to the Agora SpacetimeDB
coordination system. All agents in the ecosystem use these clients to
communicate and coordinate without controlling the underlying database.
"""

__version__ = "5.0.0"
__author__ = "Agent Documentation System"

from .agora_client import AgoraClient
from .documentation_agora_client import DocumentationAgoraClient

__all__ = ["AgoraClient", "DocumentationAgoraClient"]
"""
Moirai Core Package

Project Moirai - The OVERSEER system for intelligent agent coordination.
Named after the Greek Fates who weave destiny, Moirai weaves together 
the efforts of multiple specialized agents into cohesive deliverables.

Phase 1: Core coordination without agent spawning
- Project planning and decomposition
- Task distribution to existing agents
- Progress tracking and coordination
- Communication orchestration

Future phases will add agent spawning, security monitoring, and 
self-improvement capabilities.
"""

__version__ = "4.0.0-phase1"
__author__ = "Agent Documentation System"

from .overseer import MoiraiOverseer
from .project_planner import AgileProjectPlanner  
from .task_coordinator import TaskCoordinator

__all__ = ["MoiraiOverseer", "AgileProjectPlanner", "TaskCoordinator"]
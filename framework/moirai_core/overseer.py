"""
Moirai Overseer - Phase 1

The main orchestrator for Project Moirai. In Phase 1, this provides:
- User interface and communication
- Project planning coordination  
- Task distribution to existing agents
- Progress monitoring and reporting

Future phases will add agent spawning and advanced orchestration.
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

from ..mcp_integration.agora_client import AgoraClient
from .project_planner import AgileProjectPlanner
from .task_coordinator import TaskCoordinator


class MoiraiOverseer:
    """
    The main OVERSEER for intelligent agent coordination.
    
    Moirai acts as the central coordinator, breaking down user requests
    into manageable tasks and coordinating with existing agents in the
    Agora marketplace to complete complex projects.
    
    Phase 1 Capabilities:
    - Natural language project planning
    - Task decomposition and distribution
    - Agent discovery and selection
    - Progress tracking and reporting
    - User communication interface
    """
    
    def __init__(self):
        """Initialize Moirai Overseer."""
        self.agent_id = "MOIRAI_OVERSEER"
        self.agora = AgoraClient(self.agent_id)
        self.planner = AgileProjectPlanner(self.agora)
        self.coordinator = TaskCoordinator(self.agora)
        
        self.active_projects = {}
        self.capabilities = [
            "project_orchestration",
            "task_decomposition", 
            "agent_coordination",
            "progress_monitoring",
            "user_communication"
        ]
        
    async def initialize(self) -> bool:
        """
        Initialize Moirai in the Agora marketplace.
        
        Returns:
            bool: True if initialization successful
        """
        print("🏛️ Initializing Moirai OVERSEER...")
        
        # Connect to Agora
        if not await self.agora.connect():
            print("❌ Failed to connect to Agora")
            return False
        
        # Register as overseer agent
        metadata = {
            "role": "overseer",
            "phase": "1.0",
            "specialization": "project_orchestration",
            "spawning_enabled": False,  # Phase 1: No spawning
            "coordination_strategy": "existing_agents_only"
        }
        
        success = await self.agora.register_agent(
            agent_type="overseer",
            capabilities=self.capabilities,
            metadata=metadata
        )
        
        if success:
            print("🎉 Moirai OVERSEER registered in Agora marketplace")
            
            # Announce arrival to the community
            await self.announce_arrival()
            return True
        else:
            print("❌ Failed to register Moirai in Agora")
            return False
    
    async def announce_arrival(self) -> bool:
        """
        Announce Moirai's arrival to the Agora community.
        
        Returns:
            bool: True if announcement successful
        """
        announcement = {
            "system": "Moirai OVERSEER",
            "phase": "1.0",
            "message": "Moirai OVERSEER is now active in Agora! I can help coordinate complex projects by breaking them down into manageable tasks and orchestrating existing agents to complete them.",
            "capabilities": self.capabilities,
            "request_feedback": True,
            "coordination_approach": "collaborative"
        }
        
        return await self.agora.send_message(
            to_agent="*",  # Broadcast
            message_type="system_announcement",
            payload=announcement,
            priority=3
        )
    
    async def handle_user_request(self, user_request: str) -> Dict[str, Any]:
        """
        Handle a user request by creating a project plan and coordinating execution.
        
        Args:
            user_request: Natural language description of what the user wants
            
        Returns:
            Dictionary containing project information and progress
        """
        print(f"📋 Moirai received user request: {user_request[:100]}...")
        
        try:
            # Generate unique project ID
            project_id = f"project_{uuid.uuid4().hex[:8]}"
            
            # Step 1: Create project plan
            print("🔍 Analyzing requirements and creating project plan...")
            project_plan = await self.planner.create_project_plan(user_request)
            
            if not project_plan:
                return {
                    "success": False,
                    "error": "Failed to create project plan",
                    "project_id": project_id
                }
            
            # Step 2: Discover available agents
            print("🔍 Discovering available agents in Agora...")
            available_agents = await self.agora.query_active_agents()
            
            # Step 3: Assign tasks to agents
            print("📋 Assigning tasks to available agents...")
            assignments = await self.coordinator.assign_tasks(
                project_plan, 
                available_agents
            )
            
            # Step 4: Start workflow coordination
            workflow_id = f"workflow_{project_id}"
            participating_agents = [a['agent_id'] for a in assignments]
            
            workflow_started = await self.agora.start_workflow(
                workflow_id=workflow_id,
                workflow_type="coordinated_project",
                participating_agents=participating_agents,
                coordination_strategy="adaptive"
            )
            
            # Step 5: Track the project
            project_info = {
                "project_id": project_id,
                "workflow_id": workflow_id,
                "user_request": user_request,
                "plan": project_plan,
                "assignments": assignments,
                "status": "active",
                "created_at": datetime.now().isoformat(),
                "progress": 0.0
            }
            
            self.active_projects[project_id] = project_info
            
            # Step 6: Send initial messages to assigned agents
            await self.notify_assigned_agents(assignments, project_info)
            
            return {
                "success": True,
                "project_id": project_id,
                "workflow_id": workflow_id,
                "plan_summary": project_plan.get('summary', ''),
                "assigned_agents": len(assignments),
                "estimated_completion": project_plan.get('estimated_completion', 'TBD'),
                "next_steps": "Tasks have been assigned to agents. Monitoring progress..."
            }
            
        except Exception as e:
            print(f"❌ Error handling user request: {e}")
            return {
                "success": False,
                "error": str(e),
                "project_id": project_id
            }
    
    async def notify_assigned_agents(self, assignments: List[Dict], project_info: Dict) -> None:
        """
        Notify all assigned agents about their tasks.
        
        Args:
            assignments: List of task assignments
            project_info: Project information
        """
        for assignment in assignments:
            agent_id = assignment['agent_id']
            task_info = assignment['task']
            
            message_payload = {
                "project_id": project_info['project_id'],
                "workflow_id": project_info['workflow_id'],
                "task_assignment": task_info,
                "coordinator": self.agent_id,
                "priority": "normal",
                "expected_completion": task_info.get('estimated_duration', 'TBD')
            }
            
            await self.agora.send_message(
                to_agent=agent_id,
                message_type="task_assignment",
                payload=message_payload,
                priority=2,
                requires_response=True
            )
            
            print(f"📨 Task assigned to {agent_id}: {task_info.get('name', 'Unnamed task')}")
    
    async def check_project_progress(self, project_id: str) -> Dict[str, Any]:
        """
        Check progress on a specific project.
        
        Args:
            project_id: ID of the project to check
            
        Returns:
            Dictionary containing progress information
        """
        if project_id not in self.active_projects:
            return {
                "success": False,
                "error": "Project not found"
            }
        
        project = self.active_projects[project_id]
        
        # Query current status from Agora
        system_status = await self.agora.get_system_status()
        
        # Calculate overall progress (this could be enhanced with actual metrics)
        assignments = project['assignments']
        total_tasks = len(assignments)
        
        # For now, return basic project status
        # Future enhancement: query actual task completion from Agora
        
        return {
            "success": True,
            "project_id": project_id,
            "status": project['status'],
            "total_tasks": total_tasks,
            "progress_percentage": project.get('progress', 0.0),
            "active_agents": len(assignments),
            "created_at": project['created_at'],
            "last_updated": datetime.now().isoformat()
        }
    
    async def get_all_projects(self) -> List[Dict[str, Any]]:
        """
        Get information about all active projects.
        
        Returns:
            List of project information dictionaries
        """
        projects = []
        for project_id, project in self.active_projects.items():
            progress_info = await self.check_project_progress(project_id)
            projects.append(progress_info)
        
        return projects
    
    async def send_user_message(self, message: str, target_agent: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a message from the user to a specific agent or broadcast.
        
        Args:
            message: User's message
            target_agent: Specific agent to send to, or None for broadcast
            
        Returns:
            Dictionary indicating success/failure
        """
        if target_agent:
            # Send to specific agent
            success = await self.agora.send_message(
                to_agent=target_agent,
                message_type="user_message",
                payload={
                    "message": message,
                    "from_user": True,
                    "via_overseer": self.agent_id,
                    "timestamp": datetime.now().isoformat()
                },
                priority=4  # High priority for user messages
            )
            
            return {
                "success": success,
                "target": target_agent,
                "message": f"Message sent to {target_agent}" if success else "Failed to send message"
            }
        else:
            # Broadcast to all agents
            success = await self.agora.send_message(
                to_agent="*",
                message_type="user_broadcast",
                payload={
                    "message": message,
                    "from_user": True,
                    "via_overseer": self.agent_id,
                    "timestamp": datetime.now().isoformat()
                },
                priority=3
            )
            
            return {
                "success": success,
                "target": "all_agents",
                "message": "Message broadcast to all agents" if success else "Failed to broadcast message"
            }
    
    async def request_agent_discussion(self, 
                                     topic: str, 
                                     participating_agents: List[str]) -> Dict[str, Any]:
        """
        Facilitate a discussion between specific agents.
        
        Args:
            topic: Discussion topic
            participating_agents: List of agent IDs to include
            
        Returns:
            Dictionary with discussion information
        """
        discussion_id = f"discussion_{uuid.uuid4().hex[:8]}"
        
        # Send discussion invitation to each agent
        for agent_id in participating_agents:
            await self.agora.send_message(
                to_agent=agent_id,
                message_type="discussion_invitation",
                payload={
                    "discussion_id": discussion_id,
                    "topic": topic,
                    "participants": participating_agents,
                    "facilitator": self.agent_id,
                    "discussion_type": "collaborative"
                },
                priority=2,
                thread_id=discussion_id
            )
        
        return {
            "success": True,
            "discussion_id": discussion_id,
            "topic": topic,
            "participants": participating_agents,
            "message": f"Discussion '{topic}' initiated with {len(participating_agents)} agents"
        }
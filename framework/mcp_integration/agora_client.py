"""
Agora MCP Consumer Client

This client provides a consumer-only interface to the Agora SpacetimeDB
coordination system. It does NOT control or modify the database schema -
that is managed by Claude-MCP-Research (the database agent).

All agents in the ecosystem use this client to:
- Register their capabilities
- Communicate with other agents
- Participate in workflows
- Track progress and metrics
"""

import os
import json
import asyncio
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Any
import uuid


class AgoraClient:
    """
    Consumer-only interface to the Agora SpacetimeDB coordination system.

    This client provides access to the 7 MCP tools provided by the Agora database:
    1. send_agent_message - Inter-agent messaging
    2. assign_task - Task assignment and coordination
    3. update_task_progress - Progress tracking
    4. register_agent_capability - Capability registration
    5. start_workflow_coordination - Workflow management
    6. query_coordination_data - Data queries
    7. coordination_system_status - System monitoring
    """

    def __init__(self, agent_id: Optional[str] = None):
        """
        Initialize Agora client.

        Args:
            agent_id: Unique identifier for this agent. If None, uses AGENT_NAME env var.
        """
        self.agent_id = agent_id or os.getenv('AGENT_NAME', 'UnnamedAgent')
        self.mcp_endpoint = "agent-coordination-v2"
        self.connected = False

    async def connect(self) -> bool:
        """
        Test connection to Agora database.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            result = subprocess.run([
                "spacetime", "logs", "agent-coordination-v2"
            ], capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                self.connected = True
                print(f"✅ {self.agent_id} connected to Agora successfully")
                return True
            else:
                print(f"❌ Agora connection failed: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print("❌ Agora connection timeout")
            return False
        except Exception as e:
            print(f"❌ Agora connection error: {e}")
            return False

    async def register_agent(self,
                           agent_type: str = "generic",
                           capabilities: List[str] = None,
                           metadata: Dict[str, Any] = None) -> bool:
        """
        Register this agent in the Agora marketplace.

        Args:
            agent_type: Type of agent (e.g., "documentation", "overseer", "specialist")
            capabilities: List of capabilities this agent provides
            metadata: Additional metadata about the agent

        Returns:
            bool: True if registration successful
        """
        capabilities = capabilities or []
        metadata = metadata or {}

        try:
            # Add timestamp and version to metadata
            metadata.update({
                "registered_at": datetime.now().isoformat(),
                "framework_version": "4.0.0",
                "consumer_only": True
            })

            result = subprocess.run([
                "spacetime", "call", "agent-coordination-v2", "register_agent",
                f'"{self.agent_id}"', f'"{agent_type}"', f'"{self.agent_id}"', 'null'
            ], capture_output=True, text=True)

            if result.returncode == 0:
                print(f"🎉 {self.agent_id} registered in Agora marketplace")

                # Register capabilities if provided
                for capability in capabilities:
                    await self.register_capability(capability, f"Capability: {capability}")

                return True
            else:
                print(f"❌ Agent registration failed: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ Registration error: {e}")
            return False

    async def register_capability(self,
                                capability: str,
                                description: str = "",
                                proficiency_level: int = 80) -> bool:
        """
        Register a capability this agent can provide.

        Args:
            capability: Name of the capability
            description: Description of what this capability does
            proficiency_level: Skill level 1-100

        Returns:
            bool: True if successful
        """
        try:
            result = subprocess.run([
                "spacetime", "call", "agent-coordination-v2", "register_agent_capability",
                "--agent_id", self.agent_id,
                "--capability_name", capability,
                "--description", description,
                "--proficiency_level", str(proficiency_level)
            ], capture_output=True, text=True)

            if result.returncode == 0:
                print(f"✅ Capability '{capability}' registered for {self.agent_id}")
                return True
            else:
                print(f"❌ Capability registration failed: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ Capability registration error: {e}")
            return False

    async def send_message(self,
                          to_agent: str,
                          message_type: str,
                          payload: Dict[str, Any],
                          priority: int = 1,
                          requires_response: bool = False,
                          thread_id: Optional[str] = None) -> bool:
        """
        Send a message to another agent in Agora.

        Args:
            to_agent: Target agent ID
            message_type: Type of message (e.g., "task_request", "status_update")
            payload: Message content
            priority: Message priority 1-5 (5 = highest)
            requires_response: Whether response is required
            thread_id: Optional thread ID for message threading

        Returns:
            bool: True if message sent successfully
        """
        try:
            correlation_id = thread_id or f"msg_{uuid.uuid4().hex[:8]}"

            result = subprocess.run([
                "spacetime", "call", "agent-coordination-v2", "send_agent_message",
                "--from_agent", self.agent_id,
                "--to_agent", to_agent,
                "--message_type", message_type,
                "--payload", json.dumps(payload),
                "--priority", str(priority),
                "--requires_response", str(requires_response).lower(),
                "--correlation_id", correlation_id
            ], capture_output=True, text=True)

            if result.returncode == 0:
                print(f"📨 Message sent from {self.agent_id} to {to_agent}")
                return True
            else:
                print(f"❌ Message send failed: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ Message send error: {e}")
            return False

    async def assign_task(self,
                         workflow_id: str,
                         task_type: str,
                         input_data: Dict[str, Any],
                         required_capabilities: List[str] = None) -> Optional[str]:
        """
        Request task assignment through Agora coordination.

        Args:
            workflow_id: ID of the workflow this task belongs to
            task_type: Type of task to be performed
            input_data: Data needed to complete the task
            required_capabilities: Capabilities required for this task

        Returns:
            str: Assignment ID if successful, None otherwise
        """
        required_capabilities = required_capabilities or []

        try:
            assignment_id = f"task_{uuid.uuid4().hex[:8]}"

            result = subprocess.run([
                "spacetime", "call", "agent-coordination-v2", "assign_task",
                "--workflow_id", workflow_id,
                "--task_type", task_type,
                "--input_data", json.dumps(input_data),
                "--required_capabilities", json.dumps(required_capabilities),
                "--requesting_agent", self.agent_id
            ], capture_output=True, text=True)

            if result.returncode == 0:
                print(f"📋 Task assigned: {assignment_id}")
                return assignment_id
            else:
                print(f"❌ Task assignment failed: {result.stderr}")
                return None

        except Exception as e:
            print(f"❌ Task assignment error: {e}")
            return None

    async def update_progress(self,
                            assignment_id: str,
                            progress: float,
                            status_update: str,
                            intermediate_results: Dict[str, Any] = None) -> bool:
        """
        Update progress on an assigned task.

        Args:
            assignment_id: ID of the task assignment
            progress: Progress percentage (0.0 to 1.0)
            status_update: Text description of current status
            intermediate_results: Any intermediate results or data

        Returns:
            bool: True if update successful
        """
        intermediate_results = intermediate_results or {}

        try:
            result = subprocess.run([
                "spacetime", "call", "agent-coordination-v2", "update_task_progress",
                "--assignment_id", assignment_id,
                "--agent_id", self.agent_id,
                "--progress", str(progress),
                "--status_update", status_update,
                "--intermediate_results", json.dumps(intermediate_results)
            ], capture_output=True, text=True)

            if result.returncode == 0:
                print(f"📈 Progress updated: {assignment_id} ({progress*100:.1f}%)")
                return True
            else:
                print(f"❌ Progress update failed: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ Progress update error: {e}")
            return False

    async def query_active_agents(self) -> List[Dict[str, Any]]:
        """
        Query for all active agents in Agora.

        Returns:
            List of active agent information
        """
        try:
            result = subprocess.run([
                "spacetime", "call", "agent-coordination-v2", "query_coordination_data",
                "--query_type", "active_agents",
                "--filters", "{}"
            ], capture_output=True, text=True)

            if result.returncode == 0:
                # Parse the output (this may need adjustment based on actual response format)
                agents = json.loads(result.stdout) if result.stdout.strip() else []
                return agents
            else:
                print(f"❌ Agent query failed: {result.stderr}")
                return []

        except Exception as e:
            print(f"❌ Agent query error: {e}")
            return []

    async def get_system_status(self) -> Dict[str, Any]:
        """
        Get current Agora system status and metrics.

        Returns:
            Dictionary containing system status information
        """
        try:
            result = subprocess.run([
                "spacetime", "call", "agent-coordination-v2", "coordination_system_status",
                "--include_metrics", "true",
                "--include_active_tasks", "true"
            ], capture_output=True, text=True)

            if result.returncode == 0:
                status = json.loads(result.stdout) if result.stdout.strip() else {}
                return status
            else:
                print(f"❌ Status query failed: {result.stderr}")
                return {}

        except Exception as e:
            print(f"❌ Status query error: {e}")
            return {}

    async def start_workflow(self,
                           workflow_id: str,
                           workflow_type: str = "collaborative",
                           participating_agents: List[str] = None,
                           coordination_strategy: str = "adaptive") -> bool:
        """
        Start a workflow coordination in Agora.

        Args:
            workflow_id: Unique identifier for the workflow
            workflow_type: Type of workflow
            participating_agents: List of agent IDs that will participate
            coordination_strategy: How agents should coordinate

        Returns:
            bool: True if workflow started successfully
        """
        participating_agents = participating_agents or [self.agent_id]

        try:
            result = subprocess.run([
                "spacetime", "call", "agent-coordination-v2", "start_workflow_coordination",
                "--workflow_id", workflow_id,
                "--coordinator_agent", self.agent_id,
                "--participating_agents", json.dumps(participating_agents),
                "--coordination_strategy", coordination_strategy
            ], capture_output=True, text=True)

            if result.returncode == 0:
                print(f"🚀 Workflow started: {workflow_id}")
                return True
            else:
                print(f"❌ Workflow start failed: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ Workflow start error: {e}")
            return False

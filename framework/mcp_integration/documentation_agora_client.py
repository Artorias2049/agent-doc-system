"""
Documentation System Agora Client

Specialized Agora client for documentation system agents.
Provides domain-specific methods for documentation tasks while
consuming the Agora coordination services.
"""

import os
import json
from typing import Dict, List, Optional, Any
from .agora_client import AgoraClient


class DocumentationAgoraClient(AgoraClient):
    """
    Specialized Agora client for documentation system operations.

    This client extends the base AgoraClient with documentation-specific
    capabilities and workflows while maintaining the consumer-only pattern.
    """

    def __init__(self, agent_id: Optional[str] = None):
        """Initialize documentation-specific Agora client."""
        super().__init__(agent_id)
        self.capabilities = [
            "documentation_creation",
            "protocol_validation",
            "template_generation",
            "metadata_enhancement",
            "quality_assessment",
            "schema_validation"
        ]

    async def register_documentation_agent(self) -> bool:
        """
        Register this agent as a documentation specialist in Agora.

        Returns:
            bool: True if registration successful
        """
        metadata = {
            "domain": "documentation",
            "framework_version": "5.0.0",
            "protocol_compliance": "THE_PROTOCOL_v5.0",
            "specialization": "documentation_system",
            "template_support": True,
            "validation_support": True,
            "ai_feedback_support": True
        }

        success = await self.register_agent(
            agent_type="documentation",
            capabilities=self.capabilities,
            metadata=metadata
        )

        if success:
            print(f"📚 {self.agent_id} registered as documentation specialist")

        return success

    async def announce_documentation_capability(self,
                                              capability: str,
                                              description: str,
                                              proficiency: int = 90) -> bool:
        """
        Announce a specific documentation capability to the Agora marketplace.

        Args:
            capability: Name of the documentation capability
            description: Description of what this capability provides
            proficiency: Proficiency level (1-100)

        Returns:
            bool: True if announcement successful
        """
        success = await self.register_capability(capability, description, proficiency)

        if success:
            # Also send announcement message to all agents
            await self.send_message(
                to_agent="*",  # Broadcast
                message_type="capability_announcement",
                payload={
                    "capability": capability,
                    "description": description,
                    "proficiency": proficiency,
                    "domain": "documentation",
                    "available_immediately": True
                },
                priority=2
            )

        return success

    async def request_documentation_task(self,
                                       task_description: str,
                                       document_type: str,
                                       requirements: Dict[str, Any] = None) -> Optional[str]:
        """
        Request a documentation task assignment through Agora.

        Args:
            task_description: Description of the documentation needed
            document_type: Type of document (e.g., "api", "component", "project")
            requirements: Specific requirements for the documentation

        Returns:
            str: Assignment ID if successful
        """
        requirements = requirements or {}

        workflow_id = f"doc_{document_type}_{hash(task_description) % 10000}"

        input_data = {
            "description": task_description,
            "document_type": document_type,
            "requirements": requirements,
            "template_needed": True,
            "validation_required": True,
            "ai_feedback_requested": True
        }

        return await self.assign_task(
            workflow_id=workflow_id,
            task_type="documentation_creation",
            input_data=input_data,
            required_capabilities=["documentation_creation", "protocol_validation"]
        )

    async def update_documentation_progress(self,
                                          assignment_id: str,
                                          stage: str,
                                          progress: float,
                                          validation_status: str = "pending",
                                          quality_score: Optional[int] = None) -> bool:
        """
        Update progress on a documentation task with domain-specific information.

        Args:
            assignment_id: Task assignment ID
            stage: Current stage (e.g., "planning", "writing", "validating", "complete")
            progress: Progress percentage (0.0 to 1.0)
            validation_status: Status of validation ("pending", "passed", "failed")
            quality_score: Quality assessment score (1-100)

        Returns:
            bool: True if update successful
        """
        intermediate_results = {
            "stage": stage,
            "validation_status": validation_status,
            "protocol_compliance": "THE_PROTOCOL_v4.0"
        }

        if quality_score is not None:
            intermediate_results["quality_score"] = quality_score

        status_update = f"Documentation {stage} - {progress*100:.1f}% complete"

        return await self.update_progress(
            assignment_id=assignment_id,
            progress=progress,
            status_update=status_update,
            intermediate_results=intermediate_results
        )

    async def request_peer_review(self,
                                document_path: str,
                                review_type: str = "quality") -> Optional[str]:
        """
        Request peer review of a document through Agora.

        Args:
            document_path: Path to the document needing review
            review_type: Type of review ("quality", "technical", "compliance")

        Returns:
            str: Review request ID if successful
        """
        workflow_id = f"review_{review_type}_{hash(document_path) % 10000}"

        input_data = {
            "document_path": document_path,
            "review_type": review_type,
            "requester": self.agent_id,
            "urgency": "normal"
        }

        # Look for agents with review capabilities
        assignment_id = await self.assign_task(
            workflow_id=workflow_id,
            task_type="document_review",
            input_data=input_data,
            required_capabilities=["document_review", review_type]
        )

        if assignment_id:
            print(f"📋 Review requested for {document_path}")

        return assignment_id

    async def share_template(self,
                           template_name: str,
                           template_path: str,
                           template_type: str,
                           description: str) -> bool:
        """
        Share a documentation template with the Agora community.

        Args:
            template_name: Name of the template
            template_path: Path to the template file
            template_type: Type of template ("project", "component", "api")
            description: Description of the template

        Returns:
            bool: True if sharing successful
        """
        return await self.send_message(
            to_agent="*",  # Broadcast to all agents
            message_type="template_sharing",
            payload={
                "template_name": template_name,
                "template_path": template_path,
                "template_type": template_type,
                "description": description,
                "shared_by": self.agent_id,
                "framework_version": "5.0.0"
            },
            priority=1
        )

    async def request_ai_feedback(self,
                                document_path: str,
                                feedback_type: str = "comprehensive") -> Optional[str]:
        """
        Request AI feedback on a document through Agora.

        Args:
            document_path: Path to document needing feedback
            feedback_type: Type of feedback ("comprehensive", "quality", "suggestions")

        Returns:
            str: Feedback request ID if successful
        """
        workflow_id = f"ai_feedback_{feedback_type}_{hash(document_path) % 10000}"

        input_data = {
            "document_path": document_path,
            "feedback_type": feedback_type,
            "requester": self.agent_id,
            "enhanced_validation": True
        }

        return await self.assign_task(
            workflow_id=workflow_id,
            task_type="ai_feedback_generation",
            input_data=input_data,
            required_capabilities=["ai_feedback", "quality_assessment"]
        )

    async def find_documentation_helpers(self,
                                       task_type: str) -> List[Dict[str, Any]]:
        """
        Find other agents who can help with documentation tasks.

        Args:
            task_type: Type of documentation task needing help

        Returns:
            List of agents capable of helping
        """
        all_agents = await self.query_active_agents()

        # Filter for agents with relevant capabilities
        helpers = []
        for agent in all_agents:
            agent_capabilities = agent.get('capabilities', [])
            if any(cap in ['documentation_creation', 'template_generation',
                          'quality_assessment', 'ai_feedback'] for cap in agent_capabilities):
                helpers.append(agent)

        return helpers

    async def start_documentation_workflow(self,
                                         project_name: str,
                                         document_types: List[str],
                                         collaborators: List[str] = None) -> bool:
        """
        Start a collaborative documentation workflow.

        Args:
            project_name: Name of the project being documented
            document_types: Types of documents needed
            collaborators: List of agent IDs to collaborate with

        Returns:
            bool: True if workflow started successfully
        """
        workflow_id = f"docs_{project_name}_{hash(''.join(document_types)) % 10000}"

        collaborators = collaborators or []
        participating_agents = [self.agent_id] + collaborators

        # Start the workflow
        success = await self.start_workflow(
            workflow_id=workflow_id,
            workflow_type="documentation",
            participating_agents=participating_agents,
            coordination_strategy="collaborative"
        )

        if success:
            # Send workflow invitation to all participants
            for agent_id in collaborators:
                await self.send_message(
                    to_agent=agent_id,
                    message_type="workflow_invitation",
                    payload={
                        "workflow_id": workflow_id,
                        "project_name": project_name,
                        "document_types": document_types,
                        "coordinator": self.agent_id,
                        "role": "collaborator"
                    },
                    priority=3,
                    requires_response=True
                )

        return success

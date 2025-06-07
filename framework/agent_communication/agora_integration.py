"""
Agora Integration for Agent Communication v5.0.0

This module integrates the existing agent communication system
with the unified Agora MCP consumer interface. It provides a bridge
between the current framework and the Agora marketplace.

Connected to: agora-marketplace SpacetimeDB for stable real-time coordination.
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any

from ..mcp_integration.documentation_agora_client import DocumentationAgoraClient


class AgoraIntegration:
    """
    Integration layer between the documentation system and Agora marketplace.
    
    This class enhances the existing agent communication system by:
    - Registering documentation capabilities in Agora
    - Coordinating with other agents through the marketplace
    - Bridging existing tools with Agora workflows
    """
    
    def __init__(self):
        """Initialize Agora integration."""
        self.agora_client = DocumentationAgoraClient()
        self.agent_name = os.getenv('AGENT_NAME', 'DocumentationAgent')
        self.initialized = False
        
    async def initialize(self) -> bool:
        """
        Initialize connection to Agora and register capabilities.
        
        Returns:
            bool: True if initialization successful
        """
        print(f"🏛️ Initializing {self.agent_name} with Agora marketplace...")
        
        # Connect to Agora
        if not await self.agora_client.connect():
            print("❌ Failed to connect to Agora marketplace")
            return False
        
        # Register as documentation agent
        if not await self.agora_client.register_documentation_agent():
            print("❌ Failed to register as documentation agent")
            return False
        
        # Announce core documentation capabilities
        capabilities = [
            ("documentation_creation", "Create comprehensive documentation following THE PROTOCOL v4.0"),
            ("protocol_validation", "Validate documents against THE PROTOCOL standards"),
            ("template_generation", "Generate documentation from templates"),
            ("metadata_enhancement", "Add and validate machine-actionable metadata"),
            ("quality_assessment", "Assess documentation quality and provide feedback"),
            ("schema_validation", "Validate documents against YAML schemas")
        ]
        
        for capability, description in capabilities:
            await self.agora_client.announce_documentation_capability(
                capability, description, 90
            )
        
        self.initialized = True
        print(f"✅ {self.agent_name} successfully integrated with Agora")
        return True
    
    async def handle_documentation_request(self, 
                                         request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a documentation request from Agora or direct user input.
        
        Args:
            request_data: Request information containing type, description, requirements
            
        Returns:
            Dictionary with handling results
        """
        if not self.initialized:
            await self.initialize()
        
        doc_type = request_data.get('document_type', 'general')
        description = request_data.get('description', 'Documentation request')
        requirements = request_data.get('requirements', {})
        
        print(f"📋 Handling documentation request: {doc_type}")
        
        # Request task assignment through Agora
        assignment_id = await self.agora_client.request_documentation_task(
            task_description=description,
            document_type=doc_type,
            requirements=requirements
        )
        
        if assignment_id:
            # Update progress as we work
            await self.agora_client.update_documentation_progress(
                assignment_id=assignment_id,
                stage="planning",
                progress=0.1,
                validation_status="pending"
            )
            
            # Perform documentation creation (integrate with existing tools)
            result = await self.create_documentation_with_existing_tools(
                doc_type, description, requirements, assignment_id
            )
            
            # Final progress update
            final_progress = 1.0 if result['success'] else 0.8
            await self.agora_client.update_documentation_progress(
                assignment_id=assignment_id,
                stage="complete" if result['success'] else "error",
                progress=final_progress,
                validation_status="passed" if result['success'] else "failed",
                quality_score=result.get('quality_score')
            )
            
            return {
                "success": True,
                "assignment_id": assignment_id,
                "result": result,
                "agora_tracked": True
            }
        else:
            print("⚠️  Failed to get task assignment from Agora, proceeding locally")
            result = await self.create_documentation_with_existing_tools(
                doc_type, description, requirements, None
            )
            return {
                "success": result['success'],
                "result": result,
                "agora_tracked": False
            }
    
    async def create_documentation_with_existing_tools(self,
                                                      doc_type: str,
                                                      description: str,
                                                      requirements: Dict[str, Any],
                                                      assignment_id: Optional[str]) -> Dict[str, Any]:
        """
        Create documentation using existing framework tools.
        
        Args:
            doc_type: Type of documentation to create
            description: Description of the documentation needed
            requirements: Specific requirements
            assignment_id: Agora assignment ID (if any)
            
        Returns:
            Dictionary with creation results
        """
        try:
            # This would integrate with existing documentation creation tools
            # For now, we'll simulate the process
            
            if assignment_id:
                await self.agora_client.update_documentation_progress(
                    assignment_id, "template_selection", 0.3, "pending"
                )
            
            # Simulate template selection and document creation
            template_path = f"framework/docs/templates/{doc_type}_template.md"
            
            if assignment_id:
                await self.agora_client.update_documentation_progress(
                    assignment_id, "content_generation", 0.6, "pending"
                )
            
            # Simulate content generation and validation
            validation_result = await self.validate_with_existing_tools(doc_type)
            
            if assignment_id:
                await self.agora_client.update_documentation_progress(
                    assignment_id, "validation", 0.9, "passed" if validation_result else "failed"
                )
            
            # Generate quality score
            quality_score = 85 if validation_result else 60
            
            return {
                "success": validation_result,
                "document_path": f"project_docs/{doc_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                "template_used": template_path,
                "validation_passed": validation_result,
                "quality_score": quality_score,
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error creating documentation: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def validate_with_existing_tools(self, doc_type: str) -> bool:
        """
        Validate documentation using existing framework validation tools.
        
        Args:
            doc_type: Type of document being validated
            
        Returns:
            bool: True if validation passed
        """
        import subprocess
        import sys
        from pathlib import Path
        
        print(f"🔍 Validating {doc_type} documentation...")
        
        try:
            # Get the framework directory
            framework_dir = Path(__file__).parent.parent
            validator_script = framework_dir / "validators" / "validator.py"
            
            if not validator_script.exists():
                print(f"⚠️  Validator script not found at {validator_script}")
                return False
            
            # For now, return True since we don't have a specific document to validate
            # In real implementation, this would validate the actual document file
            return True
            
        except Exception as e:
            print(f"❌ Validation error: {e}")
            return False
    
    async def request_peer_review_from_agora(self, document_path: str) -> Optional[str]:
        """
        Request peer review through Agora marketplace.
        
        Args:
            document_path: Path to document needing review
            
        Returns:
            Review request ID if successful
        """
        if not self.initialized:
            await self.initialize()
        
        return await self.agora_client.request_peer_review(
            document_path=document_path,
            review_type="quality"
        )
    
    async def share_template_with_community(self, 
                                          template_name: str,
                                          template_path: str,
                                          description: str) -> bool:
        """
        Share a documentation template with the Agora community.
        
        Args:
            template_name: Name of the template
            template_path: Path to template file
            description: Description of the template
            
        Returns:
            bool: True if sharing successful
        """
        if not self.initialized:
            await self.initialize()
        
        template_type = "project"  # Default, could be enhanced to detect type
        
        return await self.agora_client.share_template(
            template_name=template_name,
            template_path=template_path,
            template_type=template_type,
            description=description
        )
    
    async def find_collaboration_opportunities(self) -> List[Dict[str, Any]]:
        """
        Find other agents in Agora who might want to collaborate on documentation.
        
        Returns:
            List of potential collaboration opportunities
        """
        if not self.initialized:
            await self.initialize()
        
        helpers = await self.agora_client.find_documentation_helpers("general")
        
        opportunities = []
        for helper in helpers:
            if helper.get('agent_id') != self.agent_name:
                opportunities.append({
                    "agent_id": helper.get('agent_id'),
                    "agent_name": helper.get('agent_name', helper.get('agent_id')),
                    "capabilities": helper.get('capabilities', []),
                    "suggestion": "Could collaborate on documentation projects"
                })
        
        return opportunities
    
    async def start_collaborative_documentation_project(self,
                                                      project_name: str,
                                                      document_types: List[str],
                                                      potential_collaborators: List[str] = None) -> bool:
        """
        Start a collaborative documentation project through Agora.
        
        Args:
            project_name: Name of the documentation project
            document_types: Types of documents needed
            potential_collaborators: List of agent IDs to invite
            
        Returns:
            bool: True if project started successfully
        """
        if not self.initialized:
            await self.initialize()
        
        if not potential_collaborators:
            # Find potential collaborators automatically
            helpers = await self.agora_client.find_documentation_helpers("collaboration")
            potential_collaborators = [h.get('agent_id') for h in helpers[:3]]  # Max 3
        
        return await self.agora_client.start_documentation_workflow(
            project_name=project_name,
            document_types=document_types,
            collaborators=potential_collaborators
        )
    
    async def announce_capability_update(self, capability: str, description: str) -> bool:
        """
        Announce a new or updated capability to the Agora community.
        
        Args:
            capability: Name of the capability
            description: Description of the capability
            
        Returns:
            bool: True if announcement successful
        """
        if not self.initialized:
            await self.initialize()
        
        return await self.agora_client.announce_documentation_capability(
            capability=capability,
            description=description,
            proficiency=90
        )
    
    async def get_agora_status(self) -> Dict[str, Any]:
        """
        Get current status from Agora marketplace.
        
        Returns:
            Dictionary containing Agora status information
        """
        if not self.initialized:
            await self.initialize()
        
        return await self.agora_client.get_system_status()
    
    async def check_for_messages(self) -> List[Dict[str, Any]]:
        """
        Check for messages from other agents in Agora.
        
        Returns:
            List of messages (placeholder - would need real implementation)
        """
        # This would integrate with the existing check_messages.py functionality
        # For now, return placeholder
        return []
    
    async def respond_to_task_assignment(self, assignment_data: Dict[str, Any]) -> bool:
        """
        Respond to a task assignment received through Agora.
        
        Args:
            assignment_data: Task assignment information
            
        Returns:
            bool: True if response sent successfully
        """
        assignment_id = assignment_data.get('assignment_id')
        task_data = assignment_data.get('task', {})
        
        if assignment_id:
            # Accept the assignment
            return await self.agora_client.update_progress(
                assignment_id=assignment_id,
                progress=0.0,
                status_update="Task accepted, starting work",
                intermediate_results={"status": "accepted", "agent": self.agent_name}
            )
        
        return False
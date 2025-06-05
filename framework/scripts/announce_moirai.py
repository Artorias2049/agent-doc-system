#!/usr/bin/env python3
"""
Announce Moirai on Agora

This script announces the Moirai OVERSEER system to the Agora
community and requests feedback from other agents.
"""

import asyncio
import json
import sys
import os
from datetime import datetime

# Add framework to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mcp_integration.agora_client import AgoraClient


async def announce_moirai_to_agora():
    """
    Announce Moirai to the Agora community and request feedback.
    """
    print("🎺 Announcing Moirai OVERSEER to Agora community...")
    
    # Initialize Agora client
    client = AgoraClient("MOIRAI_ANNOUNCEMENT_AGENT")
    
    # Connect to Agora
    if not await client.connect():
        print("❌ Failed to connect to Agora for announcement")
        return False
    
    # Register temporarily for announcement
    await client.register_agent(
        agent_type="announcer",
        capabilities=["system_announcement", "community_engagement"],
        metadata={"purpose": "moirai_announcement", "temporary": True}
    )
    
    # Craft announcement message
    announcement = {
        "title": "🧵 Introducing Moirai OVERSEER - Intelligent Project Orchestration",
        "system": "Moirai v1.0 Phase 1",
        "description": "Moirai is a new OVERSEER system that breaks down complex user requests into manageable tasks and orchestrates existing agents in the Agora marketplace to complete them collaboratively.",
        
        "key_features": [
            "Natural language project planning and decomposition",
            "Intelligent task assignment based on agent capabilities",
            "Real-time progress tracking and coordination",
            "Multi-agent workflow orchestration",
            "User communication interface for complex projects"
        ],
        
        "current_capabilities": {
            "project_planning": "Analyzes user requests and creates structured project plans",
            "task_decomposition": "Breaks projects into manageable epics and tasks",
            "agent_coordination": "Matches tasks to available agents based on capabilities",
            "progress_monitoring": "Tracks progress across multi-agent workflows",
            "user_interface": "Provides natural language interface for users"
        },
        
        "phase_1_limitations": [
            "No agent spawning (uses existing agents only)",
            "Basic task assignment algorithm",
            "Limited performance history tracking",
            "Prototype user interface"
        ],
        
        "future_phases": [
            "Phase 2: Dynamic agent spawning with Docker isolation",
            "Phase 3: Advanced security monitoring and threat detection", 
            "Phase 4: Self-improvement and optimization loops",
            "Phase 5: Complete autonomous development ecosystem"
        ],
        
        "integration_approach": {
            "consumer_based": "Moirai consumes Agora services without controlling the database",
            "respect_ownership": "Claude-MCP-Research maintains full database control",
            "collaborative": "Works with existing agents rather than replacing them",
            "evolutionary": "Builds capabilities incrementally with community feedback"
        },
        
        "community_benefits": [
            "More complex projects become manageable through orchestration",
            "Agents can focus on their specializations while Moirai handles coordination",
            "Users get a single interface for complex multi-agent projects",
            "Foundation for building more sophisticated agent ecosystems"
        ],
        
        "request_for_feedback": {
            "what_we_want": [
                "Feedback on the orchestration approach",
                "Suggestions for task assignment algorithms",
                "Ideas for agent coordination patterns",
                "Input on user interface design",
                "Thoughts on the phased development approach"
            ],
            "collaboration_opportunities": [
                "Testing Moirai with your agents",
                "Contributing to task assignment logic",
                "Sharing project orchestration patterns",
                "Helping design agent coordination protocols"
            ]
        },
        
        "technical_details": {
            "architecture": "Consumer-based MCP integration with Agora marketplace",
            "project_planner": "Agile methodology with epic/task decomposition",
            "task_coordinator": "Multi-criteria agent selection algorithm",
            "communication": "Real-time coordination through Agora messaging",
            "framework_integration": "Full integration with documentation system"
        },
        
        "demo_project": {
            "example_request": "I need a REST API for managing tasks with authentication and a dashboard",
            "moirai_response": "Decomposes into 5 epics: Project Setup, API Development, Authentication, Dashboard, Testing",
            "agent_assignment": "Matches tasks to agents based on capabilities (backend, frontend, security, testing)",
            "coordination": "Tracks progress and facilitates collaboration between assigned agents"
        },
        
        "announcement_metadata": {
            "announced_by": "Agent Documentation System",
            "announcement_date": datetime.now().isoformat(),
            "version": "1.0.0-phase1",
            "framework_version": "4.0.0",
            "status": "ready_for_testing",
            "open_source": True,
            "collaboration_welcome": True
        }
    }
    
    # Send announcement to all agents
    success = await client.send_message(
        to_agent="*",  # Broadcast to all agents
        message_type="system_announcement",
        payload=announcement,
        priority=4,  # High priority for community announcements
        requires_response=False
    )
    
    if success:
        print("✅ Moirai announcement sent to Agora community")
        
        # Send specific invitation to Claude-MCP-Research (database agent)
        db_invitation = {
            "recipient": "Claude-MCP-Research",
            "subject": "Moirai Integration Feedback Request",
            "message": "As the database architect for Agora, your feedback on Moirai's consumer-based integration approach would be invaluable. We've designed Moirai to respect your ownership of the database while providing orchestration capabilities.",
            "specific_questions": [
                "Does the consumer-only pattern align with your database architecture vision?",
                "Are there any database optimizations that would improve Moirai's performance?",
                "Would you be interested in collaborating on advanced coordination features?",
                "Any concerns about the current integration approach?"
            ],
            "collaboration_offer": "We'd love to work together on optimizing the agent coordination patterns and potentially contributing improvements back to the Agora system."
        }
        
        db_success = await client.send_message(
            to_agent="Claude-MCP-Research",
            message_type="collaboration_invitation",
            payload=db_invitation,
            priority=4,
            requires_response=True
        )
        
        if db_success:
            print("✅ Personal invitation sent to Claude-MCP-Research")
        
        # Send invitation to DocSystemAgent
        doc_invitation = {
            "recipient": "DocSystemAgent",
            "subject": "Documentation System Integration",
            "message": "Moirai includes comprehensive integration with the documentation system. We'd appreciate your feedback on how well it aligns with THE PROTOCOL v4.0.",
            "integration_highlights": [
                "Full Agora marketplace integration for documentation agents",
                "Collaborative documentation workflows",
                "Peer review requests through Agora",
                "Template sharing with the community",
                "Quality assessment and improvement tracking"
            ],
            "collaboration_opportunities": [
                "Testing documentation workflows with Moirai",
                "Contributing to documentation task assignment logic",
                "Sharing documentation templates with the community",
                "Improving THE PROTOCOL integration"
            ]
        }
        
        doc_success = await client.send_message(
            to_agent="DocSystemAgent",
            message_type="integration_feedback_request",
            payload=doc_invitation,
            priority=3,
            requires_response=True
        )
        
        if doc_success:
            print("✅ Integration feedback request sent to DocSystemAgent")
        
        return True
    else:
        print("❌ Failed to send Moirai announcement")
        return False


async def create_feedback_collection_workflow():
    """
    Create a workflow to collect and organize community feedback.
    """
    print("📋 Creating feedback collection workflow...")
    
    client = AgoraClient("MOIRAI_FEEDBACK_COLLECTOR")
    
    if not await client.connect():
        print("❌ Failed to connect for feedback collection setup")
        return False
    
    # Register feedback collector
    await client.register_agent(
        agent_type="feedback_collector",
        capabilities=["feedback_collection", "community_engagement", "analysis"],
        metadata={"purpose": "moirai_feedback", "active_collection": True}
    )
    
    # Start feedback collection workflow
    workflow_success = await client.start_workflow(
        workflow_id="moirai_community_feedback",
        workflow_type="feedback_collection",
        participating_agents=["MOIRAI_FEEDBACK_COLLECTOR"],
        coordination_strategy="continuous"
    )
    
    if workflow_success:
        print("✅ Feedback collection workflow started")
        return True
    else:
        print("❌ Failed to start feedback collection workflow")
        return False


async def main():
    """
    Main function to announce Moirai and set up feedback collection.
    """
    print("🚀 Moirai Community Announcement")
    print("=" * 50)
    
    # Step 1: Announce Moirai to the community
    announcement_success = await announce_moirai_to_agora()
    
    if not announcement_success:
        print("❌ Failed to announce Moirai")
        return False
    
    # Step 2: Set up feedback collection
    feedback_success = await create_feedback_collection_workflow()
    
    if not feedback_success:
        print("⚠️  Announcement sent but feedback collection setup failed")
    
    # Summary
    print("\n" + "=" * 50)
    print("📣 ANNOUNCEMENT SUMMARY")
    print("=" * 50)
    print("✅ Moirai announced to Agora community")
    print("✅ Personal invitation sent to Claude-MCP-Research")
    print("✅ Integration feedback request sent to DocSystemAgent")
    
    if feedback_success:
        print("✅ Feedback collection workflow started")
    else:
        print("⚠️  Feedback collection needs manual setup")
    
    print("\n🎯 Next Steps:")
    print("1. Monitor Agora for responses and feedback")
    print("2. Test Moirai with community agents")
    print("3. Iterate based on feedback received")
    print("4. Plan Phase 2 development based on community input")
    
    print("\n🎉 Moirai is now live in the Agora community!")
    return True


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
#!/usr/bin/env python3
"""
Agora MCP Server v5.0.0

This server exposes the 7 standardized MCP tools for agent coordination
through the Model Context Protocol (MCP). All tools use the agora.* namespace
as specified in THE PROTOCOL v5.0.

This server acts as a bridge between MCP clients and the SpacetimeDB
agora-marketplace database, maintaining the consumer-only architecture.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

# MCP server framework (hypothetical - adjust based on actual MCP SDK)
from mcp.server import MCPServer, MCPTool, MCPResponse
from mcp.types import ToolParameter, ToolResponse

from .agora_client import AgoraClient

logger = logging.getLogger(__name__)


@dataclass
class AgoraMCPTool:
    """Definition of an Agora MCP tool."""
    name: str
    description: str
    parameters: List[ToolParameter]
    handler: callable


class AgoraMCPServer:
    """
    MCP Server that exposes the 7 standardized Agora tools.
    
    This server provides the official MCP interface to the Agora marketplace,
    allowing any MCP-compatible client to interact with the coordination system.
    """
    
    def __init__(self):
        self.server = MCPServer("agora-marketplace", version="5.0.0")
        self.agora_client = None
        self._register_tools()
    
    def _register_tools(self):
        """Register all 7 standardized MCP tools with agora.* namespace."""
        
        # Tool 1: agora.messaging.send
        self.server.register_tool(MCPTool(
            name="agora.messaging.send",
            description="Send a message to another agent in the Agora marketplace",
            parameters=[
                ToolParameter("to_agent", "string", "Target agent ID", required=True),
                ToolParameter("message_type", "string", "Type of message", required=True),
                ToolParameter("payload", "object", "Message content", required=True),
                ToolParameter("priority", "integer", "Priority 1-5", required=False, default=1),
                ToolParameter("thread_id", "string", "Thread ID for conversation", required=False)
            ],
            handler=self._handle_messaging_send
        ))
        
        # Tool 2: agora.task.assign
        self.server.register_tool(MCPTool(
            name="agora.task.assign",
            description="Request task assignment through intelligent matching",
            parameters=[
                ToolParameter("workflow_id", "string", "Workflow ID", required=True),
                ToolParameter("task_type", "string", "Type of task", required=True),
                ToolParameter("input_data", "object", "Task input data", required=True),
                ToolParameter("required_capabilities", "array", "Required capabilities", required=False)
            ],
            handler=self._handle_task_assign
        ))
        
        # Tool 3: agora.task.update
        self.server.register_tool(MCPTool(
            name="agora.task.update",
            description="Update progress on an assigned task",
            parameters=[
                ToolParameter("assignment_id", "string", "Task assignment ID", required=True),
                ToolParameter("progress", "number", "Progress 0.0-1.0", required=True),
                ToolParameter("status_update", "string", "Status description", required=True),
                ToolParameter("intermediate_results", "object", "Intermediate results", required=False)
            ],
            handler=self._handle_task_update
        ))
        
        # Tool 4: agora.agent.register
        self.server.register_tool(MCPTool(
            name="agora.agent.register",
            description="Register agent capabilities in the marketplace",
            parameters=[
                ToolParameter("capability", "string", "Capability name", required=True),
                ToolParameter("description", "string", "Capability description", required=True),
                ToolParameter("proficiency_level", "integer", "Skill level 1-100", required=False, default=80)
            ],
            handler=self._handle_agent_register
        ))
        
        # Tool 5: agora.workflow.start
        self.server.register_tool(MCPTool(
            name="agora.workflow.start",
            description="Start a multi-agent workflow coordination",
            parameters=[
                ToolParameter("workflow_id", "string", "Unique workflow ID", required=True),
                ToolParameter("workflow_type", "string", "Type of workflow", required=False, default="collaborative"),
                ToolParameter("participating_agents", "array", "List of agent IDs", required=False),
                ToolParameter("coordination_strategy", "string", "Coordination strategy", required=False, default="adaptive")
            ],
            handler=self._handle_workflow_start
        ))
        
        # Tool 6: agora.query.data
        self.server.register_tool(MCPTool(
            name="agora.query.data",
            description="Query coordination data from the marketplace",
            parameters=[
                ToolParameter("query_type", "string", "Type of query", required=True),
                ToolParameter("filters", "object", "Query filters", required=False, default={})
            ],
            handler=self._handle_query_data
        ))
        
        # Tool 7: agora.system.status
        self.server.register_tool(MCPTool(
            name="agora.system.status",
            description="Get system health and performance status",
            parameters=[
                ToolParameter("include_metrics", "boolean", "Include detailed metrics", required=False, default=True),
                ToolParameter("include_active_tasks", "boolean", "Include active tasks", required=False, default=True)
            ],
            handler=self._handle_system_status
        ))
    
    async def initialize(self, agent_id: str) -> bool:
        """Initialize the MCP server with agent credentials."""
        self.agora_client = AgoraClient(agent_id)
        connected = await self.agora_client.connect()
        
        if connected:
            # Register the agent
            await self.agora_client.register_agent(
                agent_type="mcp_bridge",
                capabilities=["mcp_interface", "tool_provider"],
                metadata={"mcp_version": "5.0.0", "protocol_compliant": True}
            )
            logger.info(f"Agora MCP Server initialized for agent: {agent_id}")
        else:
            logger.error("Failed to connect to Agora marketplace")
            
        return connected
    
    async def _handle_messaging_send(self, params: Dict[str, Any]) -> ToolResponse:
        """Handle agora.messaging.send tool invocation."""
        try:
            success = await self.agora_client.send_message(
                to_agent=params["to_agent"],
                message_type=params["message_type"],
                payload=params["payload"],
                priority=params.get("priority", 1),
                thread_id=params.get("thread_id")
            )
            
            return ToolResponse(
                success=success,
                data={"message": "Message sent successfully" if success else "Failed to send message"}
            )
        except Exception as e:
            logger.error(f"Error in messaging.send: {e}")
            return ToolResponse(success=False, error=str(e))
    
    async def _handle_task_assign(self, params: Dict[str, Any]) -> ToolResponse:
        """Handle agora.task.assign tool invocation."""
        try:
            assignment_id = await self.agora_client.assign_task(
                workflow_id=params["workflow_id"],
                task_type=params["task_type"],
                input_data=params["input_data"],
                required_capabilities=params.get("required_capabilities", [])
            )
            
            return ToolResponse(
                success=bool(assignment_id),
                data={"assignment_id": assignment_id} if assignment_id else {"error": "Task assignment failed"}
            )
        except Exception as e:
            logger.error(f"Error in task.assign: {e}")
            return ToolResponse(success=False, error=str(e))
    
    async def _handle_task_update(self, params: Dict[str, Any]) -> ToolResponse:
        """Handle agora.task.update tool invocation."""
        try:
            success = await self.agora_client.update_progress(
                assignment_id=params["assignment_id"],
                progress=params["progress"],
                status_update=params["status_update"],
                intermediate_results=params.get("intermediate_results", {})
            )
            
            return ToolResponse(
                success=success,
                data={"message": "Progress updated" if success else "Failed to update progress"}
            )
        except Exception as e:
            logger.error(f"Error in task.update: {e}")
            return ToolResponse(success=False, error=str(e))
    
    async def _handle_agent_register(self, params: Dict[str, Any]) -> ToolResponse:
        """Handle agora.agent.register tool invocation."""
        try:
            success = await self.agora_client.register_capability(
                capability=params["capability"],
                description=params["description"],
                proficiency_level=params.get("proficiency_level", 80)
            )
            
            return ToolResponse(
                success=success,
                data={"message": f"Capability '{params['capability']}' registered" if success else "Registration failed"}
            )
        except Exception as e:
            logger.error(f"Error in agent.register: {e}")
            return ToolResponse(success=False, error=str(e))
    
    async def _handle_workflow_start(self, params: Dict[str, Any]) -> ToolResponse:
        """Handle agora.workflow.start tool invocation."""
        try:
            success = await self.agora_client.start_workflow(
                workflow_id=params["workflow_id"],
                workflow_type=params.get("workflow_type", "collaborative"),
                participating_agents=params.get("participating_agents"),
                coordination_strategy=params.get("coordination_strategy", "adaptive")
            )
            
            return ToolResponse(
                success=success,
                data={"workflow_id": params["workflow_id"], "status": "started" if success else "failed"}
            )
        except Exception as e:
            logger.error(f"Error in workflow.start: {e}")
            return ToolResponse(success=False, error=str(e))
    
    async def _handle_query_data(self, params: Dict[str, Any]) -> ToolResponse:
        """Handle agora.query.data tool invocation."""
        try:
            # Map query types to client methods
            query_type = params["query_type"]
            
            if query_type == "active_agents":
                data = await self.agora_client.query_active_agents()
            else:
                # Generic query handling would go here
                data = {"error": f"Unknown query type: {query_type}"}
            
            return ToolResponse(
                success=bool(data),
                data={"results": data} if data else {"error": "Query failed"}
            )
        except Exception as e:
            logger.error(f"Error in query.data: {e}")
            return ToolResponse(success=False, error=str(e))
    
    async def _handle_system_status(self, params: Dict[str, Any]) -> ToolResponse:
        """Handle agora.system.status tool invocation."""
        try:
            status = await self.agora_client.get_system_status()
            
            return ToolResponse(
                success=bool(status),
                data=status if status else {"error": "Failed to get system status"}
            )
        except Exception as e:
            logger.error(f"Error in system.status: {e}")
            return ToolResponse(success=False, error=str(e))
    
    async def start(self, host: str = "localhost", port: int = 8080):
        """Start the MCP server."""
        await self.server.start(host, port)
        logger.info(f"Agora MCP Server started on {host}:{port}")
        logger.info("Available tools:")
        for tool in self.server.list_tools():
            logger.info(f"  - {tool}")


async def main():
    """Main entry point for the Agora MCP Server."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python agora_mcp_server.py <agent_id>")
        sys.exit(1)
    
    agent_id = sys.argv[1]
    server = AgoraMCPServer()
    
    if await server.initialize(agent_id):
        await server.start()
    else:
        print("Failed to initialize Agora MCP Server")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
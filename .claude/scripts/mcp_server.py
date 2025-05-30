#!/usr/bin/env python3
"""
MCP Server for Agent Documentation System
Exposes agent communication and chat management as MCP tools.
"""

import asyncio
import sys
from pathlib import Path
from typing import List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from mcp.server import NotificationOptions, Server
    from mcp.server.models import InitializationOptions
    from mcp.types import CallToolRequest, CallToolResult, TextContent, Tool

    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("MCP not available. Install with: pip install mcp", file=sys.stderr)

from framework.agent_communication.core.enhanced_protocol import (
    EnhancedAgentProtocol,
)

# Import chat logger with proper path handling
try:
    from .chat_logger import ChatLogger
except ImportError:
    # Fallback for direct execution
    import sys
    from pathlib import Path

    script_dir = Path(__file__).parent
    sys.path.insert(0, str(script_dir))
    from chat_logger import ChatLogger

# Initialize server
server = Server("agent-doc-system")

# Global instances
protocol = None
chat_logger = None


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="agent_send",
            description="Send an agent message with validation",
            inputSchema={
                "type": "object",
                "properties": {
                    "message_type": {
                        "type": "string",
                        "enum": [
                            "test_request",
                            "test_result",
                            "status_update",
                            "context_update",
                            "workflow_request",
                            "validation_request",
                            "documentation_update",
                        ],
                        "description": "Type of message to send",
                    },
                    "content": {
                        "type": "object",
                        "description": "Message content as JSON object",
                    },
                    "target_agent": {
                        "type": "string",
                        "description": "Target agent identifier (optional)",
                    },
                },
                "required": ["message_type", "content"],
            },
        ),
        Tool(
            name="agent_read",
            description="Read and filter agent messages",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["pending", "processed", "failed"],
                        "description": "Filter by message status",
                    },
                    "message_type": {
                        "type": "string",
                        "enum": [
                            "test_request",
                            "test_result",
                            "status_update",
                            "context_update",
                            "workflow_request",
                            "validation_request",
                            "documentation_update",
                        ],
                        "description": "Filter by message type",
                    },
                    "sender": {
                        "type": "string",
                        "description": "Filter by sender",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Limit number of results",
                        "default": 10,
                    },
                },
            },
        ),
        Tool(
            name="agent_validate",
            description="Validate all agent messages",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="agent_workflow",
            description="Execute a workflow request",
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow_name": {
                        "type": "string",
                        "description": "Name of the workflow",
                    },
                    "steps": {
                        "type": "array",
                        "description": "Array of workflow steps",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "action": {"type": "string"},
                                "parameters": {"type": "object"},
                            },
                        },
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Workflow parameters",
                    },
                    "parallel_execution": {
                        "type": "boolean",
                        "description": "Enable parallel execution",
                        "default": False,
                    },
                },
                "required": ["workflow_name", "steps"],
            },
        ),
        Tool(
            name="chat_export",
            description="Export current chat session",
            inputSchema={
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "enum": ["markdown", "json", "html"],
                        "description": "Export format",
                        "default": "markdown",
                    },
                    "include_metadata": {
                        "type": "boolean",
                        "description": "Include session metadata",
                        "default": True,
                    },
                    "sanitize": {
                        "type": "boolean",
                        "description": "Apply privacy filters",
                        "default": True,
                    },
                },
            },
        ),
        Tool(
            name="chat_history",
            description="List recent chat sessions",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of sessions to show",
                        "default": 10,
                    }
                },
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(request: CallToolRequest) -> CallToolResult:
    """Handle tool calls."""
    global protocol, chat_logger

    # Initialize on first call
    if protocol is None:
        protocol = EnhancedAgentProtocol("mcp-server")
    if chat_logger is None:
        chat_logger = ChatLogger()

    try:
        if request.name == "agent_send":
            # Send agent message
            message_type = request.arguments["message_type"]
            content = request.arguments["content"]
            target_agent = request.arguments.get("target_agent")

            message_id = protocol.send_message(
                message_type=message_type,
                content=content,
                target_agent=target_agent,
            )

            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"✅ Message sent successfully with ID: {message_id}",
                    )
                ]
            )

        elif request.name == "agent_read":
            # Read agent messages
            from framework.agent_communication.core.models import (
                MessageStatus,
                MessageType,
            )

            status = (
                MessageStatus(request.arguments["status"])
                if request.arguments.get("status")
                else None
            )
            message_type = (
                MessageType(request.arguments["message_type"])
                if request.arguments.get("message_type")
                else None
            )
            sender = request.arguments.get("sender")
            limit = request.arguments.get("limit", 10)

            messages = protocol.get_messages(
                status=status,
                message_type=message_type,
                sender=sender,
                limit=limit,
            )

            if messages:
                result = f"Found {len(messages)} messages:\n\n"
                for msg in messages:
                    result += (
                        f"**{msg.type}** from {msg.sender} ({msg.status})\n"
                    )
                    result += f"ID: {str(msg.id)[:8]}...\n"
                    result += (
                        f"Time: {msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    )
                    result += f"Content: {str(msg.content)[:100]}...\n\n"
            else:
                result = "No messages found."

            return CallToolResult(
                content=[TextContent(type="text", text=result)]
            )

        elif request.name == "agent_validate":
            # Validate messages
            report = protocol.validate_all_messages()

            if report["invalid_messages"] == 0:
                result = (
                    f"✅ All {report['total_messages']} messages are valid!"
                )
            else:
                result = f"⚠️ Found {report['invalid_messages']} invalid messages out of {report['total_messages']}"
                if report["errors"]:
                    result += "\n\nErrors:\n"
                    for error in report["errors"]:
                        result += f"- Message {error['message_id']}: {error['error']}\n"

            return CallToolResult(
                content=[TextContent(type="text", text=result)]
            )

        elif request.name == "agent_workflow":
            # Execute workflow
            workflow_name = request.arguments["workflow_name"]
            steps = request.arguments["steps"]
            parameters = request.arguments.get("parameters", {})
            parallel = request.arguments.get("parallel_execution", False)

            workflow_content = {
                "workflow_name": workflow_name,
                "steps": steps,
                "parameters": parameters,
                "parallel_execution": parallel,
                "failure_strategy": "abort",
            }

            message_id = protocol.send_message(
                message_type="workflow_request", content=workflow_content
            )

            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"✅ Workflow '{workflow_name}' request sent with ID: {message_id}",
                    )
                ]
            )

        elif request.name == "chat_export":
            # Export chat session
            try:
                session_file = chat_logger.export_current_session()
                result = f"✅ Chat session exported to: {session_file}"
            except Exception as e:
                result = f"❌ Export failed: {str(e)}"

            return CallToolResult(
                content=[TextContent(type="text", text=result)]
            )

        elif request.name == "chat_history":
            # List chat history
            limit = request.arguments.get("limit", 10)
            sessions = chat_logger.list_sessions(limit)

            if sessions:
                result = f"Found {len(sessions)} recent sessions:\n\n"
                for session in sessions:
                    result += f"**{session['name']}**\n"
                    result += f"Size: {session['size'] / 1024:.1f} KB\n"
                    result += f"Modified: {session['modified'].strftime('%Y-%m-%d %H:%M')}\n"
                    result += f"Compressed: {'Yes' if session['compressed'] else 'No'}\n\n"
            else:
                result = "No chat sessions found."

            return CallToolResult(
                content=[TextContent(type="text", text=result)]
            )

        else:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text", text=f"❌ Unknown tool: {request.name}"
                    )
                ]
            )

    except Exception as e:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"❌ Error executing {request.name}: {str(e)}",
                )
            ]
        )


async def main():
    """Run the MCP server."""
    if not MCP_AVAILABLE:
        print("MCP is not available. Please install: pip install mcp")
        sys.exit(1)

    # Run server
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="agent-doc-system",
                server_version="1.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    if MCP_AVAILABLE:
        asyncio.run(main())
    else:
        print(
            "MCP library not available. The slash commands work through direct script execution:"
        )
        print(
            "Example: python3 .claude/scripts/slash_command_handler.py '/agent:send --type test_request --content {...}'"
        )


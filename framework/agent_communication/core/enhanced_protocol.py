#!/usr/bin/env python3
"""
Enhanced agent communication protocol with Pydantic models, type safety, and Claude Code optimizations.
"""

import json
import logging
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

try:
    from .models import (
        AgentMessage,
        MessageFile,
        MessageStatus,
        MessageType,
        TestRequestContent,
        ValidationRequestContent,
        WorkflowRequestContent,
        create_message,
        serialize_message,
        validate_message_dict,
    )
except ImportError:
    # Fallback for direct execution
    import sys

    sys.path.append(str(Path(__file__).parent))
    from models import (
        AgentMessage,
        MessageFile,
        MessageType,
        MessageStatus,
        create_message,
        validate_message_dict,
        serialize_message,
        TestRequestContent,
        WorkflowRequestContent,
        ValidationRequestContent,
    )

import click
from pydantic import ValidationError
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

# Configure logging with rich formatting
logging.basicConfig(
    level=logging.INFO, format="%(message)s", handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)
console = Console()


class EnhancedAgentProtocol:
    """Enhanced agent communication protocol with Pydantic validation and Claude Code features."""

    def __init__(
        self,
        agent_id: Optional[str] = None,
        root_dir: Optional[str] = None,
        environment: str = "development",
    ):
        self.agent_id = agent_id or "default_agent"
        self.environment = environment
        self.root_dir = Path(root_dir) if root_dir else self._detect_root_dir()

        # Configuration paths - handle nested agent-doc-system usage
        self.config_dir = self.root_dir / ".claude" / "config"
        
        # Determine framework path based on usage pattern
        if (self.root_dir / "agent-doc-system" / "framework").exists():
            # Nested usage: your_project/agent-doc-system/framework/
            self.framework_dir = self.root_dir / "agent-doc-system" / "framework"
        else:
            # Direct usage: project_root/framework/
            self.framework_dir = self.root_dir / "framework"
            
        self.message_dir = self.framework_dir / "agent_communication" / "history"

        # Environment-specific message file
        if environment == "development":
            self.message_file = self.message_dir / "dev_messages.json"
        elif environment == "staging":
            self.message_file = self.message_dir / "staging_messages.json"
        else:
            self.message_file = self.message_dir / "agent_messages.json"

        self._load_configuration()
        self._initialize_protocol()

    def _detect_root_dir(self) -> Path:
        """
        Auto-detect project root directory.
        
        Supports nested usage pattern where agent-doc-system is cloned into project directories:
        your_project/                   # Project root (returned)
        └── agent-doc-system/           # Cloned framework
            └── framework/              # Framework directory
        """
        current = Path.cwd()
        while current != current.parent:
            # Check for nested agent-doc-system pattern first
            if (current / "agent-doc-system" / "framework").exists():
                return current
            # Check for direct framework usage (backward compatibility)
            elif (current / "framework").exists() or (current / ".claude").exists():
                return current
            current = current.parent
        return Path.cwd()

    def _load_configuration(self):
        """Load agent-specific configuration."""
        config_file = self.config_dir / "agent_settings.json"
        if config_file.exists():
            with open(config_file) as f:
                self.config = json.load(f)
        else:
            self.config = self._default_config()

    def _default_config(self) -> Dict[str, Any]:
        """Default configuration when no config file exists."""
        return {
            "agent_communication": {
                "cleanup_policy": {"default_retention_days": 7},
                "validation": {
                    "strict_mode": True,
                    "auto_validate_on_send": True,
                },
            },
            "development_preferences": {"testing": {"coverage_threshold": 90}},
        }

    def _initialize_protocol(self):
        """Initialize protocol and create necessary directories."""
        self.message_dir.mkdir(parents=True, exist_ok=True)

        if not self.message_file.exists():
            initial_data = MessageFile(
                messages=[],
                version="1.1.0",
                metadata={
                    "agent_id": self.agent_id,
                    "environment": self.environment,
                },
            )
            self._write_message_file(initial_data)

    def _read_message_file(self) -> MessageFile:
        """Read and validate message file."""
        try:
            if not self.message_file.exists():
                return MessageFile()

            with open(self.message_file) as f:
                data = json.load(f)

            # Handle legacy format or raw dict conversion
            if "messages" in data:
                validated_messages = []
                for msg_data in data["messages"]:
                    try:
                        # Convert string timestamps to datetime objects if needed
                        if isinstance(msg_data.get("timestamp"), str):
                            msg_data["timestamp"] = datetime.fromisoformat(
                                msg_data["timestamp"].replace("Z", "+00:00")
                            )
                        validated_messages.append(AgentMessage(**msg_data))
                    except ValidationError as ve:
                        console.print(
                            f"[yellow]Skipping invalid message {msg_data.get('id', 'unknown')}: {ve}[/yellow]"
                        )
                        continue

                data["messages"] = validated_messages

            return MessageFile(**data)
        except (json.JSONDecodeError, ValidationError) as e:
            logger.warning(f"Invalid message file format: {e}")
            # Backup corrupted file and create new one
            backup_path = self.message_file.with_suffix(".backup.json")
            if self.message_file.exists():
                self.message_file.rename(backup_path)
                console.print(
                    f"[yellow]Corrupted file backed up to {backup_path}[/yellow]"
                )

            return MessageFile()

    def _write_message_file(self, message_file: MessageFile):
        """Write validated message file."""
        message_file.last_updated = datetime.now(timezone.utc)

        with open(self.message_file, "w") as f:
            json.dump(
                message_file.dict(by_alias=True), f, indent=2, default=str
            )

    def send_message(
        self,
        message_type: Union[str, MessageType],
        content: Dict[str, Any],
        target_agent: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Send a validated message with enhanced error handling."""

        # Convert string to enum if needed
        if isinstance(message_type, str):
            try:
                message_type = MessageType(message_type)
            except ValueError:
                raise ValueError(f"Invalid message type: {message_type}")

        # Validate content early if strict mode is enabled
        if (
            self.config.get("agent_communication", {})
            .get("validation", {})
            .get("auto_validate_on_send", True)
        ):
            try:
                # Create and validate message
                message = create_message(
                    sender=self.agent_id,
                    message_type=message_type,
                    content=content,
                    metadata=metadata,
                )
            except ValidationError as e:
                console.print(f"[red]Message validation failed:[/red]")
                console.print(JSON(e.json()))
                raise ValueError(f"Invalid message content: {e}")
        else:
            # Create message without early validation
            message = AgentMessage(
                sender=self.agent_id,
                type=message_type,
                content=content,
                metadata=metadata or {},
            )

        # Add to message file
        message_file = self._read_message_file()
        message_file.messages.append(message)
        self._write_message_file(message_file)

        # Log success with rich formatting
        console.print(
            Panel(
                f"[green]✅ Message sent successfully[/green]\n"
                f"ID: {message.id}\n"
                f"Type: {message.type}\n"
                f"Target: {target_agent or 'broadcast'}\n"
                f"File: {self.message_file}",
                title="Message Sent",
                border_style="green",
            )
        )

        return str(message.id)

    def get_messages(
        self,
        status: Optional[MessageStatus] = None,
        message_type: Optional[MessageType] = None,
        sender: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[AgentMessage]:
        """Get messages with flexible filtering."""
        message_file = self._read_message_file()
        messages = message_file.messages

        # Apply filters
        if status:
            messages = [msg for msg in messages if msg.status == status]
        if message_type:
            messages = [msg for msg in messages if msg.type == message_type]
        if sender:
            messages = [msg for msg in messages if msg.sender == sender]

        # Apply limit
        if limit:
            messages = messages[-limit:]

        return messages

    def update_message_status(
        self,
        message_id: Union[str, uuid.UUID],
        status: MessageStatus,
        metadata_update: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Update message status with validation."""
        message_file = self._read_message_file()
        message_id_str = str(message_id)

        for message in message_file.messages:
            if str(message.id) == message_id_str:
                message.status = status
                if metadata_update:
                    message.metadata.update(metadata_update)

                self._write_message_file(message_file)
                console.print(
                    f"[green]✅ Message {message_id_str} status updated to {status}[/green]"
                )
                return True

        console.print(f"[red]❌ Message {message_id_str} not found[/red]")
        return False

    def cleanup_old_messages(
        self, days: Optional[int] = None, archive: bool = True
    ) -> int:
        """Clean up old messages with archiving option."""
        days = days or self.config.get("agent_communication", {}).get(
            "cleanup_policy", {}
        ).get("default_retention_days", 7)

        message_file = self._read_message_file()
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

        old_messages = []
        current_messages = []

        for message in message_file.messages:
            if (
                message.timestamp < cutoff_date
                and message.status == MessageStatus.PROCESSED
            ):
                old_messages.append(message)
            else:
                current_messages.append(message)

        if old_messages and archive:
            # Archive old messages
            archive_file = (
                self.message_dir
                / f"archive_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
            )
            archive_data = MessageFile(
                messages=old_messages,
                version=message_file.version,
                metadata={
                    "archived_from": str(self.message_file),
                    "archive_date": datetime.now(timezone.utc),
                },
            )

            with open(archive_file, "w") as f:
                json.dump(
                    archive_data.dict(by_alias=True), f, indent=2, default=str
                )

            console.print(
                f"[blue]📦 Archived {len(old_messages)} messages to {archive_file}[/blue]"
            )

        # Update message file with current messages
        message_file.messages = current_messages
        self._write_message_file(message_file)

        console.print(
            f"[green]🧹 Cleaned up {len(old_messages)} messages older than {days} days[/green]"
        )
        return len(old_messages)

    def validate_all_messages(self) -> Dict[str, Any]:
        """Validate all messages in the file and return report."""
        message_file = self._read_message_file()

        validation_report = {
            "total_messages": len(message_file.messages),
            "valid_messages": 0,
            "invalid_messages": 0,
            "errors": [],
        }

        for i, message in enumerate(message_file.messages):
            try:
                # Re-validate message
                AgentMessage(**message.dict())
                validation_report["valid_messages"] += 1
            except ValidationError as e:
                validation_report["invalid_messages"] += 1
                validation_report["errors"].append(
                    {
                        "message_index": i,
                        "message_id": str(message.id),
                        "error": e.json(),
                    }
                )

        return validation_report

    def display_messages(self, messages: List[AgentMessage]):
        """Display messages in a rich table format."""
        if not messages:
            console.print("[yellow]No messages found.[/yellow]")
            return

        table = Table(title=f"Agent Messages ({len(messages)} found)")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Type", style="magenta")
        table.add_column("Sender", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Timestamp", style="blue")
        table.add_column("Content Preview", style="white")

        for message in messages:
            content_preview = (
                str(message.content)[:50] + "..."
                if len(str(message.content)) > 50
                else str(message.content)
            )
            table.add_row(
                str(message.id)[:8] + "...",
                message.type,
                message.sender,
                message.status,
                message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                content_preview,
            )

        console.print(table)

    # Convenience methods to match THE PROTOCOL documentation
    
    def create_test_request(
        self,
        test_type: str,
        test_file: str,
        parameters: Dict[str, Any],
        sender: Optional[str] = None,
    ) -> str:
        """Create and send a test request message."""
        content = {
            "test_type": test_type,
            "test_file": test_file,
            "parameters": parameters
        }
        return self.send_message(
            message_type=MessageType.TEST_REQUEST,
            content=content,
            metadata={"created_by": "create_test_request"}
        )

    def create_workflow_request(
        self,
        workflow_name: str,
        steps: List[Dict[str, Any]],
        sender: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        parallel_execution: bool = False,
        failure_strategy: str = "abort"
    ) -> str:
        """Create and send a workflow request message."""
        content = {
            "workflow_name": workflow_name,
            "steps": steps,
            "parameters": parameters or {},
            "parallel_execution": parallel_execution,
            "failure_strategy": failure_strategy
        }
        return self.send_message(
            message_type=MessageType.WORKFLOW_REQUEST,
            content=content,
            metadata={"created_by": "create_workflow_request"}
        )

    def create_validation_request(
        self,
        validation_type: str,
        target_files: List[str],
        sender: Optional[str] = None,
        validation_level: str = "enhanced",
        auto_fix: bool = False,
        generate_report: bool = True
    ) -> str:
        """Create and send a validation request message."""
        content = {
            "validation_type": validation_type,
            "target_files": target_files,
            "validation_level": validation_level,
            "auto_fix": auto_fix,
            "generate_report": generate_report
        }
        return self.send_message(
            message_type=MessageType.VALIDATION_REQUEST,
            content=content,
            metadata={"created_by": "create_validation_request"}
        )

    def read_messages(self, **filters) -> List[AgentMessage]:
        """Alias for get_messages to match THE PROTOCOL documentation."""
        return self.get_messages(**filters)


# CLI Commands using Click


@click.group()
@click.option("--agent-id", required=True, help="Agent identifier")
@click.option(
    "--environment",
    default="development",
    help="Environment (development/staging/production)",
)
@click.option("--root-dir", help="Project root directory")
@click.pass_context
def cli(ctx, agent_id, environment, root_dir):
    """Enhanced Agent Communication Protocol CLI."""
    ctx.ensure_object(dict)
    ctx.obj["protocol"] = EnhancedAgentProtocol(agent_id, root_dir, environment)


@cli.command()
@click.option(
    "--type",
    "message_type",
    required=True,
    type=click.Choice(
        [
            "test_request",
            "test_result",
            "status_update",
            "context_update",
            "workflow_request",
            "validation_request",
            "documentation_update",
        ]
    ),
)
@click.option("--content", required=True, help="Message content as JSON string")
@click.option("--target", help="Target agent identifier")
@click.option("--metadata", help="Additional metadata as JSON string")
@click.pass_context
def send(ctx, message_type, content, target, metadata):
    """Send an agent message with validation."""
    protocol = ctx.obj["protocol"]

    try:
        content_dict = json.loads(content)
        metadata_dict = json.loads(metadata) if metadata else None

        message_id = protocol.send_message(
            message_type=message_type,
            content=content_dict,
            target_agent=target,
            metadata=metadata_dict,
        )

    except json.JSONDecodeError as e:
        console.print(f"[red]Invalid JSON: {e}[/red]")
        raise click.Abort()
    except Exception as e:
        console.print(f"[red]Error sending message: {e}[/red]")
        raise click.Abort()


@cli.command()
@click.option("--status", type=click.Choice(["pending", "processed", "failed"]))
@click.option(
    "--type",
    "message_type",
    type=click.Choice(
        [
            "test_request",
            "test_result",
            "status_update",
            "context_update",
            "workflow_request",
            "validation_request",
            "documentation_update",
        ]
    ),
)
@click.option("--sender", help="Filter by sender")
@click.option("--limit", type=int, help="Limit number of results")
@click.pass_context
def read(ctx, status, message_type, sender, limit):
    """Read and display messages with filtering."""
    protocol = ctx.obj["protocol"]

    # Convert string enums
    status_enum = MessageStatus(status) if status else None
    type_enum = MessageType(message_type) if message_type else None

    messages = protocol.get_messages(
        status=status_enum, message_type=type_enum, sender=sender, limit=limit
    )

    protocol.display_messages(messages)


@cli.command()
@click.option("--days", type=int, help="Retention days (default: from config)")
@click.option("--no-archive", is_flag=True, help="Delete instead of archiving")
@click.pass_context
def cleanup(ctx, days, no_archive):
    """Clean up old processed messages."""
    protocol = ctx.obj["protocol"]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task("Cleaning up messages...", total=None)
        cleaned_count = protocol.cleanup_old_messages(
            days=days, archive=not no_archive
        )
        progress.remove_task(task)


@cli.command()
@click.pass_context
def validate(ctx):
    """Validate all messages in the file."""
    protocol = ctx.obj["protocol"]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task("Validating messages...", total=None)
        report = protocol.validate_all_messages()
        progress.remove_task(task)

    # Display validation report
    if report["invalid_messages"] == 0:
        console.print(
            f"[green]✅ All {report['total_messages']} messages are valid![/green]"
        )
    else:
        console.print(
            f"[yellow]⚠️  Found {report['invalid_messages']} invalid messages out of {report['total_messages']}[/yellow]"
        )

        if report["errors"]:
            console.print("\n[red]Validation Errors:[/red]")
            for error in report["errors"]:
                console.print(
                    f"Message {error['message_id']}: {error['error']}"
                )


@cli.command()
@click.option("--name", required=True, help="Workflow name")
@click.option("--steps", required=True, help="Workflow steps as JSON array")
@click.option("--parameters", help="Workflow parameters as JSON string")
@click.option("--parallel", is_flag=True, help="Enable parallel execution")
@click.pass_context
def workflow(ctx, name, steps, parameters, parallel):
    """Execute a workflow request."""
    protocol = ctx.obj["protocol"]

    try:
        steps_list = json.loads(steps)
        parameters_dict = json.loads(parameters) if parameters else {}

        workflow_content = {
            "workflow_name": name,
            "steps": steps_list,
            "parameters": parameters_dict,
            "parallel_execution": parallel,
            "failure_strategy": "abort",
        }

        message_id = protocol.send_message(
            message_type="workflow_request", content=workflow_content
        )

        console.print(
            f"[green]✅ Workflow '{name}' request sent with ID: {message_id}[/green]"
        )

    except json.JSONDecodeError as e:
        console.print(f"[red]Invalid JSON: {e}[/red]")
        raise click.Abort()
    except Exception as e:
        console.print(f"[red]Error executing workflow: {e}[/red]")
        raise click.Abort()


if __name__ == "__main__":
    cli()


#!/usr/bin/env python3
"""
Claude Code Slash Command Handler
Entry point for processing slash commands from Claude Code interface.
"""

import sys
import os
from pathlib import Path

# Add the .claude/core directory to Python path for imports
claude_core_path = Path(__file__).parent.parent / "core"
sys.path.insert(0, str(claude_core_path))

from command_router import CommandRouter
from rich.console import Console

console = Console()


def main():
    """Main entry point for slash command processing."""
    if len(sys.argv) < 2:
        console.print("[red]❌ No command provided[/red]")
        console.print("Usage: slash_command_handler.py '/command:subcommand [args...]'")
        sys.exit(1)
    
    # Join all arguments to reconstruct the full command line
    command_line = " ".join(sys.argv[1:])
    
    # Handle special case where command might be quoted
    if command_line.startswith('"') and command_line.endswith('"'):
        command_line = command_line[1:-1]
    elif command_line.startswith("'") and command_line.endswith("'"):
        command_line = command_line[1:-1]
    
    # Initialize router and process command
    try:
        router = CommandRouter()
        success = router.process_command_line(command_line)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Command interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]❌ Unexpected error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Claude Code Slash Command Router
Parses and executes slash commands by bridging to existing Python implementations.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import shlex

import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()


class CommandRouter:
    """Routes slash commands to appropriate Python implementations."""
    
    def __init__(self, root_dir: Optional[str] = None):
        self.root_dir = Path(root_dir) if root_dir else self._detect_root_dir()
        self.config_path = self.root_dir / ".claude" / "config" / "command_routing.json"
        self.commands_dir = self.root_dir / ".claude" / "commands"
        
        self.command_config = self._load_command_config()
        self._validate_environment()
    
    def _detect_root_dir(self) -> Path:
        """Auto-detect project root directory."""
        current = Path.cwd()
        while current != current.parent:
            if (current / ".claude").exists() or (current / "framework").exists():
                return current
            current = current.parent
        return Path.cwd()
    
    def _load_command_config(self) -> Dict[str, Any]:
        """Load command routing configuration."""
        if self.config_path.exists():
            with open(self.config_path) as f:
                return json.load(f)
        return self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default command routing configuration."""
        config = {
            "version": "1.1.0",
            "commands": {
                "agent": {
                    "send": {
                        "script": "framework/agent_communication/core/enhanced_protocol.py",
                        "method": "send",
                        "description": "Send agent message"
                    },
                    "read": {
                        "script": "framework/agent_communication/core/enhanced_protocol.py", 
                        "method": "read",
                        "description": "Read agent messages"
                    },
                    "validate": {
                        "script": "framework/agent_communication/core/enhanced_protocol.py",
                        "method": "validate", 
                        "description": "Validate agent messages"
                    },
                    "cleanup": {
                        "script": "framework/agent_communication/core/enhanced_protocol.py",
                        "method": "cleanup",
                        "description": "Cleanup old messages"
                    },
                    "audit": {
                        "script": "framework/scripts/validate.sh",
                        "method": "shell",
                        "description": "Audit agent components"
                    }
                },
                "chat": {
                    "export": {
                        "script": ".claude/scripts/chat_logger.py",
                        "method": "export",
                        "description": "Export current chat session"
                    },
                    "history": {
                        "script": ".claude/scripts/chat_logger.py",
                        "method": "list",
                        "description": "Browse chat history"
                    },
                    "config": {
                        "script": ".claude/scripts/chat_logger.py",
                        "method": "config",
                        "description": "Configure chat settings"
                    }
                }
            },
            "aliases": {
                "/agent:send": "agent send",
                "/agent:read": "agent read", 
                "/agent:validate": "agent validate",
                "/agent:workflow": "agent workflow",
                "/agent:audit": "agent audit",
                "/chat:export": "chat export",
                "/chat:history": "chat history",
                "/chat:config": "chat config"
            }
        }
        
        # Save config for future use
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        return config
    
    def _validate_environment(self):
        """Validate that required scripts exist."""
        missing_scripts = []
        
        for category, commands in self.command_config["commands"].items():
            for cmd_name, cmd_config in commands.items():
                script_path = self.root_dir / cmd_config["script"]
                if not script_path.exists():
                    missing_scripts.append(f"{category}:{cmd_name} -> {script_path}")
        
        if missing_scripts:
            console.print("[yellow]⚠️  Warning: Some command scripts are missing:[/yellow]")
            for script in missing_scripts:
                console.print(f"  - {script}")
    
    def parse_slash_command(self, command_line: str) -> Tuple[Optional[str], Optional[str], List[str]]:
        """Parse slash command into category, command, and arguments."""
        # Remove leading slash and split
        if not command_line.startswith('/'):
            return None, None, []
        
        command_line = command_line[1:]  # Remove leading /
        
        # Split on first space to separate command from args
        parts = command_line.split(' ', 1)
        command_part = parts[0]
        args_part = parts[1] if len(parts) > 1 else ""
        
        # Parse command (category:subcommand)
        if ':' not in command_part:
            return None, None, []
        
        category, subcommand = command_part.split(':', 1)
        
        # Parse arguments using shell-like parsing
        try:
            args = shlex.split(args_part) if args_part else []
        except ValueError:
            # Fallback to simple split if shlex fails
            args = args_part.split() if args_part else []
        
        return category, subcommand, args
    
    def execute_command(self, category: str, command: str, args: List[str]) -> bool:
        """Execute a routed command."""
        # Check if command exists
        if category not in self.command_config["commands"]:
            console.print(f"[red]❌ Unknown command category: {category}[/red]")
            return False
        
        if command not in self.command_config["commands"][category]:
            console.print(f"[red]❌ Unknown command: {category}:{command}[/red]")
            self._show_available_commands(category)
            return False
        
        cmd_config = self.command_config["commands"][category][command]
        script_path = self.root_dir / cmd_config["script"]
        
        if not script_path.exists():
            console.print(f"[red]❌ Script not found: {script_path}[/red]")
            return False
        
        console.print(f"[blue]🚀 Executing: {category}:{command}[/blue]")
        
        try:
            return self._execute_script(script_path, cmd_config["method"], args)
        except Exception as e:
            console.print(f"[red]❌ Command failed: {e}[/red]")
            return False
    
    def _execute_script(self, script_path: Path, method: str, args: List[str]) -> bool:
        """Execute the actual script with proper arguments."""
        if method == "shell":
            # Execute shell script
            cmd = [str(script_path)] + args
            result = subprocess.run(cmd, cwd=self.root_dir, capture_output=True, text=True)
            
            if result.stdout:
                console.print(result.stdout)
            if result.stderr:
                console.print(f"[yellow]{result.stderr}[/yellow]")
            
            return result.returncode == 0
        
        else:
            # Execute Python script with method and proper PYTHONPATH
            env = os.environ.copy()
            # Add project root and script directory to Python path
            script_dir = str(script_path.parent)
            current_path = env.get('PYTHONPATH', '')
            env['PYTHONPATH'] = f"{self.root_dir}:{script_dir}:{current_path}" if current_path else f"{self.root_dir}:{script_dir}"
            
            # Special handling for enhanced_protocol.py which requires --agent-id
            if script_path.name == "enhanced_protocol.py":
                agent_id = "system"  # Default agent ID
                cmd = [sys.executable, str(script_path), "--agent-id", agent_id, method] + args
            else:
                cmd = [sys.executable, str(script_path), method] + args
                
            result = subprocess.run(cmd, cwd=self.root_dir, capture_output=True, text=True, env=env)
            
            if result.stdout:
                console.print(result.stdout)
            if result.stderr and result.returncode != 0:
                console.print(f"[red]{result.stderr}[/red]")
            
            return result.returncode == 0
    
    def _show_available_commands(self, category: Optional[str] = None):
        """Show available commands."""
        if category and category in self.command_config["commands"]:
            console.print(f"\n[blue]Available commands for {category}:[/blue]")
            for cmd_name, cmd_config in self.command_config["commands"][category].items():
                console.print(f"  /{category}:{cmd_name} - {cmd_config['description']}")
        else:
            console.print("\n[blue]Available slash commands:[/blue]")
            for cat, commands in self.command_config["commands"].items():
                for cmd_name, cmd_config in commands.items():
                    console.print(f"  /{cat}:{cmd_name} - {cmd_config['description']}")
    
    def process_command_line(self, command_line: str) -> bool:
        """Main entry point for processing a command line."""
        category, command, args = self.parse_slash_command(command_line)
        
        if not category or not command:
            if command_line.strip() == "/help" or command_line.strip() == "/?":
                self._show_available_commands()
                return True
            else:
                console.print(f"[red]❌ Invalid command format: {command_line}[/red]")
                console.print("Use format: /category:command [args...]")
                console.print("Type /help for available commands")
                return False
        
        return self.execute_command(category, command, args)


# CLI Interface
@click.group()
@click.option('--root-dir', help='Project root directory')
@click.pass_context
def cli(ctx, root_dir):
    """Claude Code Slash Command Router."""
    ctx.ensure_object(dict)
    ctx.obj['router'] = CommandRouter(root_dir)


@cli.command()
@click.argument('command_line')
@click.pass_context
def execute(ctx, command_line):
    """Execute a slash command."""
    router = ctx.obj['router']
    success = router.process_command_line(command_line)
    sys.exit(0 if success else 1)


@cli.command()
@click.pass_context
def list_commands(ctx):
    """List all available slash commands."""
    router = ctx.obj['router']
    router._show_available_commands()


@cli.command()
@click.pass_context 
def validate_config(ctx):
    """Validate command configuration."""
    router = ctx.obj['router']
    router._validate_environment()
    console.print("[green]✅ Configuration validated[/green]")


if __name__ == "__main__":
    cli()
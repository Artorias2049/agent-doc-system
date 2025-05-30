#!/usr/bin/env python3
"""
Claude Code Chat Logger
Exports and manages chat history from Claude Code sessions.
"""

import json
import os
import re
import subprocess
import gzip
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
import uuid
import hashlib

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class ChatLogger:
    """Manages Claude Code chat logging and export functionality."""
    
    def __init__(self, root_dir: Optional[str] = None):
        self.root_dir = Path(root_dir) if root_dir else self._detect_root_dir()
        self.config_path = self.root_dir / ".claude" / "config" / "chat_logging.json"
        self.history_dir = self.root_dir / ".claude" / "chat_history"
        
        self.config = self._load_config()
        self._ensure_directories()
    
    def _detect_root_dir(self) -> Path:
        """Auto-detect project root directory."""
        current = Path.cwd()
        while current != current.parent:
            if (current / ".claude").exists() or (current / "framework").exists():
                return current
            current = current.parent
        return Path.cwd()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load chat logging configuration."""
        if self.config_path.exists():
            with open(self.config_path) as f:
                return json.load(f)
        return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration when no config file exists."""
        return {
            "chat_logging": {
                "enabled": True,
                "auto_export": True,
                "storage": {"base_path": ".claude/chat_history", "format": "markdown"},
                "retention": {"max_days": 90, "auto_cleanup": True},
                "privacy": {"sanitize_secrets": True}
            }
        }
    
    def _ensure_directories(self):
        """Create necessary directories."""
        self.history_dir.mkdir(parents=True, exist_ok=True)
        (self.history_dir / "sessions").mkdir(exist_ok=True)
        (self.history_dir / "archives").mkdir(exist_ok=True)
        (self.history_dir / "exports").mkdir(exist_ok=True)
    
    def capture_session_context(self) -> Dict[str, Any]:
        """Capture current session context."""
        context = {
            "session_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "working_directory": str(Path.cwd()),
            "git_info": self._get_git_info(),
            "environment": self._get_environment_info(),
            "claude_info": self._get_claude_info()
        }
        return context
    
    def _get_git_info(self) -> Dict[str, Any]:
        """Get current git repository information."""
        try:
            git_info = {
                "branch": subprocess.check_output(
                    ["git", "branch", "--show-current"], 
                    text=True, stderr=subprocess.DEVNULL
                ).strip(),
                "commit": subprocess.check_output(
                    ["git", "rev-parse", "HEAD"], 
                    text=True, stderr=subprocess.DEVNULL
                ).strip()[:8],
                "status": subprocess.check_output(
                    ["git", "status", "--porcelain"], 
                    text=True, stderr=subprocess.DEVNULL
                ).strip(),
                "remote": subprocess.check_output(
                    ["git", "remote", "get-url", "origin"], 
                    text=True, stderr=subprocess.DEVNULL
                ).strip()
            }
            return git_info
        except (subprocess.CalledProcessError, FileNotFoundError):
            return {"error": "Not a git repository or git not available"}
    
    def _get_environment_info(self) -> Dict[str, Any]:
        """Get environment information."""
        return {
            "python_version": subprocess.check_output(
                ["python", "--version"], text=True
            ).strip(),
            "os": os.name,
            "platform": subprocess.check_output(
                ["uname", "-a"], text=True, stderr=subprocess.DEVNULL
            ).strip() if os.name != "nt" else "Windows"
        }
    
    def _get_claude_info(self) -> Dict[str, Any]:
        """Get Claude Code information if available."""
        try:
            # Try to get Claude Code version/info
            result = subprocess.check_output(
                ["claude", "--version"], text=True, stderr=subprocess.DEVNULL
            )
            return {"version": result.strip()}
        except (subprocess.CalledProcessError, FileNotFoundError):
            return {"version": "unknown"}
    
    def create_session_log(self, session_context: Dict[str, Any]) -> Path:
        """Create a new session log file."""
        session_id = session_context["session_id"]
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        
        filename = f"session_{timestamp}_{session_id[:8]}.md"
        session_file = self.history_dir / "sessions" / filename
        
        # Create session header
        header = self._generate_session_header(session_context)
        
        with open(session_file, "w") as f:
            f.write(header)
        
        console.print(f"[green]📝 Created session log: {session_file}[/green]")
        return session_file
    
    def _generate_session_header(self, context: Dict[str, Any]) -> str:
        """Generate session header with metadata."""
        git_info = context.get("git_info", {})
        
        header = f"""# Claude Code Chat Session
        
## Session Information
- **Session ID:** {context["session_id"]}
- **Timestamp:** {context["timestamp"]}
- **Working Directory:** `{context["working_directory"]}`

## Git Context
- **Branch:** {git_info.get("branch", "unknown")}
- **Commit:** {git_info.get("commit", "unknown")}
- **Status:** {"Clean" if not git_info.get("status") else "Modified files"}

## Environment
- **Python:** {context.get("environment", {}).get("python_version", "unknown")}
- **Platform:** {context.get("environment", {}).get("platform", "unknown")}
- **Claude:** {context.get("claude_info", {}).get("version", "unknown")}

---

## Chat History

"""
        return header
    
    def export_current_session(self, output_path: Optional[str] = None, no_input: bool = False) -> Path:
        """Export current Claude Code session (manual trigger)."""
        console.print("[blue]📤 Exporting current chat session...[/blue]")
        
        # Capture session context
        session_context = self.capture_session_context()
        
        # Create session log
        session_file = self.create_session_log(session_context)
        
        # Attempt to capture chat content using various methods
        if no_input:
            console.print("[yellow]⚠️  Running in non-interactive mode. Session metadata only.[/yellow]")
            chat_content = None
        else:
            chat_content = self._capture_chat_content()
        
        if chat_content:
            self._append_chat_content(session_file, chat_content)
        else:
            console.print("[yellow]⚠️  No chat content captured. Session metadata saved.[/yellow]")
        
        # Apply privacy filters
        if self.config["chat_logging"]["privacy"]["sanitize_secrets"]:
            self._sanitize_session_file(session_file)
        
        # Compress if enabled
        if self.config["chat_logging"]["storage"].get("compression", False):
            compressed_file = self._compress_session(session_file)
            session_file.unlink()  # Remove original
            session_file = compressed_file
        
        console.print(f"[green]✅ Session exported to: {session_file}[/green]")
        return session_file
    
    def _capture_chat_content(self) -> Optional[str]:
        """Attempt to capture chat content using available methods."""
        console.print("[yellow]💡 Attempting to capture chat from clipboard...[/yellow]")
        
        # Try clipboard first without prompting
        chat_content = self._try_clipboard_capture()
        if chat_content:
            return chat_content
        
        console.print("[yellow]💡 No chat content found in clipboard.[/yellow]")
        console.print("1. Select all chat content (Cmd+A or Ctrl+A)")
        console.print("2. Copy to clipboard (Cmd+C or Ctrl+C)")
        console.print("3. Run the command again")
        
        return None
    
    def _try_claude_cache_extraction(self) -> Optional[str]:
        """Try to extract chat from Claude Code cache/memory."""
        # Claude Code may store session data in ~/.claude/ or similar
        possible_cache_dirs = [
            Path.home() / ".claude",
            Path.home() / ".config" / "claude",
            Path.home() / "Library" / "Application Support" / "Claude",
        ]
        
        for cache_dir in possible_cache_dirs:
            if cache_dir.exists():
                # Look for session files, memory files, etc.
                for file_pattern in ["*session*", "*memory*", "*chat*", "*.log"]:
                    for cache_file in cache_dir.rglob(file_pattern):
                        try:
                            if cache_file.is_file() and cache_file.stat().st_size > 0:
                                # Check if recently modified (within last hour)
                                if datetime.fromtimestamp(cache_file.stat().st_mtime, tz=timezone.utc) > datetime.now(timezone.utc) - timedelta(hours=1):
                                    content = cache_file.read_text()
                                    if self._looks_like_chat_content(content):
                                        return content
                        except (PermissionError, UnicodeDecodeError):
                            continue
        
        return None
    
    def _try_clipboard_capture(self) -> Optional[str]:
        """Try to capture chat content from clipboard."""
        try:
            import pyperclip
            clipboard_content = pyperclip.paste()
            
            if not clipboard_content or len(clipboard_content) < 10:
                console.print("[red]❌ Clipboard is empty or too short[/red]")
                return None
            
            console.print(f"[green]✅ Captured {len(clipboard_content)} characters from clipboard[/green]")
            
            # Preview first few lines
            preview_lines = clipboard_content.split('\n')[:3]
            console.print("[blue]Preview:[/blue]")
            for line in preview_lines:
                console.print(f"  {line[:80]}{'...' if len(line) > 80 else ''}")
            
            console.print("[green]✅ Using clipboard content for chat export[/green]")
            return clipboard_content
                
        except ImportError:
            console.print("[red]❌ pyperclip not installed. Installing now...[/red]")
            try:
                import subprocess
                subprocess.check_call(["pip", "install", "pyperclip"])
                import pyperclip
                clipboard_content = pyperclip.paste()
                if clipboard_content and len(clipboard_content) > 10:
                    console.print(f"[green]✅ Captured {len(clipboard_content)} characters[/green]")
                    return clipboard_content
            except Exception as e:
                console.print(f"[red]❌ Could not install pyperclip: {e}[/red]")
        except Exception as e:
            console.print(f"[red]❌ Clipboard error: {e}[/red]")
        
        return None
    
    def _looks_like_chat_content(self, content: str) -> bool:
        """Heuristic to detect if content looks like a Claude chat."""
        indicators = [
            "Human:", "Assistant:", "User:", "Claude:",
            "```", "I'll help", "Let me", "I can", "Here's",
            "/agent:", "@claude", "function_calls"
        ]
        
        # Content should be substantial and contain chat indicators
        return (
            len(content) > 100 and
            sum(1 for indicator in indicators if indicator in content) >= 2
        )
    
    def _prompt_manual_input(self) -> Optional[str]:
        """Prompt user for manual chat input."""
        console.print("[yellow]💭 No automatic chat capture available[/yellow]")
        
        try:
            if click.confirm("Would you like to manually paste chat content?"):
                console.print("Paste your chat content (press Ctrl+D when done):")
                lines = []
                try:
                    while True:
                        line = input()
                        lines.append(line)
                except EOFError:
                    pass
                
                content = "\n".join(lines)
                if content.strip():
                    return content
        except (EOFError, KeyboardInterrupt):
            console.print("\n[yellow]Skipping manual input[/yellow]")
        
        return None
    
    def _append_chat_content(self, session_file: Path, content: str):
        """Append chat content to session file."""
        formatted_content = self._format_chat_content(content)
        
        with open(session_file, "a") as f:
            f.write("\n\n")
            f.write(formatted_content)
            f.write("\n\n---\n\n*Chat exported automatically by Claude Chat Logger*\n")
    
    def _format_chat_content(self, content: str) -> str:
        """Format chat content for markdown output."""
        # Basic formatting to make chat more readable
        formatted = content
        
        # Add proper spacing around Human/Assistant markers
        formatted = re.sub(r'^(Human|User):', r'### 👤 \1:', formatted, flags=re.MULTILINE)
        formatted = re.sub(r'^(Assistant|Claude):', r'### 🤖 \1:', formatted, flags=re.MULTILINE)
        
        # Ensure code blocks are properly formatted
        formatted = re.sub(r'```(\w+)?\n', r'```\1\n', formatted)
        
        return formatted
    
    def _sanitize_session_file(self, session_file: Path):
        """Remove sensitive information from session file."""
        content = session_file.read_text()
        
        # Remove patterns that look like secrets
        patterns = self.config.get("chat_logging", {}).get("privacy", {}).get("exclude_patterns", [])
        
        for pattern in patterns:
            # Redact lines containing sensitive patterns
            content = re.sub(
                rf'.*{pattern}.*',
                f'[REDACTED - {pattern.upper()} DETECTED]',
                content,
                flags=re.IGNORECASE
            )
        
        # Redact potential API keys, tokens, etc.
        content = re.sub(
            r'["\']?[a-zA-Z0-9]{20,}["\']?',
            '[REDACTED - POTENTIAL_TOKEN]',
            content
        )
        
        session_file.write_text(content)
    
    def _compress_session(self, session_file: Path) -> Path:
        """Compress session file."""
        compressed_file = session_file.with_suffix(session_file.suffix + ".gz")
        
        with open(session_file, "rb") as f_in:
            with gzip.open(compressed_file, "wb") as f_out:
                f_out.write(f_in.read())
        
        return compressed_file
    
    def list_sessions(self, limit: int = 20) -> List[Dict[str, Any]]:
        """List recent chat sessions."""
        sessions = []
        session_dir = self.history_dir / "sessions"
        
        if not session_dir.exists():
            return sessions
        
        for session_file in sorted(session_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            if session_file.suffix in [".md", ".gz"]:
                sessions.append({
                    "file": session_file,
                    "name": session_file.name,
                    "size": session_file.stat().st_size,
                    "modified": datetime.fromtimestamp(session_file.stat().st_mtime, tz=timezone.utc),
                    "compressed": session_file.suffix == ".gz"
                })
                
                if len(sessions) >= limit:
                    break
        
        return sessions
    
    def cleanup_old_sessions(self, days: Optional[int] = None) -> int:
        """Clean up old chat sessions."""
        days = days or self.config["chat_logging"]["retention"]["max_days"]
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        
        sessions_cleaned = 0
        session_dir = self.history_dir / "sessions"
        
        if not session_dir.exists():
            return 0
        
        archive_dir = self.history_dir / "archives"
        archive_dir.mkdir(exist_ok=True)
        
        for session_file in session_dir.iterdir():
            if session_file.is_file():
                file_date = datetime.fromtimestamp(session_file.stat().st_mtime, tz=timezone.utc)
                
                if file_date < cutoff_date:
                    # Archive instead of delete
                    archive_path = archive_dir / session_file.name
                    session_file.rename(archive_path)
                    sessions_cleaned += 1
        
        return sessions_cleaned
    
    def display_sessions(self, sessions: List[Dict[str, Any]]):
        """Display sessions in a formatted table."""
        if not sessions:
            console.print("[yellow]No chat sessions found.[/yellow]")
            return
        
        table = Table(title=f"Chat Sessions ({len(sessions)} found)")
        table.add_column("Session", style="cyan")
        table.add_column("Size", style="green")
        table.add_column("Modified", style="yellow")
        table.add_column("Compressed", style="blue")
        
        for session in sessions:
            size_kb = session["size"] / 1024
            modified_str = session["modified"].strftime("%Y-%m-%d %H:%M")
            compressed_str = "Yes" if session["compressed"] else "No"
            
            table.add_row(
                session["name"][:40] + "..." if len(session["name"]) > 40 else session["name"],
                f"{size_kb:.1f} KB",
                modified_str,
                compressed_str
            )
        
        console.print(table)


# CLI Commands

@click.group()
@click.option('--root-dir', help='Project root directory')
@click.pass_context
def cli(ctx, root_dir):
    """Claude Code Chat Logger CLI."""
    ctx.ensure_object(dict)
    ctx.obj['logger'] = ChatLogger(root_dir)


@cli.command()
@click.option('--output', '-o', help='Output file path')
@click.option('--no-input', is_flag=True, help='Skip interactive prompts')
@click.pass_context
def export(ctx, output, no_input):
    """Export current chat session."""
    logger = ctx.obj['logger']
    
    if not logger.config["chat_logging"]["enabled"]:
        console.print("[red]❌ Chat logging is disabled in configuration[/red]")
        return
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task("Exporting chat session...", total=None)
        session_file = logger.export_current_session(output, no_input)
        progress.remove_task(task)
    
    console.print(Panel(
        f"[green]✅ Chat session exported successfully[/green]\n"
        f"File: {session_file}\n"
        f"Size: {session_file.stat().st_size / 1024:.1f} KB",
        title="Export Complete",
        border_style="green"
    ))


@cli.command()
@click.option('--limit', '-l', default=20, help='Number of sessions to show')
@click.pass_context
def list(ctx, limit):
    """List recent chat sessions."""
    logger = ctx.obj['logger']
    sessions = logger.list_sessions(limit)
    logger.display_sessions(sessions)


@cli.command()
@click.option('--days', '-d', help='Days to retain (default: from config)')
@click.option('--dry-run', is_flag=True, help='Show what would be cleaned without doing it')
@click.pass_context
def cleanup(ctx, days, dry_run):
    """Clean up old chat sessions."""
    logger = ctx.obj['logger']
    
    if dry_run:
        console.print("[yellow]Dry run mode - no files will be moved[/yellow]")
    
    cleaned_count = logger.cleanup_old_sessions(days) if not dry_run else 0
    
    if cleaned_count > 0:
        console.print(f"[green]✅ Archived {cleaned_count} old chat sessions[/green]")
    else:
        console.print("[blue]No old sessions to clean up[/blue]")


@cli.command()
@click.argument('session_name')
@click.pass_context
def view(ctx, session_name):
    """View a specific chat session."""
    logger = ctx.obj['logger']
    session_file = logger.history_dir / "sessions" / session_name
    
    if not session_file.exists():
        # Try with .md extension
        session_file = session_file.with_suffix(".md")
        if not session_file.exists():
            console.print(f"[red]❌ Session not found: {session_name}[/red]")
            return
    
    if session_file.suffix == ".gz":
        # Decompress and display
        import gzip
        with gzip.open(session_file, "rt") as f:
            content = f.read()
    else:
        content = session_file.read_text()
    
    console.print(Panel(
        content,
        title=f"Chat Session: {session_name}",
        border_style="blue"
    ))


if __name__ == "__main__":
    cli()
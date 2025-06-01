#!/usr/bin/env python3
"""
🤖 Agent Name Setup Script - One-time agent naming system
Creates a locked agent name that cannot be overwritten once set.

Usage:
    python setup_agent_name.py "MyProjectAgent"
    python setup_agent_name.py --check
    python setup_agent_name.py --status
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime


class AgentNameSetup:
    """Manages one-time agent name setup with locking mechanism."""
    
    def __init__(self, project_root=None):
        """Initialize with project root directory."""
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.config_dir = self.project_root / ".agent_config"
        self.config_file = self.config_dir / "agent_name.json"
        self.env_file = self.config_dir / "agent_env.sh"
        
    def setup_directories(self):
        """Create configuration directories if they don't exist."""
        self.config_dir.mkdir(exist_ok=True)
        
    def check_existing_name(self):
        """Check if agent name is already set."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                return config.get('agent_name'), config.get('locked_at')
            except (json.JSONDecodeError, KeyError):
                return None, None
        return None, None
    
    def validate_agent_name(self, name):
        """Validate agent name format."""
        if not name:
            raise ValueError("Agent name cannot be empty")
        
        if len(name) < 3:
            raise ValueError("Agent name must be at least 3 characters")
        
        if len(name) > 50:
            raise ValueError("Agent name must be less than 50 characters")
        
        # Allow alphanumeric, underscores, hyphens
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', name):
            raise ValueError("Agent name can only contain letters, numbers, underscores, and hyphens")
        
        return True
    
    def set_agent_name(self, name, force=False):
        """Set agent name with locking mechanism."""
        # Check if already set
        existing_name, locked_at = self.check_existing_name()
        
        if existing_name and not force:
            raise ValueError(
                f"Agent name already set to '{existing_name}' at {locked_at}. "
                f"Cannot overwrite. Use --force to override (not recommended)."
            )
        
        # Validate new name
        self.validate_agent_name(name)
        
        # Setup directories
        self.setup_directories()
        
        # Create configuration
        config = {
            "agent_name": name,
            "project_directory": str(self.project_root.absolute()),
            "locked_at": datetime.now().isoformat(),
            "locked": True,
            "version": "1.0"
        }
        
        # Write configuration file
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Create environment file for sourcing
        env_content = f"""#!/bin/bash
# Agent Name Environment Configuration
# Generated at: {datetime.now().isoformat()}
# DO NOT EDIT - This file is auto-generated

export AGENT_NAME="{name}"
export AGENT_PROJECT_DIR="{self.project_root.absolute()}"
export AGENT_LOCKED="true"

# Usage: source .agent_config/agent_env.sh
echo "🤖 Agent name set to: $AGENT_NAME"
"""
        
        with open(self.env_file, 'w') as f:
            f.write(env_content)
        
        # Make env file executable
        os.chmod(self.env_file, 0o755)
        
        return name, config
    
    def get_status(self):
        """Get current agent naming status."""
        existing_name, locked_at = self.check_existing_name()
        
        status = {
            "configured": existing_name is not None,
            "agent_name": existing_name,
            "locked_at": locked_at,
            "project_directory": str(self.project_root.absolute()),
            "config_file": str(self.config_file),
            "env_file": str(self.env_file)
        }
        
        # Check environment variable
        env_name = os.getenv('AGENT_NAME')
        status["env_agent_name"] = env_name
        status["env_matches_config"] = env_name == existing_name
        
        return status


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="🤖 Agent Name Setup - One-time agent naming system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python setup_agent_name.py "MyProjectAgent"    # Set agent name
  python setup_agent_name.py --check             # Check current name
  python setup_agent_name.py --status            # Detailed status
  python setup_agent_name.py --force "NewName"   # Force override (careful!)
        """
    )
    
    parser.add_argument(
        'name', 
        nargs='?', 
        help='Agent name to set (3-50 characters, alphanumeric with _ and -)'
    )
    parser.add_argument(
        '--check', 
        action='store_true', 
        help='Check if agent name is already set'
    )
    parser.add_argument(
        '--status', 
        action='store_true', 
        help='Show detailed status information'
    )
    parser.add_argument(
        '--force', 
        action='store_true', 
        help='Force override existing name (use with caution)'
    )
    parser.add_argument(
        '--project-dir', 
        help='Project directory (defaults to current directory)'
    )
    
    args = parser.parse_args()
    
    try:
        setup = AgentNameSetup(args.project_dir)
        
        if args.check:
            name, locked_at = setup.check_existing_name()
            if name:
                print(f"✅ Agent name: {name}")
                print(f"🔒 Locked at: {locked_at}")
            else:
                print("❌ No agent name configured")
                print("💡 Run: python setup_agent_name.py \"YourAgentName\"")
        
        elif args.status:
            status = setup.get_status()
            print("🤖 Agent Name Status")
            print("=" * 40)
            print(f"Configured: {'✅' if status['configured'] else '❌'}")
            print(f"Agent Name: {status['agent_name'] or 'Not set'}")
            print(f"Locked At: {status['locked_at'] or 'N/A'}")
            print(f"Project Dir: {status['project_directory']}")
            print(f"Config File: {status['config_file']}")
            print(f"Env File: {status['env_file']}")
            print(f"Environment Variable: {status['env_agent_name'] or 'Not set'}")
            print(f"Env Matches Config: {'✅' if status['env_matches_config'] else '❌'}")
            
            if not status['env_matches_config'] and status['configured']:
                print(f"\n💡 To set environment variable:")
                print(f"   source {status['env_file']}")
        
        elif args.name:
            # Set the agent name
            name, config = setup.set_agent_name(args.name, force=args.force)
            
            print("🎉 Agent name configured successfully!")
            print("=" * 40)
            print(f"✅ Agent Name: {name}")
            print(f"📁 Project Directory: {config['project_directory']}")
            print(f"🔒 Locked At: {config['locked_at']}")
            print(f"📄 Config File: {setup.config_file}")
            print(f"🌍 Environment File: {setup.env_file}")
            
            print(f"\n💡 To activate in your shell:")
            print(f"   source {setup.env_file}")
            
            print(f"\n🤖 Your agent is now ready!")
            print(f"   Agent Name: {name}")
            
        else:
            parser.print_help()
    
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
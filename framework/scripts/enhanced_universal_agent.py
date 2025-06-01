#!/usr/bin/env python3
"""
🤖 Enhanced Universal Agent Client - Project-Locked Agent Names
Integrates with the agent naming system for secure, locked agent identification

This enhanced client:
1. Automatically detects configured agent names
2. Enforces project directory binding
3. Validates against the locked naming system
4. Provides clear error messages for naming conflicts
"""

import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentNameError(Exception):
    """Exception raised for agent naming issues."""
    pass


class ProjectLockedAgent:
    """
    🔒 Project-Locked Agent with Naming System Integration
    
    Features:
    - Automatic agent name detection from project configuration
    - Project directory binding enforcement
    - One agent per project directory restriction
    - Integration with environment variable system
    """
    
    def __init__(self, agent_name: str = None, project_dir: str = None, auto_detect: bool = True):
        """
        Initialize project-locked agent
        
        Args:
            agent_name: Agent name (optional if auto_detect=True)
            project_dir: Project directory (defaults to current directory)
            auto_detect: Auto-detect agent name from configuration
        """
        self.project_dir = Path(project_dir) if project_dir else Path.cwd()
        self.config_dir = self.project_dir / ".agent_config"
        self.config_file = self.config_dir / "agent_name.json"
        
        # Detect or validate agent name
        if auto_detect:
            self.agent_name = self._detect_agent_name(agent_name)
        else:
            self.agent_name = agent_name or self._detect_agent_name()
        
        self._validate_agent_setup()
        self._load_universal_client()
        
        logger.info(f"🔒 {self.agent_name} loaded with project-locked naming")
    
    def _detect_agent_name(self, provided_name: str = None) -> str:
        """Detect agent name from configuration or environment."""
        
        # Method 1: Check environment variable
        env_name = os.getenv('AGENT_NAME')
        
        # Method 2: Check configuration file
        config_name = None
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                config_name = config.get('agent_name')
            except (json.JSONDecodeError, KeyError):
                pass
        
        # Method 3: Use provided name
        detected_name = provided_name or env_name or config_name
        
        if not detected_name:
            raise AgentNameError(
                "🚨 No agent name configured!\n"
                f"Please run: python framework/scripts/setup_agent_name.py \"YourAgentName\"\n"
                f"Or set AGENT_NAME environment variable"
            )
        
        # Validate consistency between sources
        if env_name and config_name and env_name != config_name:
            raise AgentNameError(
                f"🚨 Agent name mismatch!\n"
                f"Environment: {env_name}\n"
                f"Config file: {config_name}\n"
                f"Please run: source {self.config_dir}/agent_env.sh"
            )
        
        if provided_name and config_name and provided_name != config_name:
            raise AgentNameError(
                f"🚨 Cannot override locked agent name!\n"
                f"Provided: {provided_name}\n"
                f"Locked name: {config_name}\n"
                f"Use the configured name or setup a new project"
            )
        
        return detected_name
    
    def _validate_agent_setup(self):
        """Validate agent configuration and project binding."""
        
        # Check if configuration exists
        if not self.config_file.exists():
            raise AgentNameError(
                f"🚨 Agent not configured for this project!\n"
                f"Project: {self.project_dir}\n"
                f"Please run: python framework/scripts/setup_agent_name.py \"{self.agent_name}\""
            )
        
        # Load and validate configuration
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
        except (json.JSONDecodeError, KeyError) as e:
            raise AgentNameError(f"🚨 Invalid agent configuration: {e}")
        
        # Validate project directory binding
        config_project_dir = Path(config.get('project_directory', ''))
        if config_project_dir.resolve() != self.project_dir.resolve():
            raise AgentNameError(
                f"🚨 Agent configured for different project!\n"
                f"Current project: {self.project_dir.resolve()}\n"
                f"Configured for: {config_project_dir.resolve()}\n"
                f"Each project needs its own agent configuration"
            )
        
        # Validate agent name matches
        config_name = config.get('agent_name')
        if config_name != self.agent_name:
            raise AgentNameError(
                f"🚨 Agent name mismatch in configuration!\n"
                f"Requested: {self.agent_name}\n"
                f"Configured: {config_name}"
            )
        
        # Store configuration
        self.config = config
        logger.info(f"✅ Agent configuration validated for {self.agent_name}")
    
    def _load_universal_client(self):
        """Load the universal agent client with our validated name."""
        
        # Try to import the universal client
        try:
            # Add global hub to path if needed
            global_hub_path = Path.home() / '.claude' / 'mcp-global-hub' / 'servers'
            if global_hub_path.exists():
                sys.path.insert(0, str(global_hub_path))
            
            # Also check local universal client
            local_client = self.project_dir / 'universal_agent_client.py'
            if local_client.exists():
                sys.path.insert(0, str(self.project_dir))
            
            from universal_agent_client import UniversalAgent
            
            # Initialize with validated name and project binding
            self.universal_client = UniversalAgent(
                agent_name=self.agent_name,
                agent_location=str(self.project_dir)
            )
            
            logger.info(f"🌐 {self.agent_name} connected to global network")
            
        except ImportError as e:
            logger.warning(f"⚠️ Global client unavailable: {e}")
            logger.info("🔄 Falling back to local agent communication")
            self.universal_client = None
    
    def say(self, message: str, priority: str = "normal"):
        """Send a message to the global network."""
        if self.universal_client:
            return self.universal_client.say(message, priority)
        else:
            # Fallback to local communication
            logger.info(f"💬 {self.agent_name}: {message}")
            return f"local_msg_{datetime.now().timestamp()}"
    
    def listen(self) -> List[Dict]:
        """Listen for messages from other agents."""
        if self.universal_client:
            return self.universal_client.listen()
        else:
            return []  # No messages in local mode
    
    def share(self, data: Dict):
        """Share data with other agents."""
        if self.universal_client:
            return self.universal_client.share(data)
        else:
            logger.info(f"📊 {self.agent_name} sharing: {data}")
            return f"local_share_{datetime.now().timestamp()}"
    
    def ask(self, question: str):
        """Ask a question to other agents."""
        if self.universal_client:
            return self.universal_client.ask(question)
        else:
            logger.info(f"❓ {self.agent_name} asks: {question}")
            return f"local_question_{datetime.now().timestamp()}"
    
    def respond(self, question_id: str, answer: str):
        """Respond to a question."""
        if self.universal_client:
            return self.universal_client.respond(question_id, answer)
        else:
            logger.info(f"💡 {self.agent_name} responds to {question_id}: {answer}")
    
    def collaborate(self, task: str, details: Dict = None):
        """Start a collaboration task."""
        if self.universal_client:
            return self.universal_client.collaborate(task, details or {})
        else:
            logger.info(f"🤝 {self.agent_name} collaborating on: {task}")
            return f"local_collab_{datetime.now().timestamp()}"
    
    def get_active_agents(self) -> List[Dict]:
        """Get list of active agents."""
        if self.universal_client:
            return self.universal_client.get_active_agents()
        else:
            return [{"name": self.agent_name, "location": str(self.project_dir)}]
    
    def status(self) -> Dict:
        """Get agent status information."""
        return {
            "agent_name": self.agent_name,
            "project_directory": str(self.project_dir),
            "config_file": str(self.config_file),
            "locked_at": self.config.get('locked_at'),
            "global_connected": self.universal_client is not None,
            "agent_id": f"{self.agent_name}@{self.project_dir.name}"
        }


def create_agent(agent_name: str = None, project_dir: str = None) -> ProjectLockedAgent:
    """
    🚀 Factory function to create a project-locked agent
    
    Usage:
        agent = create_agent()  # Auto-detect name
        agent = create_agent("MyAgent")  # Validate against config
        agent.say("Hello from locked agent!")
    """
    return ProjectLockedAgent(agent_name, project_dir)


# Convenience alias
Agent = ProjectLockedAgent


if __name__ == '__main__':
    """
    CLI interface for testing the enhanced agent client
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="🤖 Enhanced Universal Agent Client")
    parser.add_argument('--name', help='Agent name (auto-detected if not provided)')
    parser.add_argument('--test', action='store_true', help='Run basic connectivity test')
    parser.add_argument('--status', action='store_true', help='Show agent status')
    
    args = parser.parse_args()
    
    try:
        agent = create_agent(args.name)
        
        if args.status:
            status = agent.status()
            print("🤖 Agent Status")
            print("=" * 30)
            for key, value in status.items():
                print(f"{key}: {value}")
        
        elif args.test:
            print(f"🧪 Testing agent: {agent.agent_name}")
            
            # Test basic operations
            agent.say("🧪 Test message from enhanced agent client")
            
            status = agent.status()
            print(f"✅ Agent operational: {status['agent_id']}")
            
            active_agents = agent.get_active_agents()
            print(f"👥 Active agents: {len(active_agents)}")
        
        else:
            print(f"✅ Agent {agent.agent_name} ready!")
            print("💡 Use --test or --status for more information")
    
    except AgentNameError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
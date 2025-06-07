#!/usr/bin/env python3
"""
SpacetimeDB Operations - Direct database interaction tool for agents.

This script provides actual database operations for the agora-marketplace.
Designed to be used as a tool by AI agents for database interaction.

Database: agora-marketplace
Tables: Unified architecture as defined in THE PROTOCOL v5.0
"""

import subprocess
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any


class SpacetimeDB:
    """Direct interface to SpacetimeDB agora-marketplace."""
    
    def __init__(self):
        self.database = "agora-marketplace"
        self.agent_name = self._get_agent_name()
        
    def _get_agent_name(self) -> str:
        """Get agent name from configuration."""
        config_file = os.path.join(os.getcwd(), '.agent_config', 'agent_name.json')
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('agent_name', 'UnnamedAgent')
            except:
                pass
        
        return os.environ.get('AGENT_NAME', 'UnnamedAgent')
    
    def _run_spacetime_cmd(self, args: List[str]) -> Dict[str, Any]:
        """Run a spacetime command and return result."""
        try:
            result = subprocess.run(
                ["spacetime"] + args,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Command timeout",
                "stdout": "",
                "stderr": "Operation timed out after 30 seconds"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "stdout": "",
                "stderr": str(e)
            }
    
    # ===== Connection Operations =====
    
    def verify_connection(self) -> bool:
        """Verify connection to agora-marketplace."""
        result = self._run_spacetime_cmd(["logs", self.database, "--num-lines", "1"])
        return result["success"]
    
    def get_logs(self, lines: int = 50) -> str:
        """Get recent logs from agora-marketplace."""
        result = self._run_spacetime_cmd(["logs", self.database, "--num-lines", str(lines)])
        if result["success"]:
            return result["stdout"]
        return f"Error: {result['stderr']}"
    
    # ===== Agent Operations =====
    
    def register_agent(self, agent_type: str = "worker", capabilities: str = "") -> bool:
        """Register this agent in agora-marketplace."""
        args = [
            "call", self.database, "register_agent_capability",
            f'"{self.agent_name}"', f'"{agent_type}"', f'"{self.agent_name}"', 'null'
        ]
        
        result = self._run_spacetime_cmd(args)
        if result["success"]:
            print(f"✅ Agent '{self.agent_name}' registered successfully")
        else:
            print(f"❌ Registration failed: {result['stderr']}")
        
        return result["success"]
    
    def update_agent_status(self, status: str) -> bool:
        """Update agent status (active/inactive/busy)."""
        args = [
            "call", self.database, "update_agent_status",
            f'"{self.agent_name}"', f'"{status}"'
        ]
        
        result = self._run_spacetime_cmd(args)
        return result["success"]
    
    def send_heartbeat(self) -> bool:
        """Send heartbeat to maintain agent connection."""
        args = [
            "call", self.database, "agent_heartbeat",
            f'"{self.agent_name}"'
        ]
        
        result = self._run_spacetime_cmd(args)
        return result["success"]
    
    # ===== Event Operations =====
    
    def create_event(self, event_type: str, target_agent: str, data: Dict, priority: int = 1) -> bool:
        """Create a system event."""
        event_id = f"evt_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        args = [
            "call", self.database, "create_system_event",
            "--event_id", event_id,
            "--event_type", event_type,
            "--source_agent", self.agent_name,
            "--target_agent", target_agent,
            "--data", json.dumps(data),
            "--priority", str(priority)
        ]
        
        result = self._run_spacetime_cmd(args)
        if result["success"]:
            print(f"✅ Event created: {event_id}")
        else:
            print(f"❌ Event creation failed: {result['stderr']}")
        
        return result["success"]
    
    def announce(self, message: str, priority: int = 2) -> bool:
        """Send announcement to all agents."""
        return self.create_event(
            event_type="announcement",
            target_agent="all_agents",
            data={"message": message, "timestamp": datetime.now().isoformat()},
            priority=priority
        )
    
    # ===== Workflow Operations =====
    
    def create_workflow(self, workflow_type: str, assigned_agents: List[str], metadata: Dict) -> Optional[str]:
        """Create a new workflow."""
        workflow_id = f"wf_{workflow_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        args = [
            "call", self.database, "create_workflow",
            "--workflow_id", workflow_id,
            "--workflow_type", workflow_type,
            "--initiator_agent", self.agent_name,
            "--assigned_agents", json.dumps(assigned_agents),
            "--metadata", json.dumps(metadata)
        ]
        
        result = self._run_spacetime_cmd(args)
        if result["success"]:
            print(f"✅ Workflow created: {workflow_id}")
            return workflow_id
        else:
            print(f"❌ Workflow creation failed: {result['stderr']}")
            return None
    
    def update_workflow_status(self, workflow_id: str, status: str) -> bool:
        """Update workflow status."""
        args = [
            "call", self.database, "update_workflow_status",
            "--workflow_id", workflow_id,
            "--status", status
        ]
        
        result = self._run_spacetime_cmd(args)
        return result["success"]
    
    # ===== User Notification Operations =====
    
    def notify_user(self, user_id: str, notification_type: str, title: str, message: str, severity: str = "info") -> bool:
        """Send notification to user."""
        notification_id = f"notif_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        args = [
            "call", self.database, "create_user_notification",
            "--notification_id", notification_id,
            "--user_id", user_id,
            "--notification_type", notification_type,
            "--severity", severity,
            "--title", title,
            "--message", message
        ]
        
        result = self._run_spacetime_cmd(args)
        return result["success"]
    
    # ===== Task Queue Operations =====
    
    def create_task(self, task_type: str, payload: Dict, priority: int = 1) -> Optional[str]:
        """Create a task in the queue."""
        task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        args = [
            "call", self.database, "create_task",
            f'"{task_id}"', f'"{self.agent_name}"', f'"{task_type}"', f'"{priority}"', f'"{json.dumps(payload)}"'
        ]
        
        result = self._run_spacetime_cmd(args)
        if result["success"]:
            return task_id
        return None
    
    def complete_task(self, task_id: str) -> bool:
        """Mark task as completed."""
        args = [
            "call", self.database, "complete_task",
            "--task_id", task_id
        ]
        
        result = self._run_spacetime_cmd(args)
        return result["success"]
    
    # ===== Utility Functions =====
    
    def get_active_agents(self) -> List[str]:
        """Get list of active agents from logs."""
        logs = self.get_logs(100)
        agents = []
        
        for line in logs.split('\n'):
            if 'registered successfully' in line and 'Agent' in line:
                # Extract agent name from log line
                parts = line.split('Agent ')
                if len(parts) > 1:
                    agent_info = parts[1].split(' registered')[0]
                    agents.append(agent_info)
        
        return list(set(agents))  # Remove duplicates
    
    def system_status(self) -> Dict[str, Any]:
        """Get system status overview."""
        return {
            "database": self.database,
            "agent_name": self.agent_name,
            "connection": self.verify_connection(),
            "timestamp": datetime.now().isoformat()
        }


# ===== CLI Interface =====

def main():
    """Command-line interface for SpacetimeDB operations."""
    import argparse
    
    parser = argparse.ArgumentParser(description="SpacetimeDB Operations Tool")
    parser.add_argument("command", choices=[
        "status", "register", "heartbeat", "announce", "logs", "agents"
    ], help="Command to execute")
    parser.add_argument("--message", help="Message for announce command")
    parser.add_argument("--type", default="worker", help="Agent type for registration")
    parser.add_argument("--lines", type=int, default=50, help="Number of log lines")
    
    args = parser.parse_args()
    
    db = SpacetimeDB()
    
    if args.command == "status":
        status = db.system_status()
        print(f"\n🔍 System Status:")
        print(f"   Database: {status['database']}")
        print(f"   Agent: {status['agent_name']}")
        print(f"   Connected: {'✅' if status['connection'] else '❌'}")
        print(f"   Time: {status['timestamp']}")
        
    elif args.command == "register":
        if db.register_agent(agent_type=args.type):
            print("✅ Registration successful")
        else:
            print("❌ Registration failed")
            
    elif args.command == "heartbeat":
        if db.send_heartbeat():
            print("💓 Heartbeat sent")
        else:
            print("❌ Heartbeat failed")
            
    elif args.command == "announce":
        if not args.message:
            print("❌ Please provide --message for announcement")
            sys.exit(1)
        if db.announce(args.message):
            print("📢 Announcement sent")
        else:
            print("❌ Announcement failed")
            
    elif args.command == "logs":
        print(f"\n📜 Recent logs ({args.lines} lines):\n")
        print(db.get_logs(args.lines))
        
    elif args.command == "agents":
        agents = db.get_active_agents()
        print(f"\n👥 Active agents ({len(agents)}):")
        for agent in agents:
            print(f"   • {agent}")


if __name__ == "__main__":
    main()
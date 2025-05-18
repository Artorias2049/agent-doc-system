#!/usr/bin/env python3

import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Union
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentCommunication:
    def __init__(self, project_dir: str):
        self.project_dir = project_dir
        self.message_file = os.path.join(project_dir, "agent_messages.json")
        self._initialize_message_file()

    def _initialize_message_file(self):
        """Initialize the message file if it doesn't exist."""
        if not os.path.exists(self.message_file):
            initial_structure = {
                "messages": [],
                "last_updated": datetime.utcnow().isoformat(),
                "version": "1.0.0"
            }
            self._write_message_file(initial_structure)

    def _read_message_file(self) -> Dict:
        """Read the message file."""
        try:
            with open(self.message_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Message file not found at {self.message_file}")
            return {"messages": [], "last_updated": datetime.utcnow().isoformat(), "version": "1.0.0"}
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in message file at {self.message_file}")
            return {"messages": [], "last_updated": datetime.utcnow().isoformat(), "version": "1.0.0"}

    def _write_message_file(self, data: Dict):
        """Write to the message file."""
        try:
            with open(self.message_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error writing to message file: {e}")

    def send_message(self, message_type: str, content: Dict, sender: str) -> str:
        """Send a new message."""
        message_id = str(uuid.uuid4())
        message = {
            "id": message_id,
            "timestamp": datetime.utcnow().isoformat(),
            "sender": sender,
            "type": message_type,
            "content": content,
            "status": "pending"
        }

        data = self._read_message_file()
        data["messages"].append(message)
        data["last_updated"] = datetime.utcnow().isoformat()
        self._write_message_file(data)
        
        logger.info(f"Message sent with ID: {message_id}")
        return message_id

    def get_pending_messages(self) -> List[Dict]:
        """Get all pending messages."""
        data = self._read_message_file()
        return [msg for msg in data["messages"] if msg["status"] == "pending"]

    def update_message_status(self, message_id: str, status: str, response: Optional[Dict] = None):
        """Update message status and add response if provided."""
        data = self._read_message_file()
        for message in data["messages"]:
            if message["id"] == message_id:
                message["status"] = status
                if response:
                    message["response"] = response
                break
        data["last_updated"] = datetime.utcnow().isoformat()
        self._write_message_file(data)
        logger.info(f"Message {message_id} status updated to {status}")

    def cleanup_old_messages(self, days: int = 7):
        """Clean up messages older than specified days."""
        data = self._read_message_file()
        current_time = datetime.utcnow()
        
        data["messages"] = [
            msg for msg in data["messages"]
            if (current_time - datetime.fromisoformat(msg["timestamp"])).days <= days
        ]
        
        data["last_updated"] = current_time.isoformat()
        self._write_message_file(data)
        logger.info(f"Cleaned up messages older than {days} days")

def main():
    """Example usage of the AgentCommunication class."""
    # Example project directory
    project_dir = os.getcwd()
    agent_comm = AgentCommunication(project_dir)

    # Example: Send a test request
    test_request = {
        "test_type": "e2e",
        "test_file": "test_full_pipeline.py",
        "parameters": {
            "environment": "local",
            "verbose": True
        }
    }
    
    message_id = agent_comm.send_message(
        message_type="test_request",
        content=test_request,
        sender="e2e-test-agent"
    )
    
    # Example: Get pending messages
    pending_messages = agent_comm.get_pending_messages()
    print(f"Pending messages: {len(pending_messages)}")

if __name__ == "__main__":
    main() 
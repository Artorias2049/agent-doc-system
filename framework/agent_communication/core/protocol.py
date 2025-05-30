#!/usr/bin/env python3

import json
import os
import argparse
from datetime import datetime, UTC
from typing import Dict, Optional, List
import logging
from pathlib import Path
import yaml
import uuid

# Configure logging with a cleaner format
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'  # Only show the message, not the timestamp and level
)
logger = logging.getLogger(__name__)

class AgentProtocol:
    def __init__(self, agent_id: str, root_dir: str):
        self.agent_id = agent_id
        self.root_dir = root_dir
        self.message_dir = os.path.join(root_dir, "agent_communication", "history")
        self.message_file = os.path.join(self.message_dir, f"{agent_id}_messages.json")
        self.schema_file = os.path.join(root_dir, "schemas", "agent_communication.yml")
        self.schema = self._load_schema()
        self._initialize_protocol()

    def _load_schema(self) -> Dict:
        """Load the schema file."""
        try:
            with open(self.schema_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading schema file: {e}")
            raise

    def _initialize_protocol(self):
        """Initialize the protocol and create necessary directories."""
        os.makedirs(self.message_dir, exist_ok=True)
        if not os.path.exists(self.message_file):
            self._write_messages({
                "agent_id": self.agent_id,
                "messages": [],
                "last_updated": datetime.now(UTC).isoformat(),
                "version": "1.0.0"
            })

    def _read_messages(self) -> Dict:
        """Read messages from the message file."""
        try:
            with open(self.message_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._initialize_protocol()
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in message file: {self.message_file}")
            return self._initialize_protocol()

    def _write_messages(self, data: Dict):
        """Write messages to the message file."""
        try:
            with open(self.message_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error writing to message file: {e}")

    def validate_message(self, message: Dict) -> List[str]:
        """Validate a message against the schema."""
        errors = []
        required_fields = self.schema["message_schema"]["required_fields"]
        for field, field_schema in required_fields.items():
            if field not in message:
                errors.append(f"Missing required field: {field}")
            else:
                if field_schema["type"] == "string" and not isinstance(message[field], str):
                    errors.append(f"Field {field} must be a string")
                if field == "id" and not self._validate_uuid(message[field]):
                    errors.append("Invalid UUID format for id field")
                if field == "timestamp" and not self._validate_timestamp(message[field]):
                    errors.append("Invalid timestamp format")
                if field == "type" and message[field] not in ["test_request", "test_result", "status_update", "context_update"]:
                    errors.append(f"Invalid message type: {message['type']}")
                if field == "status" and message[field] not in ["pending", "processed", "failed"]:
                    errors.append(f"Invalid status: {message['status']}")
        return errors

    def _validate_uuid(self, uuid_str: str) -> bool:
        """Validate UUID format."""
        try:
            uuid.UUID(uuid_str)
            return True
        except ValueError:
            return False

    def _validate_timestamp(self, timestamp: str) -> bool:
        """Validate ISO-8601 timestamp format."""
        try:
            datetime.fromisoformat(timestamp)
            return True
        except ValueError:
            return False

    def send_message(self, target_agent: str, message_type: str, content: Dict) -> str:
        """Send a message to another agent."""
        message = {
            "id": f"{self.agent_id}_{datetime.now(UTC).timestamp()}",
            "timestamp": datetime.now(UTC).isoformat(),
            "sender": self.agent_id,
            "target": target_agent,
            "type": message_type,
            "content": content,
            "status": "pending"
        }
        errors = self.validate_message(message)
        if errors:
            logger.error(f"Message validation failed: {errors}")
            raise ValueError(f"Invalid message: {errors}")
        data = self._read_messages()
        data["messages"].append(message)
        data["last_updated"] = datetime.now(UTC).isoformat()
        self._write_messages(data)
        logger.info(f"Message sent to {target_agent}: {message['id']}")
        return message["id"]

    def get_pending_messages(self) -> list:
        """Get all pending messages for this agent."""
        data = self._read_messages()
        return [msg for msg in data["messages"] 
                if msg["status"] == "pending" and msg["target"] == self.agent_id]

    def update_message_status(self, message_id: str, status: str, response: Optional[Dict] = None):
        """Update the status of a message."""
        data = self._read_messages()
        for message in data["messages"]:
            if message["id"] == message_id:
                message["status"] = status
                if response:
                    message["response"] = response
                break
        data["last_updated"] = datetime.now(UTC).isoformat()
        self._write_messages(data)
        logger.info(f"Message {message_id} status updated to {status}")

    def cleanup_old_messages(self, days: int = 7):
        """Remove messages older than specified days."""
        data = self._read_messages()
        current_time = datetime.now(UTC)
        data["messages"] = [
            msg for msg in data["messages"]
            if (current_time - datetime.fromisoformat(msg["timestamp"])).days <= days
        ]
        data["last_updated"] = current_time.isoformat()
        self._write_messages(data)
        logger.info(f"Cleaned up messages older than {days} days")

def main():
    """Interactive usage of the AgentProtocol class."""
    parser = argparse.ArgumentParser(description='Agent Communication System')
    parser.add_argument('--action', choices=['send', 'read', 'cleanup'], required=True,
                      help='Action to perform: send, read, or cleanup messages')
    parser.add_argument('--agent-id', required=True, help='Agent ID')
    parser.add_argument('--root-dir', default=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                      help='Root directory of the project')
    parser.add_argument('--type', help='Message type (required for send action)')
    parser.add_argument('--target', help='Target agent name (required for send action)')
    parser.add_argument('--content', help='Message content as JSON string (required for send action)')
    parser.add_argument('--days', type=int, default=7, help='Days threshold for cleanup (default: 7)')
    
    args = parser.parse_args()
    
    # Initialize agent protocol
    agent_protocol = AgentProtocol(agent_id=args.agent_id, root_dir=args.root_dir)
    
    if args.action == 'send':
        if not all([args.type, args.target, args.content]):
            parser.error("--type, --target, and --content are required for send action")
        
        try:
            content = json.loads(args.content)
        except json.JSONDecodeError:
            parser.error("--content must be a valid JSON string")
        
        message_id = agent_protocol.send_message(
            target_agent=args.target,
            message_type=args.type,
            content=content
        )
        print(f"Message sent successfully with ID: {message_id}")
        print(f"Message file location: {os.path.abspath(agent_protocol.message_file)}")
        
    elif args.action == 'read':
        pending_messages = agent_protocol.get_pending_messages()
        if not pending_messages:
            print("No pending messages found.")
        else:
            print(f"\nFound {len(pending_messages)} pending messages in {os.path.abspath(agent_protocol.message_file)}:")
            for msg in pending_messages:
                print("\n" + "="*50)
                print(f"Message ID: {msg['id']}")
                print(f"Type: {msg['type']}")
                print(f"Sender: {msg['sender']}")
                if msg.get('target'):
                    print(f"Target: {msg['target']}")
                print(f"Timestamp: {msg['timestamp']}")
                print(f"Content: {json.dumps(msg['content'], indent=2)}")
                print("="*50)
                
    elif args.action == 'cleanup':
        agent_protocol.cleanup_old_messages(days=args.days)
        print(f"Cleaned up messages older than {args.days} days from {os.path.abspath(agent_protocol.message_file)}")

if __name__ == "__main__":
    main() 
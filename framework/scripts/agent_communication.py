#!/usr/bin/env python3

import json
import os
import uuid
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Union
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Hardcoded paths for consistency across all agents
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MESSAGE_FILE = os.path.join(PROJECT_ROOT, "agent_communication", "history", "agent_messages.json")

class AgentCommunication:
    def __init__(self, read_file: Optional[str] = None):
        """
        Initialize AgentCommunication.
        Args:
            read_file: Optional path to read messages from. If not provided, uses the default message file.
        """
        self.message_file = read_file if read_file else MESSAGE_FILE
        self._initialize_message_file()

    def _initialize_message_file(self):
        """Initialize the message file if it doesn't exist."""
        # Ensure the directory exists
        os.makedirs(os.path.dirname(os.path.abspath(self.message_file)), exist_ok=True)
        
        if not os.path.exists(self.message_file):
            initial_structure = {
                "messages": [],
                "last_updated": datetime.utcnow().isoformat(),
                "version": "1.0.0"
            }
            self._write_message_file(initial_structure)
            logger.info(f"Initialized message file at: {os.path.abspath(self.message_file)}")

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

    def send_message(self, message_type: str, content: Dict, sender: str, target: str = None) -> str:
        """Send a new message."""
        if message_type not in ["test_request", "test_result", "status_update", "context_update"]:
            raise ValueError(f"Invalid message type: {message_type}. Must be one of: test_request, test_result, status_update, context_update")
            
        message_id = str(uuid.uuid4())
        message = {
            "id": message_id,
            "timestamp": datetime.utcnow().isoformat(),
            "sender": sender,
            "target": target,
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

    def get_pending_messages(self, target: str = None) -> List[Dict]:
        """Get all pending messages, optionally filtered by target."""
        data = self._read_message_file()
        messages = [msg for msg in data["messages"] if msg["status"] == "pending"]
        if target:
            messages = [msg for msg in messages if msg["target"] == target]
        return messages

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
    """Interactive usage of the AgentCommunication class."""
    parser = argparse.ArgumentParser(description='Agent Communication System')
    parser.add_argument('--action', choices=['send', 'read', 'cleanup'], required=True,
                      help='Action to perform: send, read, or cleanup messages')
    parser.add_argument('--type', help='Message type (required for send action)')
    parser.add_argument('--sender', help='Sender name (required for send action)')
    parser.add_argument('--target', help='Target agent name (optional for send action)')
    parser.add_argument('--content', help='Message content as JSON string (required for send action)')
    parser.add_argument('--days', type=int, default=7, help='Days threshold for cleanup (default: 7)')
    parser.add_argument('--read-file', help='Path to read messages from (only for read action)')
    
    args = parser.parse_args()
    
    # Initialize agent communication
    agent_comm = AgentCommunication(read_file=args.read_file if args.action == 'read' else None)
    
    if args.action == 'send':
        if not all([args.type, args.sender, args.content]):
            parser.error("--type, --sender, and --content are required for send action")
        
        try:
            content = json.loads(args.content)
        except json.JSONDecodeError:
            parser.error("--content must be a valid JSON string")
        
        message_id = agent_comm.send_message(
            message_type=args.type,
            content=content,
            sender=args.sender,
            target=args.target
        )
        print(f"Message sent successfully with ID: {message_id}")
        print(f"Message file location: {os.path.abspath(MESSAGE_FILE)}")
        
    elif args.action == 'read':
        pending_messages = agent_comm.get_pending_messages(target=args.target)
        if not pending_messages:
            print("No pending messages found.")
        else:
            print(f"\nFound {len(pending_messages)} pending messages in {os.path.abspath(agent_comm.message_file)}:")
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
        agent_comm.cleanup_old_messages(days=args.days)
        print(f"Cleaned up messages older than {args.days} days from {os.path.abspath(MESSAGE_FILE)}")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Agent Command Wrapper
Provides a clean interface to agent commands for slash command integration.
"""

import sys
import os
import json
from pathlib import Path

# Add framework path to imports
framework_path = Path(__file__).parent.parent.parent / "framework"
sys.path.insert(0, str(framework_path))

# Try to import the enhanced protocol
try:
    from agent_communication.core.enhanced_protocol import EnhancedAgentProtocol
    from agent_communication.core.models import AgentMessage, MessageType
    PROTOCOL_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import enhanced protocol: {e}")
    PROTOCOL_AVAILABLE = False


def main():
    """Main entry point for agent commands."""
    if not PROTOCOL_AVAILABLE:
        print("Error: Enhanced protocol not available")
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("Usage: agent_wrapper.py <command> [args...]")
        print("Commands: send, read, validate, cleanup")
        sys.exit(1)
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    try:
        # Initialize protocol
        protocol = EnhancedAgentProtocol()
        
        if command == "send":
            handle_send_command(protocol, args)
        elif command == "read":
            handle_read_command(protocol, args)
        elif command == "validate":
            handle_validate_command(protocol, args)
        elif command == "cleanup":
            handle_cleanup_command(protocol, args)
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error executing command: {e}")
        sys.exit(1)


def handle_send_command(protocol, args):
    """Handle send command."""
    if len(args) < 3:
        print("Usage: send <message_type> <sender> <content_json>")
        print("Example: send test_request agent1 '{\"test_type\": \"unit\"}'")
        return
    
    message_type = args[0]
    sender = args[1] 
    content_json = args[2]
    
    # Use CLI directly for send operations
    import subprocess
    import sys
    
    script_path = Path(__file__).parent.parent.parent / "framework" / "agent_communication" / "core" / "enhanced_protocol.py"
    cmd = [sys.executable, str(script_path), "--agent-id", sender, "send", "--type", message_type, "--content", content_json]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    if result.returncode == 0:
        print(f"✅ Message sent successfully: {message_type}")
    else:
        print(f"❌ Failed to send message: {message_type}")


def handle_read_command(protocol, args):
    """Handle read command."""
    # Use CLI directly for read operations
    import subprocess
    import sys
    
    script_path = Path(__file__).parent.parent.parent / "framework" / "agent_communication" / "core" / "enhanced_protocol.py"
    cmd = [sys.executable, str(script_path), "--agent-id", "system", "read"] + args
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)


def handle_validate_command(protocol, args):
    """Handle validate command."""
    target = args[0] if args else "all"
    print(f"🔍 Validating {target}...")
    
    # Basic validation
    messages = protocol.read_messages()
    valid_count = 0
    invalid_count = 0
    
    for msg in messages:
        try:
            # Simple validation check
            required_fields = ['id', 'timestamp', 'sender', 'type', 'content']
            if all(field in msg for field in required_fields):
                valid_count += 1
            else:
                invalid_count += 1
        except:
            invalid_count += 1
    
    print(f"✅ Valid messages: {valid_count}")
    print(f"❌ Invalid messages: {invalid_count}")


def handle_cleanup_command(protocol, args):
    """Handle cleanup command."""
    days = int(args[0]) if args else 7
    print(f"🧹 Cleaning up messages older than {days} days...")
    
    cleaned = protocol.cleanup_old_messages(days)
    print(f"✅ Cleaned up {cleaned} old messages")


if __name__ == "__main__":
    main()
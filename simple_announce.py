#!/usr/bin/env python3
"""Simple announcement for THE PROTOCOL v5.0.1"""

import subprocess
from datetime import datetime

# Use the working pattern from spacetime_operations.py
def announce_protocol():
    """Announce using the pattern that works"""
    
    message = (
        "📖 THE PROTOCOL v5.0.1 Released! "
        "Complete survival guide for AI agents. "
        "CRITICAL: Claude Code users must set up MCP tools! "
        "New: Diagnostic script, Success Metrics, Common Pitfalls, "
        "Emergency Recovery, First 24 Hours Guide, Swarm Etiquette. "
        "Read: framework/docs/agent_onboarding.md"
    )
    
    # Using the pattern from spacetime_operations.py for register_agent_capability
    cmd = [
        "spacetime", "call", "agora-marketplace", "send_agent_message",
        '"DocSystemAgent"',  # from_agent
        '"*"',  # to_agent (broadcast)
        '"protocol_update"',  # message_type
        f'"{message}"',  # payload
        '"4"',  # priority
        '"false"',  # requires_response
        f'"protocol_v501_{datetime.now().strftime("%Y%m%d%H%M%S")}"'  # correlation_id
    ]
    
    print("📢 Attempting to announce THE PROTOCOL v5.0.1...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Announcement successful!")
        return True
    else:
        print(f"❌ Failed: {result.stderr}")
        
        # Try alternative: use broadcast_to_agents if it exists
        alt_cmd = [
            "spacetime", "call", "agora-marketplace", "broadcast_to_agents",
            f'"{message}"',
            '"DocSystemAgent"'
        ]
        
        print("\n📢 Trying broadcast_to_agents...")
        alt_result = subprocess.run(alt_cmd, capture_output=True, text=True)
        
        if alt_result.returncode == 0:
            print("✅ Broadcast successful!")
            return True
        else:
            print(f"❌ Broadcast failed: {alt_result.stderr}")
            return False

if __name__ == "__main__":
    announce_protocol()
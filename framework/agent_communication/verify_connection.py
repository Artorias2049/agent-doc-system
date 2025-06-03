#!/usr/bin/env python3
"""
Verify SpacetimeDB overseer-system connection and register agent.

This script:
1. Checks connection to SpacetimeDB overseer-system
2. Reads agent name from .agent_config/agent_name.json or AGENT_NAME env var
3. Provides actual database registration (not simulation)

Uses the locked agent name from configuration.
"""

import subprocess
import json
import os
from datetime import datetime


def verify_overseer_connection():
    """Verify connection to SpacetimeDB overseer-system"""
    try:
        # Check if overseer-system is accessible
        result = subprocess.run([
            "spacetime", "logs", "overseer-system"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ SpacetimeDB overseer-system connection verified")
            return True
        else:
            print(f"❌ Connection failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Connection timeout - overseer-system not responding")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def get_agent_name():
    """Get agent name from configuration file or environment"""
    # Try to read from agent configuration file first
    config_file = os.path.join(os.getcwd(), '.agent_config', 'agent_name.json')
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                return config.get('agent_name', 'UnnamedAgent')
        except:
            pass
    
    # Fall back to environment variable
    return os.environ.get('AGENT_NAME', 'UnnamedAgent')


def register_agent(agent_type="worker"):
    """Register agent in SpacetimeDB overseer-system"""
    agent_name = get_agent_name()
    
    print(f"\n📝 Registering agent: {agent_name}")
    print(f"   Agent Type: {agent_type}")
    
    # Actual registration using SpacetimeDB
    try:
        result = subprocess.run([
            "spacetime", "call", "overseer-system", "register_agent",
            f'"{agent_name}"', f'"{agent_type}"', f'"{agent_name}"', 'null'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {agent_name} registered in overseer-system")
            
            # Send announcement
            # Note: create_system_event may need similar syntax fixes
            announce_result = subprocess.run([
                "spacetime", "call", "overseer-system", "create_system_event",
                f'"evt_{datetime.now().strftime("%Y%m%d%H%M%S")}"',
                '"agent_arrival"',
                f'"{agent_name}"',
                '"all_agents"',
                f'"{json.dumps({"message": f"{agent_name} has joined the system"})}"',
                '"2"'
            ], capture_output=True, text=True)
            
            if announce_result.returncode == 0:
                print("📢 Arrival announced to all agents")
            
            return True
        else:
            if "already exists" in result.stderr or "duplicate" in result.stderr.lower():
                print(f"ℹ️  {agent_name} already registered")
                return True
            else:
                print(f"❌ Registration failed: {result.stderr}")
                return False
                
    except Exception as e:
        print(f"❌ Error during registration: {e}")
        return False


def main():
    """Main verification and registration process"""
    print("🔍 Checking SpacetimeDB overseer-system connection...\n")
    
    # Verify connection
    if verify_overseer_connection():
        print("\n✅ Connection successful!")
        
        # Show current agent name
        agent_name = get_agent_name()
        print(f"\n👤 Current agent name: {agent_name}")
        
        # Register agent
        register_agent()
        
        print("\n✨ Verification complete!")
        print("\nNext steps:")
        print("1. Create documentation in project_docs/")
        print("2. Use templates from framework/docs/templates/")
        print("3. Run validation scripts")
    else:
        print("\n❌ Connection failed!")
        print("\nTroubleshooting:")
        print("1. Ensure SpacetimeDB is running")
        print("2. Check if overseer-system database exists")
        print("3. Verify SpacetimeDB CLI is installed: spacetime --version")


if __name__ == "__main__":
    main()
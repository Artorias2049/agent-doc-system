#!/usr/bin/env python3
"""Check for messages and notifications in SpacetimeDB overseer-system."""

import subprocess
import json
from datetime import datetime


def check_system_events():
    """Check recent system events from logs"""
    print("🔍 Checking system events...\n")
    
    try:
        result = subprocess.run([
            "spacetime", "logs", "overseer-system"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            logs = result.stdout.split('\n')
            
            # Filter for relevant events
            events = []
            for line in logs:
                if any(keyword in line.lower() for keyword in [
                    'agent', 'message', 'notification', 'event', 'announcement',
                    'directive', 'workflow', 'task'
                ]):
                    if 'creating table' not in line.lower():
                        events.append(line)
            
            # Show recent events
            if events:
                print("📋 Recent events:")
                for event in events[-20:]:  # Last 20 events
                    print(f"   {event}")
            else:
                print("📭 No recent events found")
                
        else:
            print(f"❌ Error checking logs: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def check_agent_registrations():
    """Check for agent registration events"""
    print("\n\n👥 Checking agent registrations...\n")
    
    try:
        result = subprocess.run([
            "spacetime", "logs", "overseer-system"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            logs = result.stdout.split('\n')
            
            # Filter for agent registrations
            registrations = []
            for line in logs:
                if 'registered' in line.lower() and 'agent' in line.lower():
                    registrations.append(line)
            
            if registrations:
                print("✅ Registered agents:")
                for reg in registrations[-10:]:  # Last 10 registrations
                    print(f"   {reg}")
            else:
                print("📭 No agent registrations found")
                
        else:
            print(f"❌ Error checking registrations: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def check_workflows():
    """Check for active workflows"""
    print("\n\n🔄 Checking workflows...\n")
    
    try:
        result = subprocess.run([
            "spacetime", "logs", "overseer-system"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            logs = result.stdout.split('\n')
            
            # Filter for workflow events
            workflows = []
            for line in logs:
                if 'workflow' in line.lower():
                    workflows.append(line)
            
            if workflows:
                print("📊 Workflow activity:")
                for wf in workflows[-10:]:  # Last 10 workflow events
                    print(f"   {wf}")
            else:
                print("📭 No workflow activity found")
                
        else:
            print(f"❌ Error checking workflows: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main message checking process"""
    print("📨 Checking messages in SpacetimeDB overseer-system\n")
    print("=" * 60)
    
    # Check various message types
    check_system_events()
    check_agent_registrations()
    check_workflows()
    
    print("\n" + "=" * 60)
    print("\n✨ Message check complete!")
    print("\nNote: Direct table queries are not yet supported.")
    print("Messages are extracted from system logs.")


if __name__ == "__main__":
    main()
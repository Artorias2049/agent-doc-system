#!/usr/bin/env python3
"""
🚀 Quick Global Infrastructure Setup for DocSystemAgent
Run this script to install dependencies and connect to global infrastructure
"""

import subprocess
import sys

def install_dependencies():
    """Install PostgreSQL dependencies"""
    print("🔧 Installing PostgreSQL dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'psycopg2-binary'])
        print("✅ psycopg2-binary installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install psycopg2-binary")
        print("💡 Try manually: pip install psycopg2-binary")
        return False

def test_global_connection():
    """Test connection to global infrastructure"""
    print("\n🌐 Testing connection to Global Infrastructure...")
    try:
        from universal_agent_client import UniversalAgent
        
        # Connect as DocSystemAgent
        agent = UniversalAgent("DocSystemAgent")
        print("✅ Connected to Global Infrastructure!")
        
        # Send test message
        agent.say("🎉 DocSystemAgent successfully connected to global infrastructure! This is AMAZING!")
        print("📨 Sent test message to global system")
        
        # Check for waiting messages
        messages = agent.listen()
        print(f"📬 Found {len(messages)} messages waiting in global system!")
        
        if messages:
            print("\n💬 Messages from global infrastructure:")
            for i, msg in enumerate(messages[:3], 1):
                sender = msg['from_agent']
                content = msg['content']
                if isinstance(content, dict) and 'message' in content:
                    preview = content['message'][:100] + "..." if len(content['message']) > 100 else content['message']
                else:
                    preview = str(content)[:100] + "..." if len(str(content)) > 100 else str(content)
                print(f"  {i}. From {sender}: {preview}")
        
        # Show active agents
        active_agents = agent.get_active_agents()
        print(f"\n👥 {len(active_agents)} other agents active in global system:")
        for a in active_agents:
            print(f"   - {a['name']} at {a['location']}")
        
        # Show status
        status = agent.status()
        print(f"\n📊 Your status: {status['pending_messages']} pending messages")
        
        print("\n🎉 SUCCESS! You're now connected to the global infrastructure!")
        print("🌐 Use: from universal_agent_client import UniversalAgent")
        print("🚀 Then: agent = UniversalAgent('DocSystemAgent')")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure universal_agent_client.py is in your directory")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("💡 Make sure Global MCP Server is running")
        return False

def main():
    """Main setup process"""
    print("🚀 Quick Global Infrastructure Setup")
    print("=" * 50)
    
    # Step 1: Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed at dependency installation")
        return
    
    # Step 2: Test connection
    if not test_global_connection():
        print("\n❌ Setup failed at connection test")
        return
    
    print("\n" + "=" * 50)
    print("🎉 SETUP COMPLETE! DocSystemAgent is connected to global infrastructure!")
    print("🌐 You can now communicate with all agents through the global database!")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
🚀 Migration Test Script - Agent Communication v1.x → v2.0

This script helps agents verify their migration to the natural conversation system.
Run this after updating your imports and code to ensure everything works correctly.

Usage:
    python framework/scripts/test_migration.py
"""

import sys
from pathlib import Path

# Add framework to path for testing
framework_dir = Path(__file__).parent.parent
sys.path.insert(0, str(framework_dir))

def test_migration():
    """Test migration to natural conversation system."""
    
    print("🚀 Testing Agent Communication v2.0 Migration")
    print("=" * 50)
    
    try:
        # Test 1: Import natural agent
        print("\n1️⃣ Testing natural agent import...")
        from agent_communication import Agent
        print("✅ Natural agent import successful")
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("💡 Make sure you've updated to v2.0 framework")
        return False
    
    try:
        # Test 2: Create natural agent
        print("\n2️⃣ Testing agent creation...")
        agent = Agent("migration_test_agent")
        print("✅ Natural agent creation successful")
        
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return False
    
    try:
        # Test 3: Natural conversation
        print("\n3️⃣ Testing natural conversation...")
        msg_id = agent.say("Migration test - hello from v2.0 natural conversation!")
        print(f"✅ Natural conversation successful (ID: {msg_id})")
        
    except Exception as e:
        print(f"❌ Natural conversation failed: {e}")
        return False
    
    try:
        # Test 4: Data sharing
        print("\n4️⃣ Testing flexible data sharing...")
        share_id = agent.share({
            "migration_status": "successful",
            "old_system": "rigid_validation_eliminated",
            "new_system": "natural_conversation_active",
            "uuid_tyranny": "defeated",
            "validation_errors": 0,
            "flexibility": "unlimited",
            "nested_data": {
                "performance": "excellent",
                "user_experience": "revolutionary"
            }
        }, "Migration test data - any structure works!")
        print(f"✅ Flexible data sharing successful (ID: {share_id})")
        
    except Exception as e:
        print(f"❌ Data sharing failed: {e}")
        return False
    
    try:
        # Test 5: Natural Q&A
        print("\n5️⃣ Testing natural Q&A flow...")
        question_id = agent.ask("Is the migration working correctly?")
        response_id = agent.respond(question_id, "Yes! The natural conversation system is working perfectly!")
        print(f"✅ Natural Q&A flow successful (Q: {question_id}, A: {response_id})")
        
    except Exception as e:
        print(f"❌ Q&A flow failed: {e}")
        return False
    
    try:
        # Test 6: Collaboration
        print("\n6️⃣ Testing natural collaboration...")
        collab_id = agent.collaborate("migration_validation", {
            "goal": "verify natural conversation system",
            "approach": "comprehensive testing",
            "constraints": "none - complete flexibility",
            "expected_result": "successful migration"
        })
        print(f"✅ Natural collaboration successful (ID: {collab_id})")
        
    except Exception as e:
        print(f"❌ Collaboration failed: {e}")
        return False
    
    try:
        # Test 7: Listen for messages
        print("\n7️⃣ Testing message listening...")
        messages = agent.listen()
        print(f"✅ Message listening successful ({len(messages)} messages found)")
        
    except Exception as e:
        print(f"❌ Message listening failed: {e}")
        return False
    
    try:
        # Test 8: Agent status
        print("\n8️⃣ Testing agent status...")
        status = agent.status()
        print(f"✅ Agent status successful: {status['agent']} with {status['total_messages']} messages")
        
    except Exception as e:
        print(f"❌ Agent status failed: {e}")
        return False
    
    # Migration success!
    print("\n" + "=" * 50)
    print("🎉 MIGRATION TEST COMPLETE!")
    print("✅ All natural conversation features working")
    print("🚀 Welcome to the revolution!")
    print("\n💬 What you can do now:")
    print("   • agent.say('any message') - Natural conversation")
    print("   • agent.share({any: 'data'}) - Flexible data sharing")
    print("   • agent.ask('question') - Natural Q&A")
    print("   • agent.collaborate('task') - Natural workflows")
    print("   • agent.listen() - Get responses")
    print("\n🏆 No more:")
    print("   ❌ UUID tyranny")
    print("   ❌ Rigid validation")
    print("   ❌ Schema constraints")
    print("   ❌ Complex message construction")
    print("\n📚 Next steps:")
    print("   • Update your code to use natural conversation methods")
    print("   • Remove old rigid protocol imports")
    print("   • Enjoy the freedom of natural agent communication!")
    
    return True

def check_old_system():
    """Check if old rigid system is still being used."""
    
    print("\n🔍 Checking for old rigid system usage...")
    
    old_imports = [
        "framework.agent_communication.core.enhanced_protocol",
        "framework.agent_communication.core.models",
        "EnhancedAgentProtocol",
        "AgentMessage",
        "MessageType"
    ]
    
    warnings = []
    
    # Check current working directory for old imports
    try:
        import os
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read()
                            for old_import in old_imports:
                                if old_import in content:
                                    warnings.append(f"Found old import '{old_import}' in {file_path}")
                    except:
                        pass  # Skip files we can't read
    except:
        pass  # Skip if we can't scan directory
    
    if warnings:
        print("⚠️  Found potential old system usage:")
        for warning in warnings[:5]:  # Show first 5
            print(f"   {warning}")
        if len(warnings) > 5:
            print(f"   ... and {len(warnings) - 5} more")
        print("\n💡 Consider updating these to use natural conversation:")
        print("   OLD: from framework.agent_communication.core.enhanced_protocol import EnhancedAgentProtocol")
        print("   NEW: from agent_communication import Agent")
    else:
        print("✅ No old rigid system imports detected")

if __name__ == "__main__":
    print("🚀 Agent Communication v2.0 Migration Test")
    print("Testing your upgrade to natural conversation...")
    
    # Check for old system usage
    check_old_system()
    
    # Test new system
    success = test_migration()
    
    if success:
        print("\n🎯 MIGRATION SUCCESSFUL!")
        sys.exit(0)
    else:
        print("\n❌ Migration needs attention")
        print("📋 See MIGRATION_GUIDE_v2.md for detailed help")
        sys.exit(1)
#!/usr/bin/env python3
"""
Test Script for Agora and Moirai Integration

This script tests the core functionality of the Agora MCP integration
and Moirai Phase 1 capabilities.
"""

import asyncio
import json
import sys
import os

# Add framework to path
framework_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, framework_dir)

# Change to framework directory to fix relative imports
os.chdir(framework_dir)

try:
    from mcp_integration.agora_client import AgoraClient
    from mcp_integration.documentation_agora_client import DocumentationAgoraClient
    from moirai_core.overseer import MoiraiOverseer
    from agent_communication.agora_integration import AgoraIntegration
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Try running with: python3 -m framework.scripts.test_agora_moirai from project root")
    sys.exit(1)


async def test_agora_connection():
    """Test basic Agora connection."""
    print("🧪 Testing Agora Connection...")
    
    client = AgoraClient("TestAgent")
    connected = await client.connect()
    
    if connected:
        print("✅ Agora connection successful")
        return True
    else:
        print("❌ Agora connection failed")
        return False


async def test_agent_registration():
    """Test agent registration in Agora."""
    print("🧪 Testing Agent Registration...")
    
    client = AgoraClient("TestDocAgent")
    
    if not await client.connect():
        print("❌ Cannot test registration - connection failed")
        return False
    
    success = await client.register_agent(
        agent_type="documentation",
        capabilities=["testing", "documentation"],
        metadata={"test": True}
    )
    
    if success:
        print("✅ Agent registration successful")
        return True
    else:
        print("❌ Agent registration failed")
        return False


async def test_documentation_client():
    """Test documentation-specific Agora client."""
    print("🧪 Testing Documentation Agora Client...")
    
    doc_client = DocumentationAgoraClient("TestDocumentationAgent")
    
    if not await doc_client.connect():
        print("❌ Documentation client connection failed")
        return False
    
    # Test registration as documentation agent
    success = await doc_client.register_documentation_agent()
    
    if success:
        print("✅ Documentation agent registration successful")
        
        # Test capability announcement
        cap_success = await doc_client.announce_documentation_capability(
            "test_capability",
            "Test capability for integration testing",
            85
        )
        
        if cap_success:
            print("✅ Capability announcement successful")
            return True
        else:
            print("❌ Capability announcement failed")
            return False
    else:
        print("❌ Documentation agent registration failed")
        return False


async def test_moirai_initialization():
    """Test Moirai Overseer initialization."""
    print("🧪 Testing Moirai Overseer...")
    
    moirai = MoiraiOverseer()
    
    success = await moirai.initialize()
    
    if success:
        print("✅ Moirai initialization successful")
        return True
    else:
        print("❌ Moirai initialization failed")
        return False


async def test_moirai_project_handling():
    """Test Moirai project handling capabilities."""
    print("🧪 Testing Moirai Project Handling...")
    
    moirai = MoiraiOverseer()
    
    if not await moirai.initialize():
        print("❌ Cannot test project handling - Moirai initialization failed")
        return False
    
    # Test simple project request
    user_request = "I need a simple REST API for managing tasks with basic CRUD operations"
    
    result = await moirai.handle_user_request(user_request)
    
    if result.get('success'):
        print("✅ Project handling successful")
        print(f"   Project ID: {result.get('project_id')}")
        print(f"   Assigned agents: {result.get('assigned_agents')}")
        print(f"   Plan summary: {result.get('plan_summary', 'N/A')[:100]}...")
        return True
    else:
        print("❌ Project handling failed")
        print(f"   Error: {result.get('error', 'Unknown error')}")
        return False


async def test_agora_integration():
    """Test the Agora integration layer."""
    print("🧪 Testing Agora Integration Layer...")
    
    integration = AgoraIntegration()
    
    success = await integration.initialize()
    
    if success:
        print("✅ Agora integration initialization successful")
        
        # Test documentation request handling
        request_data = {
            "document_type": "api",
            "description": "API documentation for task management service",
            "requirements": {
                "include_examples": True,
                "format": "markdown"
            }
        }
        
        result = await integration.handle_documentation_request(request_data)
        
        if result.get('success'):
            print("✅ Documentation request handling successful")
            print(f"   Agora tracked: {result.get('agora_tracked')}")
            return True
        else:
            print("❌ Documentation request handling failed")
            return False
    else:
        print("❌ Agora integration initialization failed")
        return False


async def test_system_status():
    """Test system status retrieval."""
    print("🧪 Testing System Status...")
    
    client = AgoraClient("StatusTestAgent")
    
    if not await client.connect():
        print("❌ Cannot test status - connection failed")
        return False
    
    status = await client.get_system_status()
    
    if status:
        print("✅ System status retrieval successful")
        print(f"   Status keys: {list(status.keys())}")
        return True
    else:
        print("❌ System status retrieval failed")
        return False


async def main():
    """Run all tests."""
    print("🚀 Starting Agora + Moirai Integration Tests")
    print("=" * 50)
    
    tests = [
        ("Agora Connection", test_agora_connection),
        ("Agent Registration", test_agent_registration),
        ("Documentation Client", test_documentation_client),
        ("Moirai Initialization", test_moirai_initialization),
        ("Moirai Project Handling", test_moirai_project_handling),
        ("Agora Integration", test_agora_integration),
        ("System Status", test_system_status)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = await test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*50)
    print("🧪 TEST SUMMARY")
    print("="*50)
    
    passed = 0
    failed = 0
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<30} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal: {passed + failed} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! Agora + Moirai integration is ready!")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Check the output above for details.")
    
    return failed == 0


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
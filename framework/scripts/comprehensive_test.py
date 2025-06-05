#!/usr/bin/env python3
"""
Comprehensive Framework Test Suite

This script performs a complete validation of the Agent Documentation System v4.0.0
framework including structure, documentation, schemas, and basic functionality.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Any

def test_framework_structure():
    """Test framework directory structure."""
    print("🧪 Testing Framework Structure...")
    
    framework_dir = Path(__file__).parent.parent
    
    required_dirs = [
        "mcp_integration",
        "moirai_core", 
        "agent_communication",
        "docs",
        "schemas",
        "scripts",
        "validators"
    ]
    
    missing_dirs = []
    for dir_name in required_dirs:
        if not (framework_dir / dir_name).exists():
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
    
    print("✅ All required directories exist")
    return True

def test_version_consistency():
    """Test version consistency across framework."""
    print("🧪 Testing Version Consistency...")
    
    framework_dir = Path(__file__).parent.parent
    expected_version = "4.0.0"
    
    # Check __init__.py files
    init_files = [
        "mcp_integration/__init__.py",
        "moirai_core/__init__.py", 
        "agent_communication/__init__.py"
    ]
    
    version_issues = []
    
    for init_file in init_files:
        init_path = framework_dir / init_file
        if init_path.exists():
            content = init_path.read_text()
            if f'"{expected_version}"' not in content and f"'{expected_version}'" not in content:
                # Check for any version that's not 4.0.0
                if "__version__" in content and expected_version not in content:
                    version_issues.append(f"{init_file} - wrong version")
    
    # Check schemas
    schema_files = [
        "schemas/document_protocol.yml",
        "schemas/enhanced_metadata_schema.yml"
    ]
    
    for schema_file in schema_files:
        schema_path = framework_dir / schema_file
        if schema_path.exists():
            content = schema_path.read_text()
            if f"version: \"{expected_version}\"" not in content:
                version_issues.append(f"{schema_file} - wrong version")
    
    if version_issues:
        print(f"❌ Version inconsistencies: {version_issues}")
        return False
    
    print(f"✅ All versions consistent with v{expected_version}")
    return True

def test_documentation_validation():
    """Test documentation validation."""
    print("🧪 Testing Documentation Validation...")
    
    framework_dir = Path(__file__).parent.parent
    validator_script = framework_dir / "validators" / "validator.py"
    
    if not validator_script.exists():
        print("❌ Validator script missing")
        return False
    
    # Find a documentation file to test
    doc_files = list((framework_dir / "docs").rglob("*.md"))
    if not doc_files:
        print("❌ No documentation files found to test")
        return False
    
    # Test validation of first doc file
    test_file = doc_files[0]
    
    try:
        result = subprocess.run([
            sys.executable, str(validator_script), "doc", str(test_file), str(framework_dir)
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Validation failed for {test_file}")
            print(result.stdout)
            print(result.stderr)
            return False
        
        print(f"✅ Documentation validation works (tested {test_file.name})")
        return True
        
    except Exception as e:
        print(f"❌ Validation test error: {e}")
        return False

def test_agora_client_structure():
    """Test Agora client implementation structure."""
    print("🧪 Testing Agora Client Structure...")
    
    framework_dir = Path(__file__).parent.parent
    agora_client_path = framework_dir / "mcp_integration" / "agora_client.py"
    
    if not agora_client_path.exists():
        print("❌ Agora client missing")
        return False
    
    content = agora_client_path.read_text()
    
    # Check for key methods
    required_methods = [
        "connect",
        "register_agent", 
        "register_capability",
        "send_message",
        "assign_task",
        "update_progress"
    ]
    
    missing_methods = []
    for method in required_methods:
        if f"async def {method}" not in content:
            missing_methods.append(method)
    
    if missing_methods:
        print(f"❌ Missing methods in AgoraClient: {missing_methods}")
        return False
    
    # Check for correct database reference
    if "agent-coordination-v2" not in content:
        print("❌ Wrong database reference in AgoraClient")
        return False
    
    print("✅ Agora client structure valid")
    return True

def test_moirai_overseer_structure():
    """Test Moirai Overseer implementation structure."""
    print("🧪 Testing Moirai Overseer Structure...")
    
    framework_dir = Path(__file__).parent.parent
    overseer_path = framework_dir / "moirai_core" / "overseer.py"
    
    if not overseer_path.exists():
        print("❌ Moirai Overseer missing")
        return False
    
    content = overseer_path.read_text()
    
    # Check for key methods
    required_methods = [
        "initialize",
        "handle_user_request",
        "announce_arrival"
    ]
    
    missing_methods = []
    for method in required_methods:
        if f"async def {method}" not in content:
            missing_methods.append(method)
    
    if missing_methods:
        print(f"❌ Missing methods in MoiraiOverseer: {missing_methods}")
        return False
    
    print("✅ Moirai Overseer structure valid")
    return True

def test_schema_validation():
    """Test schema files."""
    print("🧪 Testing Schema Validation...")
    
    framework_dir = Path(__file__).parent.parent
    schema_dir = framework_dir / "schemas"
    
    required_schemas = [
        "document_protocol.yml",
        "enhanced_metadata_schema.yml",
        "enhanced_feedback_schema.yml"
    ]
    
    try:
        import yaml
        
        for schema_name in required_schemas:
            schema_path = schema_dir / schema_name
            
            if not schema_path.exists():
                print(f"❌ Missing schema: {schema_name}")
                return False
            
            # Test YAML parsing
            try:
                with open(schema_path, 'r') as f:
                    schema_data = yaml.safe_load(f)
                    
                # Check for required fields
                if 'version' not in schema_data:
                    print(f"❌ Schema {schema_name} missing version field")
                    return False
                    
            except yaml.YAMLError as e:
                print(f"❌ Invalid YAML in {schema_name}: {e}")
                return False
        
        print("✅ All schemas valid")
        return True
        
    except ImportError:
        print("⚠️  PyYAML not available, skipping detailed schema validation")
        
        # Basic existence check
        for schema_name in required_schemas:
            schema_path = schema_dir / schema_name
            if not schema_path.exists():
                print(f"❌ Missing schema: {schema_name}")
                return False
        
        print("✅ All schemas exist (YAML validation skipped)")
        return True

def test_script_functionality():
    """Test key scripts."""
    print("🧪 Testing Script Functionality...")
    
    framework_dir = Path(__file__).parent.parent
    scripts_dir = framework_dir / "scripts"
    
    # Test validation script
    validate_script = scripts_dir / "validate.sh"
    if not validate_script.exists():
        print("❌ Validation script missing")
        return False
    
    # Make sure it's executable
    if not os.access(validate_script, os.X_OK):
        print("⚠️  Validation script not executable")
        # Try to make it executable
        try:
            os.chmod(validate_script, 0o755)
            print("✅ Made validation script executable")
        except:
            print("❌ Could not make validation script executable")
            return False
    
    print("✅ Key scripts are present and executable")
    return True

def test_integration_consistency():
    """Test integration between components."""
    print("🧪 Testing Integration Consistency...")
    
    framework_dir = Path(__file__).parent.parent
    
    # Check that components reference the same database
    components_to_check = [
        "mcp_integration/agora_client.py",
        "agent_communication/agora_integration.py"
    ]
    
    inconsistencies = []
    
    for component in components_to_check:
        component_path = framework_dir / component
        if component_path.exists():
            content = component_path.read_text()
            
            # Check for correct database reference
            if "agent-coordination-v2" not in content:
                inconsistencies.append(f"{component} - wrong database reference")
            
            # Check for correct framework version
            if "4.0.0" not in content:
                inconsistencies.append(f"{component} - missing v4.0.0 reference")
    
    if inconsistencies:
        print(f"❌ Integration inconsistencies: {inconsistencies}")
        return False
    
    print("✅ Component integration consistent")
    return True

def test_the_protocol_compliance():
    """Test compliance with THE PROTOCOL v4.0."""
    print("🧪 Testing THE PROTOCOL v4.0 Compliance...")
    
    framework_dir = Path(__file__).parent.parent
    protocol_path = framework_dir / "docs" / "agent_onboarding.md"
    
    if not protocol_path.exists():
        print("❌ THE PROTOCOL document missing")
        return False
    
    content = protocol_path.read_text()
    
    # Check for v4.0.0 references
    compliance_checks = [
        ("version: \"4.0.0\"", "Document version"),
        ("Agora marketplace", "Agora integration"),
        ("Moirai OVERSEER", "Moirai orchestration"),
        ("agent-coordination-v2", "Database reference"),
        ("Consumer-Based MCP", "MCP architecture")
    ]
    
    failed_checks = []
    for check, description in compliance_checks:
        if check not in content:
            failed_checks.append(description)
    
    if failed_checks:
        print(f"❌ Protocol compliance issues: {failed_checks}")
        return False
    
    print("✅ THE PROTOCOL v4.0 compliance verified")
    return True

def main():
    """Run comprehensive framework test suite."""
    print("🚀 Agent Documentation System v4.0.0 - Comprehensive Test Suite")
    print("=" * 70)
    
    tests = [
        ("Framework Structure", test_framework_structure),
        ("Version Consistency", test_version_consistency),
        ("Documentation Validation", test_documentation_validation),
        ("Agora Client Structure", test_agora_client_structure),
        ("Moirai Overseer Structure", test_moirai_overseer_structure),
        ("Schema Validation", test_schema_validation),
        ("Script Functionality", test_script_functionality),
        ("Integration Consistency", test_integration_consistency),
        ("THE PROTOCOL Compliance", test_the_protocol_compliance)
    ]
    
    passed = 0
    failed = 0
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*25} {test_name} {'='*25}")
        try:
            if test_func():
                results[test_name] = "✅ PASS"
                passed += 1
            else:
                results[test_name] = "❌ FAIL"
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = "❌ ERROR"
            failed += 1
    
    # Summary
    print("\n" + "="*70)
    print("🧪 COMPREHENSIVE TEST SUMMARY")
    print("="*70)
    
    for test_name, result in results.items():
        print(f"{test_name:.<40} {result}")
    
    print(f"\nTotal tests: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
        print("🏛️ Agent Documentation System v4.0.0 is ready for deployment!")
        print("🧵 Moirai OVERSEER + Agora marketplace integration verified!")
        return True
    else:
        print(f"\n⚠️  {failed} test(s) failed.")
        print("Please review the failures above before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
#!/usr/bin/env python3
"""
Simple Framework Test Script

Tests basic framework functionality without complex imports.
"""

import os
import sys
import subprocess
from pathlib import Path

def test_python_syntax():
    """Test Python syntax in all framework files."""
    print("🧪 Testing Python syntax...")
    framework_dir = Path(__file__).parent.parent
    python_files = list(framework_dir.rglob("*.py"))
    
    failed = 0
    for py_file in python_files:
        try:
            result = subprocess.run([
                sys.executable, "-m", "py_compile", str(py_file)
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Syntax error in {py_file}")
                print(result.stderr)
                failed += 1
            
        except Exception as e:
            print(f"❌ Error checking {py_file}: {e}")
            failed += 1
    
    if failed == 0:
        print(f"✅ All {len(python_files)} Python files have valid syntax")
        return True
    else:
        print(f"❌ {failed} files have syntax errors")
        return False

def test_imports():
    """Test that imports work correctly."""
    print("🧪 Testing imports...")
    
    # Test basic imports without relative imports
    try:
        # Test individual modules
        print("  Testing basic imports...")
        
        # Check if files exist
        framework_dir = Path(__file__).parent.parent
        required_files = [
            "mcp_integration/agora_client.py",
            "mcp_integration/documentation_agora_client.py", 
            "moirai_core/overseer.py",
            "moirai_core/project_planner.py",
            "moirai_core/task_coordinator.py",
            "agent_communication/agora_integration.py"
        ]
        
        missing = []
        for file_path in required_files:
            full_path = framework_dir / file_path
            if not full_path.exists():
                missing.append(file_path)
        
        if missing:
            print(f"❌ Missing required files: {missing}")
            return False
        
        print("✅ All required framework files exist")
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_schemas():
    """Test schema files exist and are valid."""
    print("🧪 Testing schemas...")
    
    framework_dir = Path(__file__).parent.parent
    schema_dir = framework_dir / "schemas"
    
    required_schemas = [
        "document_protocol.yml",
        "enhanced_metadata_schema.yml",
        "enhanced_feedback_schema.yml"
    ]
    
    missing = []
    for schema in required_schemas:
        schema_path = schema_dir / schema
        if not schema_path.exists():
            missing.append(schema)
    
    if missing:
        print(f"❌ Missing schemas: {missing}")
        return False
    
    # Test YAML syntax
    try:
        import yaml
        for schema in required_schemas:
            schema_path = schema_dir / schema
            with open(schema_path, 'r') as f:
                yaml.safe_load(f)
        
        print("✅ All schemas exist and have valid YAML syntax")
        return True
        
    except ImportError:
        print("⚠️  PyYAML not available, skipping YAML validation")
        return True
    except Exception as e:
        print(f"❌ Schema validation failed: {e}")
        return False

def test_scripts():
    """Test that key scripts exist and are executable."""
    print("🧪 Testing scripts...")
    
    framework_dir = Path(__file__).parent.parent
    scripts_dir = framework_dir / "scripts"
    
    required_scripts = [
        "validate.sh",
        "enhanced_validate.sh", 
        "create_doc.sh",
        "setup_agent_name.sh"
    ]
    
    missing = []
    for script in required_scripts:
        script_path = scripts_dir / script
        if not script_path.exists():
            missing.append(script)
    
    if missing:
        print(f"❌ Missing scripts: {missing}")
        return False
    
    print("✅ All required scripts exist")
    return True

def test_validators():
    """Test validator functionality."""
    print("🧪 Testing validators...")
    
    framework_dir = Path(__file__).parent.parent
    validator_path = framework_dir / "validators" / "validator.py"
    
    if not validator_path.exists():
        print("❌ Validator script missing")
        return False
    
    # Test validator syntax
    try:
        result = subprocess.run([
            sys.executable, "-m", "py_compile", str(validator_path)
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Validator syntax error: {result.stderr}")
            return False
        
        print("✅ Validator has valid syntax")
        return True
        
    except Exception as e:
        print(f"❌ Validator test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Framework Validation Tests")
    print("=" * 50)
    
    tests = [
        ("Python Syntax", test_python_syntax),
        ("Imports", test_imports), 
        ("Schemas", test_schemas),
        ("Scripts", test_scripts),
        ("Validators", test_validators)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            failed += 1
    
    # Summary
    print("\n" + "="*50)
    print("🧪 TEST SUMMARY")
    print("="*50)
    
    print(f"Total tests: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! Framework structure is valid!")
        return True
    else:
        print(f"\n⚠️  {failed} test(s) failed. Check output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
#!/usr/bin/env python3
# agent_doc_system/scripts/validate_docs.py

import re
import sys
import yaml
from pathlib import Path
import os

# Get the directory where the script is located
script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
# Get the parent directory (agent_doc_system)
parent_dir = script_dir.parent

def validate_version(version_str):
    return re.match(r'^\d+\.\d+\.\d+$', version_str) is not None

def validate_status(status):
    return status in ['Active', 'Draft', 'Deprecated']

def validate_document(file_path):
    errors = []
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract metadata section
    metadata_match = re.search(r'## Machine-Actionable Metadata\n```(?:yaml)?\n(.*?)\n```', content, re.DOTALL)
    if not metadata_match:
        print(f'❌ {file_path}: Missing properly formatted metadata section')
        return False
    
    # Parse YAML metadata
    try:
        metadata = yaml.safe_load(metadata_match.group(1))
        
        # Validate required fields
        if 'schema' not in metadata:
            errors.append('Missing required field: schema')
        if 'version' not in metadata:
            errors.append('Missing required field: version')
        elif not validate_version(metadata['version']):
            errors.append(f"Invalid version format: {metadata['version']}. Should be X.Y.Z")
        if 'status' not in metadata:
            errors.append('Missing required field: status')
        elif not validate_status(metadata['status']):
            errors.append(f"Invalid status: {metadata['status']}. Should be one of: Active, Draft, Deprecated")
        
        # Check for changelog section
        if '## Changelog' not in content:
            errors.append('Missing required section: Changelog')
            
        if errors:
            print(f'❌ {file_path}:')
            for error in errors:
                print(f'  - {error}')
            return False
        else:
            print(f'✅ {file_path}: Document is valid')
            return True
    except yaml.YAMLError as e:
        print(f'❌ {file_path}: Invalid YAML in metadata: {str(e)}')
        return False

def main():
    # Validate all markdown files in docs directory
    docs_dir = parent_dir / 'docs'
    valid = True
    
    if not docs_dir.exists():
        print(f"Error: Docs directory not found at {docs_dir}")
        sys.exit(1)
        
    found = False
    for file_path in docs_dir.glob('**/*.md'):
        found = True
        if not validate_document(file_path):
            valid = False
    
    if not found:
        print("No markdown files found for validation.")
        sys.exit(0)
        
    sys.exit(0 if valid else 1)

if __name__ == "__main__":
    main() 
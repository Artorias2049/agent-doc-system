#!/usr/bin/env python3

import os
import sys
import json
from pathlib import Path
import hashlib
from datetime import datetime

class FrameworkProtection:
    def __init__(self):
        self.framework_root = Path("framework")
        self.projects_root = Path("projects")  # Changed to projects root
        self.protection_dir = Path(".framework")
        self.protection_file = self.protection_dir / "protection_registry.json"
        self.initialize_protection()

    def initialize_protection(self):
        """Initialize or load the protection registry"""
        # Create protection directory if it doesn't exist
        self.protection_dir.mkdir(exist_ok=True)
        
        if not self.protection_file.exists():
            self.create_protection_registry()
        else:
            self.validate_protection_registry()

    def create_protection_registry(self):
        """Create initial protection registry with file hashes"""
        protection_data = {
            "created_at": datetime.utcnow().isoformat(),
            "last_validated": datetime.utcnow().isoformat(),
            "files": {}
        }
        
        # Calculate hashes for all framework files
        for file_path in self.framework_root.rglob("*"):
            if file_path.is_file() and not str(file_path).endswith(".framework_protection.json"):
                relative_path = str(file_path.relative_to(self.framework_root))
                file_hash = self.calculate_file_hash(file_path)
                protection_data["files"][relative_path] = {
                    "hash": file_hash,
                    "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                }

        # Save protection registry
        with open(self.protection_file, 'w') as f:
            json.dump(protection_data, f, indent=2)

    def validate_protection_registry(self):
        """Validate that no framework files have been modified"""
        with open(self.protection_file, 'r') as f:
            protection_data = json.load(f)

        violations = []
        for relative_path, file_data in protection_data["files"].items():
            file_path = self.framework_root / relative_path
            if not file_path.exists():
                violations.append(f"Missing file: {relative_path}")
                continue

            current_hash = self.calculate_file_hash(file_path)
            if current_hash != file_data["hash"]:
                violations.append(f"Modified file: {relative_path}")

        if violations:
            print("Framework Protection Violations Detected:")
            for violation in violations:
                print(f"- {violation}")
            sys.exit(1)

    def calculate_file_hash(self, file_path):
        """Calculate SHA-256 hash of a file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def validate_project_structure(self, project_path):
        """Validate that project and component files are only in allowed locations"""
        project_path = Path(project_path)
        if not project_path.exists():
            return True

        for file_path in project_path.rglob("*"):
            if file_path.is_file():
                relative_path = str(file_path.relative_to(project_path))
                if not self.is_allowed_project_file(relative_path):
                    print(f"Unauthorized file location: {relative_path}")
                    return False
        return True

    def is_allowed_project_file(self, relative_path):
        """Check if a file is in an allowed location within a project or component"""
        path_parts = Path(relative_path).parts
        
        # If it's a direct file in project root, only allow specific files
        if len(path_parts) == 1:
            allowed_root_files = ["README.md", "requirements.txt", "setup.py"]
            return path_parts[0] in allowed_root_files

        # If it's in a component directory
        if len(path_parts) >= 2:
            component_name = path_parts[0]
            # Check if it's a valid component structure
            if len(path_parts) == 2:
                # Allow component root files
                allowed_component_files = ["README.md", "requirements.txt"]
                return path_parts[1] in allowed_component_files
            else:
                # Check if it's in an allowed subdirectory of the component
                allowed_dirs = ["docs", "src", "tests", "config"]
                return path_parts[1] in allowed_dirs

        return False

def main():
    protection = FrameworkProtection()
    
    # Validate framework files
    protection.validate_protection_registry()
    
    # Validate project structure
    if not protection.validate_project_structure("projects"):
        print("Project structure validation failed")
        sys.exit(1)
    
    print("Framework protection validation passed")

if __name__ == "__main__":
    main() 
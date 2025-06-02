#!/usr/bin/env python3
"""
Validator for agent documentation system v2.4.0
Validates documentation with enhanced metadata schema support.
"""

import json
import re
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import yaml

class Validator:
    """Validator class for documentation and message validation."""
    
    def __init__(self, root_dir):
        """Initialize validator with root directory."""
        self.root_dir = Path(root_dir)
        
        # Handle both framework directory and project root directory
        if self.root_dir.name == "framework":
            # Called with framework directory, schemas are in ./schemas/
            schema_dir = self.root_dir / "schemas"
        else:
            # Called with project root, schemas are in framework/schemas/
            schema_dir = self.root_dir / "framework" / "schemas"
            
        self.schemas = {
            "document": schema_dir / "document_protocol.yml",
            "enhanced_metadata": schema_dir / "enhanced_metadata_schema.yml"
        }
        self._load_schemas()

    def _load_schemas(self):
        """Load all schema files."""
        try:
            self.schema_data = {
                name: yaml.safe_load(path.read_text())
                for name, path in self.schemas.items()
                if path.exists()
            }
        except Exception as e:
            print(f"❌ Error loading schemas: {e}")
            sys.exit(1)

    def validate_doc(self, doc_path):
        """Validate a documentation file against document_protocol.yml schema."""
        try:
            content = Path(doc_path).read_text()
            metadata = self._extract_metadata(content)
            if not metadata:
                return False, "No valid metadata found"

            errors = []
            schema = self.schema_data['document']  # Access the root level schema

            # Validate metadata section
            if 'metadata' not in metadata:
                errors.append("Missing metadata section")
            else:
                metadata_errors = self._validate_section(
                    metadata['metadata'],
                    schema['document_schema']['properties']['metadata'],
                    schema['document_schema']['properties']['metadata']['required']
                )
                errors.extend(metadata_errors)

            # Validate content section
            if 'content' not in metadata:
                errors.append("Missing content section")
            else:
                content_errors = self._validate_section(
                    metadata['content'],
                    schema['document_schema']['properties']['content'],
                    schema['document_schema']['properties']['content']['required']
                )
                errors.extend(content_errors)

            # Validate feedback section
            if 'feedback' not in metadata:
                errors.append("Missing feedback section")
            else:
                feedback_errors = self._validate_section(
                    metadata['feedback'],
                    schema['document_schema']['properties']['feedback'],
                    schema['document_schema']['properties']['feedback']['required']
                )
                errors.extend(feedback_errors)

            return len(errors) == 0, "Document is valid" if not errors else f"Validation errors: {', '.join(errors)}"
        except Exception as e:
            return False, str(e)

    def _validate_section(
        self, data: Dict[str, Any], schema: Dict[str, Any], required_fields: List[str]
    ) -> List[str]:
        """Validate a section against its schema definition."""
        errors = []

        # Check required fields
        missing = set(required_fields) - set(data.keys())
        if missing:
            errors.append(f"Missing required fields: {missing}")

        # Validate each field against its schema
        for field, value in data.items():
            if field in schema.get("properties", {}):
                field_errors = self._validate_field(value, schema["properties"][field])
                errors.extend([f"{field}: {error}" for error in field_errors])

        return errors

    def _validate_field(self, value: Any, schema: Dict[str, Any]) -> List[str]:
        """Validate a field against its schema definition."""
        errors = []

        # Type validation
        if 'type' in schema:
            if not self._validate_type(value, schema['type']):
                errors.append(f"Invalid type, expected {schema['type']}")

        # Format validation
        if 'format' in schema:
            if not self._validate_format(value, schema['format']):
                errors.append(f"Invalid format, expected {schema['format']}")

        # Pattern validation
        if 'pattern' in schema:
            if not re.match(schema['pattern'], str(value)):
                errors.append(f"Value does not match pattern {schema['pattern']}")

        # Enum validation
        if 'enum' in schema:
            if value not in schema['enum']:
                errors.append(f"Value not in allowed values: {schema['enum']}")

        # Range validation
        if 'minimum' in schema and value < schema['minimum']:
            errors.append(f"Value below minimum {schema['minimum']}")
        if 'maximum' in schema and value > schema['maximum']:
            errors.append(f"Value above maximum {schema['maximum']}")

        # Array validation
        if schema.get('type') == 'array' and 'items' in schema:
            if not isinstance(value, list):
                errors.append("Expected array")
            else:
                for item in value:
                    item_errors = self._validate_field(item, schema['items'])
                    errors.extend(item_errors)

        # Object validation
        if schema.get('type') == 'object' and 'properties' in schema:
            if not isinstance(value, dict):
                errors.append("Expected object")
            else:
                for prop_name, prop_value in value.items():
                    if prop_name in schema['properties']:
                        prop_errors = self._validate_field(prop_value, schema['properties'][prop_name])
                        errors.extend([f"{prop_name}: {error}" for error in prop_errors])

        return errors

    def validate_enhanced_metadata(self, metadata_path):
        """Validate enhanced metadata against enhanced_metadata_schema.yml."""
        try:
            if not Path(metadata_path).exists():
                return False, "File not found"
                
            content = Path(metadata_path).read_text()
            metadata = yaml.safe_load(content)
            
            if 'enhanced_metadata' not in self.schema_data:
                return False, "Enhanced metadata schema not loaded"
                
            schema = self.schema_data['enhanced_metadata']['enhanced_metadata_schema']
            errors = self._validate_section(metadata, schema, schema['required'])
            
            return len(errors) == 0, "Enhanced metadata is valid" if not errors else f"Validation errors: {', '.join(errors)}"
        except Exception as e:
            return False, str(e)

    def _validate_type(self, value: Any, expected_type: str) -> bool:
        """Validate value against expected type."""
        type_map = {
            'string': str,
            'number': (int, float),
            'boolean': bool,
            'array': list,
            'object': dict
        }
        if expected_type not in type_map:
            return True
        return isinstance(value, type_map[expected_type])

    def _validate_format(self, value: str, format_type: str) -> bool:
        """Validate value against expected format."""
        if format_type == 'uri':
            return value.startswith('https://') or value.startswith('http://')
        elif format_type == 'date-time':
            try:
                datetime.fromisoformat(value.replace('Z', '+00:00'))
                return True
            except ValueError:
                return False
        elif format_type == 'date':
            try:
                datetime.strptime(value, '%Y-%m-%d')
                return True
            except ValueError:
                return False
        elif format_type == 'uuid':
            try:
                uuid.UUID(value)
                return True
            except ValueError:
                return False
        return True

    def _extract_metadata(self, content):
        """Extract YAML metadata from markdown content."""
        if match := re.search(r'```yaml\n(.*?)\n```', content, re.DOTALL):
            try:
                return yaml.safe_load(match.group(1))
            except yaml.YAMLError:
                return None
        return None

def main():
    if len(sys.argv) < 3:
        print("Usage: validator.py <type> <path> [root_dir]")
        print("Types: doc, enhanced_metadata")
        sys.exit(1)

    validator = Validator(sys.argv[3] if len(sys.argv) > 3 else ".")
    valid_type = sys.argv[1]
    path = sys.argv[2]

    if valid_type == 'doc':
        success, msg = validator.validate_doc(path)
    elif valid_type == 'enhanced_metadata':
        success, msg = validator.validate_enhanced_metadata(path)
    else:
        print(f"Unknown validation type: {valid_type}")
        print("Available types: doc, enhanced_metadata")
        sys.exit(1)

    if not success:
        print(f"❌ {path}: {msg}")
        sys.exit(1)
    print(f"✅ {path}: {msg}")

if __name__ == '__main__':
    main()
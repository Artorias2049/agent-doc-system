#!/usr/bin/env python3

import json
import os
import sys
import yaml
from datetime import datetime
from typing import Dict, List, Any
import logging
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageValidator:
    def __init__(self, message_file: str, schema_file: str = None):
        self.message_file = message_file
        self.schema_file = schema_file or os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "schemas",
            "agent_communication.yml"
        )
        self.schema = self._load_schema()

    def _load_schema(self) -> Dict:
        """Load the schema file."""
        try:
            with open(self.schema_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading schema file: {e}")
            sys.exit(1)

    def validate_timestamp(self, timestamp: str) -> bool:
        """Validate ISO-8601 timestamp format."""
        try:
            datetime.fromisoformat(timestamp)
            return True
        except ValueError:
            return False

    def validate_uuid(self, uuid_str: str) -> bool:
        """Validate UUID format."""
        try:
            uuid.UUID(uuid_str)
            return True
        except ValueError:
            return False

    def validate_message_content(self, message_type: str, content: Dict) -> List[str]:
        """Validate message content against type-specific schema."""
        errors = []
        type_schema = self.schema.get("message_types", {}).get(message_type, {})
        
        if not type_schema:
            errors.append(f"No schema defined for message type: {message_type}")
            return errors

        required_fields = type_schema.get("required_fields", {})
        for field, field_schema in required_fields.items():
            if field not in content:
                errors.append(f"Missing required field in content: {field}")
            else:
                # Validate field type
                if field_schema.get("type") == "string":
                    if not isinstance(content[field], str):
                        errors.append(f"Field {field} must be a string")
                elif field_schema.get("type") == "number":
                    if not isinstance(content[field], (int, float)):
                        errors.append(f"Field {field} must be a number")
                elif field_schema.get("type") == "boolean":
                    if not isinstance(content[field], bool):
                        errors.append(f"Field {field} must be a boolean")
                elif field_schema.get("type") == "array":
                    if not isinstance(content[field], list):
                        errors.append(f"Field {field} must be an array")
                elif field_schema.get("type") == "object":
                    if not isinstance(content[field], dict):
                        errors.append(f"Field {field} must be an object")

                # Validate enum values
                if "enum" in field_schema:
                    if content[field] not in field_schema["enum"]:
                        errors.append(f"Field {field} must be one of: {field_schema['enum']}")

                # Validate number ranges
                if field_schema.get("type") == "number":
                    if "minimum" in field_schema and content[field] < field_schema["minimum"]:
                        errors.append(f"Field {field} must be >= {field_schema['minimum']}")
                    if "maximum" in field_schema and content[field] > field_schema["maximum"]:
                        errors.append(f"Field {field} must be <= {field_schema['maximum']}")

        return errors

    def validate_message(self, message: Dict) -> List[str]:
        """Validate a single message."""
        errors = []

        # Validate required fields from schema
        required_fields = self.schema["message_schema"]["required_fields"]
        for field, field_schema in required_fields.items():
            if field not in message:
                errors.append(f"Missing required field: {field}")
            else:
                # Validate field type
                if field_schema["type"] == "string":
                    if not isinstance(message[field], str):
                        errors.append(f"Field {field} must be a string")
                elif field_schema["type"] == "object":
                    if not isinstance(message[field], dict):
                        errors.append(f"Field {field} must be an object")

                # Validate specific formats
                if field == "id" and not self.validate_uuid(message[field]):
                    errors.append("Invalid UUID format for id field")
                if field == "timestamp" and not self.validate_timestamp(message[field]):
                    errors.append("Invalid timestamp format")
                if field == "type" and message[field] not in field_schema["enum"]:
                    errors.append(f"Invalid message type: {message['type']}")
                if field == "status" and message[field] not in field_schema["enum"]:
                    errors.append(f"Invalid status: {message['status']}")

        # Validate message content
        if "type" in message and "content" in message:
            content_errors = self.validate_message_content(message["type"], message["content"])
            errors.extend(content_errors)

        return errors

    def validate_file(self) -> List[str]:
        """Validate the entire message file."""
        errors = []

        try:
            with open(self.message_file, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            return [f"Message file not found: {self.message_file}"]
        except json.JSONDecodeError:
            return [f"Invalid JSON in message file: {self.message_file}"]

        # Validate top-level structure
        file_schema = self.schema["file_schema"]["required_fields"]
        for field, field_schema in file_schema.items():
            if field not in data:
                errors.append(f"Missing required field: {field}")
            else:
                if field == "messages" and not isinstance(data[field], list):
                    errors.append("'messages' must be an array")
                if field == "last_updated" and not self.validate_timestamp(data[field]):
                    errors.append("Invalid 'last_updated' timestamp format")
                if field == "version" and not isinstance(data[field], str):
                    errors.append("'version' must be a string")

        # Validate each message
        if "messages" in data and isinstance(data["messages"], list):
            for i, message in enumerate(data["messages"]):
                message_errors = self.validate_message(message)
                if message_errors:
                    errors.extend([f"Message {i}: {error}" for error in message_errors])

        return errors

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_agent_messages.py <message_file> [schema_file]")
        sys.exit(1)

    message_file = sys.argv[1]
    schema_file = sys.argv[2] if len(sys.argv) > 2 else None

    validator = MessageValidator(message_file, schema_file)
    errors = validator.validate_file()

    if errors:
        print("Validation errors found:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    else:
        print("Message file is valid")
        sys.exit(0)

if __name__ == "__main__":
    main() 
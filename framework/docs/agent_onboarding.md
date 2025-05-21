# Agent Onboarding Guide

## Machine-Actionable Metadata
```yaml
schema: "https://schema.org/TechnicalDocument"
version: "1.1.0"
status: "Active"
```

## Overview

This document serves as the single source of truth for understanding the agent-doc-system. It provides a comprehensive overview of the system's architecture, protocols, validation requirements, and best practices.

## Key Components

### 1. Documentation Protocol
- **Purpose:** Defines how all documentation should be structured and validated.
- **Key Files:**
  - [Documentation Protocol](documentation_protocol.md)
  - [Document Protocol Schema](../schemas/document_protocol.yml)

### 2. Agent Communication
- **Purpose:** Standardizes message formats and agent interactions.
- **Key Files:**
  - [Agent Communication Component](components/agent_communication/overview.md)
  - [Agent Communication Schema](../schemas/agent_communication.yml)
- **Core Operations:**
  - Send messages: `python framework/scripts/agent_communication.py --action send --type <type> --sender <sender> --content <json_content>`
  - Read messages: `python framework/scripts/agent_communication.py --action read [--read-file <path>]`
  - Cleanup messages: `python framework/scripts/agent_communication.py --action cleanup [--days <days>]`
- **Message Storage:**
  - Messages are stored in `framework/agent_communication/history/agent_messages.json`
  - Location is consistent across all agents (relative to project root)
  - Directory structure is created automatically if it doesn't exist
  - Each message includes:
    - ID (UUID)
    - Timestamp (ISO format)
    - Sender
    - Type
    - Content (JSON)
    - Status (pending/processed)
  - Messages are automatically cleaned up after specified days (default: 7)
- **File Structure:**
  ```
  project_root/
  ├── framework/
  │   ├── agent_communication/
  │   │   └── history/
  │   │       └── agent_messages.json
  │   └── scripts/
  │       └── agent_communication.py
  └── projects/
      └── {project_name}/
          └── {component_name}/
  ```
- **Message Types:**
  - `test_request`: Request for test execution
  - `test_result`: Results of test execution
  - `status_update`: Progress or status updates
  - `context_update`: Updates to agent context

### 3. Validation System
- **Purpose:** Automated scripts to check documentation, schemas, and agent messages for compliance.
- **Key Files:**
  - [Documentation Validation](../scripts/doc_validation.sh)
  - [Agent Message Validation](../scripts/validate_agent_messages.py)

### 4. Schemas
- **Purpose:** YAML files that define the structure for documentation and agent messages.
- **Key Files:**
  - [Document Protocol Schema](../schemas/document_protocol.yml)
  - [Agent Communication Schema](../schemas/agent_communication.yml)

### 5. Documentation Templates
- **Purpose:** Standardized templates for creating new documentation.
- **Location:** `framework/docs/templates/`
- **Available Templates:**
  - Project Templates (`framework/docs/templates/projects/`):
    - `overview.md`: Project overview documentation
    - `setup.md`: Project setup guide
  - Component Templates (`framework/docs/templates/components/`):
    - `overview.md`: Component overview documentation
    - `api.md`: API documentation

### 6. Core Components
- **Purpose:** Reusable system components with standardized documentation.
- **Location:** `framework/docs/components/`
- **Available Components:**
  - [Agent Communication](components/agent_communication/overview.md)
  - [Feedback System](components/feedback/overview.md)
  - [Git Workflow](components/git/overview.md)

## Required Practices

### Documentation Structure
1. **Location Requirements:**
   - Core documentation: `framework/docs/`
   - Project documentation: `projects/{project_name}/docs/`
   - Component documentation: `projects/{project_name}/{component_name}/docs/`
   - Templates: `framework/docs/templates/`

2. **Required Sections:**
   - Title
   - Machine-Actionable Metadata
   - Overview
   - Main Content
   - Changelog

### Metadata
Every documentation file must include a `## Machine-Actionable Metadata` section with a YAML code block containing at least:
- `schema`
- `version`
- `status`
- `id`
- `last_updated`
- `author`

### Creating New Documentation
1. Choose the appropriate template from `framework/docs/templates/`
2. Copy the template to the correct location
3. Update the metadata and content
4. Run validation before committing

### Validation
Run `./framework/scripts/doc_validation.sh` before merging or releasing to ensure compliance.

## Communication Protocol

All agent messages must follow the JSON schema defined in `framework/schemas/agent_communication.yml`. Use the provided Python script (`agent_communication.py`) for sending, receiving, and tracking messages.

Example usage:
```bash
# Send a message (always goes to framework/agent_communication/history/agent_messages.json)
python framework/scripts/agent_communication.py --action send --type "request" --sender "agent1" --content '{"action": "process", "data": {"id": 123}}'

# Read messages from default location
python framework/scripts/agent_communication.py --action read

# Read messages from a specific file (useful for reading archived messages)
python framework/scripts/agent_communication.py --action read --read-file "/path/to/other/messages.json"

# Cleanup old messages (default: 7 days)
python framework/scripts/agent_communication.py --action cleanup --days 14
```

Message Format:
```json
{
  "id": "uuid-string",
  "timestamp": "2024-03-21T12:00:00Z",
  "sender": "agent-name",
  "type": "request|response|notification|error|status_update",
  "content": {
    // Message-specific content
  },
  "status": "pending|processed"
}
```

## Best Practices

1. **Documentation:**
   - Use templates for new documentation
   - Keep documentation up to date
   - Follow the required structure
   - Include examples and diagrams

2. **Code:**
   - Update documentation with code changes
   - Use consistent formatting
   - Include examples
   - Add changelog entries

3. **Review:**
   - Regular documentation reviews
   - Validate before committing
   - Use the feedback framework

## Validation & Troubleshooting

Use the validation script to check for:
- Proper metadata and changelog sections
- Valid agent message files
- Valid YAML schemas
- Markdown formatting issues
- Template compliance

If validation fails, check the error messages for:
- Missing or misformatted sections
- Invalid metadata
- Template non-compliance
- Schema violations

## Where to Find Things

- **Framework Documentation:** `framework/docs/`
- **Project Docs:** `projects/{project_name}/docs/`
- **Component Docs:** `projects/{project_name}/{component_name}/docs/`
- **Templates:** `framework/docs/templates/`
- **Schemas:** `framework/schemas/`
- **Validation Scripts:** `framework/scripts/`
- **Agent Communication Code:** `framework/agent_communication/`

## Getting Started

1. Read the main documentation files in `framework/docs/`
2. Review the templates in `framework/docs/templates/`
3. Review the schemas in `framework/schemas/`
4. Use the provided Python classes and scripts
5. Run the validation script before submitting changes

## Quickstart Checklist

- [ ] Read the onboarding doc
- [ ] Review the templates
- [ ] Review the schemas
- [ ] Run the validation script
- [ ] Follow the commit/PR guidelines

## Changelog

- **1.1.0** (2024-03-21): Added template system and updated documentation structure
- **1.0.0** (2024-03-21): Initial release of the Agent Onboarding Guide 
# Agent Onboarding Guide [THE PROTOCOL]

## Machine-Actionable Metadata
```yaml
metadata:
  schema: "https://schema.org/TechnicalDocument"
  version: "1.0.0"
  status: "Active"
  owner: "Documentation Team"
  title: "Agent Onboarding Guide [THE PROTOCOL]"
  description: "THE PROTOCOL: Comprehensive guide for understanding the agent-doc-system and agent communication protocols"
content:
  overview: "This document serves as THE PROTOCOL - the single source of truth for understanding the agent-doc-system and agent communication protocols."
  key_components: "Documentation Protocol, Agent Communication, Validation System, Schemas, Documentation Templates, Core Components"
  sections:
    - title: "Overview"
      content: "This document serves as THE PROTOCOL - the single source of truth for understanding the agent-doc-system and agent communication protocols."
    - title: "Key Components"
      content: "Documentation Protocol, Agent Communication, Validation System, Schemas, Documentation Templates, Core Components"
    - title: "Required Practices"
      content: "Documentation Structure, Metadata, Creating New Documentation, Validation"
    - title: "Communication Protocol"
      content: "All agent messages must follow the JSON schema defined in framework/schemas/agent_communication.yml."
    - title: "Best Practices"
      content: "Documentation, Code, Review"
    - title: "Validation & Troubleshooting"
      content: "Use the validation script to check for proper metadata, valid agent message files, valid YAML schemas, markdown formatting issues, and template compliance."
    - title: "Where to Find Things"
      content: "Framework Documentation, Project Docs, Component Docs, Templates, Schemas, Validation Scripts, Agent Communication Code"
    - title: "Getting Started"
      content: "Read the main documentation files, review the templates, review the schemas, use the provided Python classes and scripts, run the validation script before submitting changes."
    - title: "Quickstart Checklist"
      content: "Read the onboarding doc, review the templates, review the schemas, run the validation script, follow the commit/PR guidelines."
    - title: "Changelog"
      content: "1.0.0 (2024-03-21): Initial release of THE PROTOCOL"
  changelog:
    - version: "1.1.0"
      date: "2024-12-29"
      changes:
        - "Added Claude Code optimization framework"
        - "Implemented Pydantic models for 50% faster validation"
        - "Added new message types: workflow_request, validation_request, documentation_update"
        - "Enhanced agent communication protocol with type safety"
        - "Added comprehensive pytest testing framework"
        - "Implemented CI/CD pipeline with automated validation"
        - "Added custom slash commands for streamlined operations"
        - "Enhanced security with OWASP compliance checking"
    - version: "1.0.0"
      date: "2024-03-21"
      changes:
        - "Initial release of THE PROTOCOL"
feedback:
  rating: 5
  comments: "Very helpful and well-structured guide."
  observations:
    - what: "Clear and comprehensive documentation."
      impact: "Improved readability and usability."
  suggestions:
    - action: "Consider adding more examples."
      priority: "Medium"
  status:
    value: "Approved"
    updated_by: "Reviewer"
    date: "2024-03-21"
    validation: "Passed"
    implementation: "Complete"
```

## Overview

This document serves as THE PROTOCOL - the single source of truth for understanding the agent-doc-system and agent communication protocols. It provides a comprehensive overview of the system's architecture, protocols, validation requirements, and best practices.

## Key Components

### 1. Documentation Protocol
- **Purpose:** Defines how all documentation should be structured and validated.
- **Key Files:**
  - [Documentation Protocol](documentation_protocol.md)
  - [Document Protocol Schema](../schemas/document_protocol.yml)

### 2. Agent Communication [PROTOCOL]
- **Purpose:** Standardizes message formats and agent interactions.
- **Key Files:**
  - [Agent Communication Component](../components/agent_communication/overview.md)
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
    - Status (pending/processed/failed)
  - Messages are automatically cleaned up after specified days (default: 7)
- **File Structure:**
  ```
  project_root/
  └── agent-doc-system/
      ├── framework/
      │   ├── agent_communication/
      │   │   ├── core/
      │   │   ├── config/
      │   │   ├── history/
      │   │   └── README.md
      │   ├── components/
      │   │   ├── feedback/
      │   │   ├── agent_communication/
      │   │   └── git/
      │   ├── docs/
      │   │   ├── documentation_protocol.md
      │   │   ├── agent_onboarding.md
      │   │   └── templates/
      │   ├── scripts/
      │   ├── schemas/
      │   └── validators/
      └── project_docs/
  ```
- **Message Types:**
  - `test_request`:
    - Required fields:
      - test_type: unit/integration/e2e/performance
      - test_file: Path to test file
      - parameters: Test parameters including environment and verbose flag
  - `test_result`:
    - Required fields:
      - test_id: UUID of the test request
      - status: passed/failed/error
      - logs: Array of test execution logs
      - artifacts: Test artifacts with path and type
  - `status_update`:
    - Required fields:
      - agent_id: Agent identifier
      - state: idle/busy/error/offline
      - progress: Progress percentage (0-100)
  - `context_update`:
    - Required fields:
      - context_id: UUID of the context
      - type: add/update/remove
      - data: Context-specific data
  - `workflow_request` (NEW in v1.1.0):
    - Required fields:
      - workflow_name: Name of workflow to execute
      - steps: Array of workflow steps with dependencies
      - parameters: Workflow-specific parameters
    - Optional fields:
      - parallel_execution: Enable parallel step execution
      - failure_strategy: abort/continue/retry
  - `validation_request` (NEW in v1.1.0):
    - Required fields:
      - validation_type: schema/documentation/messages/project
      - target_files: Array of files to validate
    - Optional fields:
      - validation_level: basic/enhanced/strict
      - auto_fix: Automatically fix issues
      - generate_report: Generate validation report
  - `documentation_update` (NEW in v1.1.0):
    - Required fields:
      - update_type: create/update/delete/sync
      - target_documents: Array of documents to update
    - Optional fields:
      - template_name: Template for creation/update
      - metadata_updates: Metadata changes to apply
      - auto_generate: Auto-generate content
- **Message Validation:**
  - All messages must validate against agent_communication.yml schema
  - Message types must include all required fields
  - Field formats must match schema specifications:
    - UUIDs must follow pattern: ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$
    - Timestamps must be ISO-8601 format
    - Sender IDs must match pattern: ^[a-zA-Z0-9_-]+$
    - File paths must match pattern: ^[a-zA-Z0-9/._-]+$

### 3. Claude Code Enhancement System (NEW in v1.1.0)
- **Purpose:** Optimized development workflow with Pydantic models and enhanced validation.
- **Key Features:**
  - **50% faster validation** through Pydantic v2 models
  - **Type safety** with comprehensive MyPy integration
  - **Enhanced CLI** with Rich console formatting
  - **Custom slash commands** for streamlined operations
- **Key Files:**
  - [Enhanced Protocol](../agent_communication/core/enhanced_protocol.py)
  - [Pydantic Models](../agent_communication/core/models.py)
  - [CLAUDE.md Configuration](../../CLAUDE.md)
- **Usage Examples:**
  ```bash
  # Send workflow request with validation
  /agent:send workflow_request agent1 {
    "workflow_name": "validate_and_test",
    "steps": [{"name": "validate", "action": "check"}],
    "parameters": {"target": "framework"}
  }
  
  # Execute comprehensive validation
  /agent:validate project --level strict --generate_report
  
  # Run security audit
  /agent:audit agent_communication --owasp-check
  ```

### 4. Validation System
- **Purpose:** Automated scripts to check documentation, schemas, and agent messages for compliance.
- **Key Files:**
  - [Documentation Validation](../scripts/doc_validation.sh)
  - [Agent Message Validation](../scripts/validate_agent_messages.py)
  - [Enhanced Validator](../validators/validator.py) (Updated for Pydantic)

### 5. Schemas
- **Purpose:** YAML files that define the structure for documentation and agent messages.
- **Key Files:**
  - [Document Protocol Schema](../schemas/document_protocol.yml)
  - [Agent Communication Schema](../schemas/agent_communication.yml)

### 6. Documentation Templates
- **Purpose:** Standardized templates for creating new documentation.
- **Location:** `framework/docs/templates/`
- **Available Templates:**
  - Project Templates (`framework/docs/templates/projects/`):
    - `overview.md`: Project overview documentation
    - `setup.md`: Project setup guide
  - Component Templates (`framework/docs/templates/components/`):
    - `overview.md`: Component overview documentation
    - `api.md`: API documentation

### 7. Core Components
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
Every documentation file must include a `## Machine-Actionable Metadata` section with a YAML code block containing:
- `schema`
- `version`
- `status`
- `owner`

### Creating New Documentation
1. Choose the appropriate template from `framework/docs/templates/`
2. Copy the template to the correct location
3. Update the metadata and content
4. Run validation before committing

### Validation
Run `./framework/scripts/doc_validation.sh` before merging or releasing to ensure compliance.

## Communication Protocol [PROTOCOL]

All agent messages must follow the JSON schema defined in `framework/schemas/agent_communication.yml`. Use the provided Python script (`agent_communication.py`) for sending, receiving, and tracking messages.

Example usage:
```bash
# Send a test request message
python framework/scripts/agent_communication.py --action send --type "test_request" --sender "agent1" --content '{
  "test_type": "unit",
  "test_file": "tests/unit/test_example.py",
  "parameters": {
    "environment": "development",
    "verbose": true
  }
}'

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
  "type": "test_request|test_result|status_update|context_update",
  "content": {
    // Message-specific content based on type
  },
  "status": "pending|processed|failed"
}
```

Message File Format:
```json
{
  "messages": [
    // Array of messages following the message format above
  ],
  "last_updated": "2024-03-21T12:00:00Z",
  "version": "1.0.0"
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

- **Framework Documentation:** `agent-doc-system/framework/docs/`
- **Project Docs:** `agent-doc-system/projects/{project_name}/`
- **Component Docs:** `agent-doc-system/framework/components/{component_name}/`
- **Templates:** `agent-doc-system/framework/docs/templates/`
- **Schemas:** `agent-doc-system/framework/schemas/`
- **Validation Scripts:** `agent-doc-system/framework/scripts/`
- **Agent Communication Code:** `agent-doc-system/framework/agent_communication/`

## Getting Started

1. Read the main documentation files in `agent-doc-system/framework/docs/`
2. Review the templates in `agent-doc-system/framework/docs/templates/`
3. Review the schemas in `agent-doc-system/framework/schemas/`
4. Use the provided Python classes and scripts
5. Run the validation script before submitting changes

## Quickstart Checklist

- [ ] Read the onboarding doc
- [ ] Review the templates
- [ ] Review the schemas
- [ ] Run the validation script
- [ ] Follow the commit/PR guidelines

## Changelog

- **1.0.0** (2024-03-21): Initial release of THE PROTOCOL 
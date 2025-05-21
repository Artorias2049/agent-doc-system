# Documentation Protocol

## Machine-Actionable Metadata
```yaml
schema: "https://schema.org/TechnicalDocument"
id: "doc-protocol"
version: "1.2.0"
last_updated: "2024-03-21"
status: "Active"
author: "Documentation Team"
```

## Overview

This document outlines the documentation protocol for the agent-doc-system project. It provides guidelines for creating, maintaining, and validating documentation.

## Documentation Structure

### Required Sections

1. Title
2. Machine-Actionable Metadata
3. Overview
4. Main Content
5. Changelog

### Documentation Location

All documentation must be stored in the following locations:

1. **Framework Documentation**: `framework/docs/`
   - System-wide documentation
   - Protocols and standards
   - General guidelines
   - Agent communication protocols
   - Validation rules

2. **Project Documentation**: `projects/<project_name>/docs/`
   - Project-specific guides
   - Implementation details
   - Project workflows
   - Project-specific protocols

3. **Component Documentation**: `projects/<project_name>/<component_name>/docs/`
   - Component-specific documentation
   - API references
   - Technical specifications
   - Integration guides

4. **Documentation Templates**: `framework/docs/templates/`
   - Project templates: `framework/docs/templates/projects/`
     - `overview.md`: Project overview template
     - `setup.md`: Project setup guide template
   - Component templates: `framework/docs/templates/components/`
     - `overview.md`: Component overview template
     - `api.md`: API documentation template

Each project and component must maintain its own documentation directory with the following structure:
```
agent-doc-system/
├── framework/
│   ├── docs/
│   │   ├── components/
│   │   │   └── <component_name>/
│   │   │       ├── overview.md
│   │   │       └── api.md
│   │   ├── templates/
│   │   │   ├── projects/
│   │   │   │   ├── overview.md
│   │   │   │   └── setup.md
│   │   │   └── components/
│   │   │       ├── overview.md
│   │   │       └── api.md
│   │   └── schemas/
│   │       ├── document_protocol.yml
│   │       └── agent_communication.yml
│   └── scripts/
│       ├── doc_validation.sh
│       └── validate_docs.py
└── projects/
    └── <project_name>/
        ├── docs/
        │   ├── overview.md
        │   └── setup.md
        └── <component_name>/
            └── docs/
                ├── overview.md
                └── api.md
```

### Metadata Format

Every documentation file must include a `## Machine-Actionable Metadata` section with a YAML code block containing:

```yaml
schema: "https://schema.org/TechnicalDocument"
id: "unique-id"                    # Required: Unique identifier for the document
version: "x.y.z"                   # Required: Semantic versioning
last_updated: "ISO8601_timestamp"  # Required: Last update timestamp
status: "Active"                   # Required: Active|Deprecated|Archived
author: "Author Name"              # Required: Document author
priority: "P0"                     # Optional: Priority level (P0-P3)
owner: "Team Name"                 # Optional: Owning team
```

## Documentation Types

1. **System Documentation**
   - Agent communication protocols
   - Framework architecture
   - Core components
   - Validation rules

2. **Project Documentation**
   - Project overview
   - Setup guides
   - Implementation details
   - Workflows

3. **Component Documentation**
   - Component overview
   - API references
   - Integration guides
   - Examples

## Writing Guidelines

1. **Structure**
   - Follow the required sections
   - Use consistent formatting
   - Include code examples
   - Add diagrams when helpful

2. **Content**
   - Use clear, concise language
   - Keep documentation up to date
   - Include practical examples
   - Document all public APIs

3. **Metadata**
   - Always include required fields
   - Use semantic versioning
   - Update timestamps
   - Maintain changelog

## Validation Process

1. **Pre-commit Checks**
   ```bash
   ./framework/scripts/doc_validation.sh
   ```
   - Validates metadata format
   - Checks required sections
   - Verifies schema compliance
   - Tests code examples

2. **Schema Validation**
   ```bash
   python framework/scripts/validate_docs.py
   ```
   - Validates against YAML schemas
   - Checks document structure
   - Verifies cross-references

3. **Manual Review**
   - Technical accuracy
   - Completeness
   - Clarity
   - Examples

## Best Practices

1. **Documentation Updates**
   - Update with code changes
   - Keep examples current
   - Maintain changelog
   - Regular reviews

2. **Code Examples**
   - Include language identifiers
   - Test all examples
   - Keep them simple
   - Add comments

3. **Cross-referencing**
   - Link related documents
   - Reference schemas
   - Include examples
   - Maintain consistency

## Tools and Resources

1. **Validation Tools**
   - `doc_validation.sh`: Main validation script
   - `validate_docs.py`: Schema validation
   - `validate_agent_messages.py`: Message validation

2. **Templates**
   - Project templates
   - Component templates
   - API documentation templates

3. **Schemas**
   - `document_protocol.yml`
   - `agent_communication.yml`
   - `feedback_framework.yml`

## Troubleshooting

Common issues and solutions:

1. **Validation Errors**
   - Check metadata format
   - Verify required sections
   - Update changelog
   - Run validation scripts

2. **Schema Violations**
   - Review schema definitions
   - Check field types
   - Verify enums
   - Update schemas

3. **Formatting Issues**
   - Use consistent style
   - Follow templates
   - Validate markdown
   - Check links

## Future Improvements

Planned enhancements:
- Automated documentation generation
- Enhanced validation pipeline
- Documentation search
- Version control integration
- API documentation generator

## Changelog

- **1.2.0** (2024-03-21): Updated directory structure and validation process
- **1.1.0** (2024-03-21): Added schema validation and templates
- **1.0.0** (2024-03-21): Initial release of the Documentation Protocol 
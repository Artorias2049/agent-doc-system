# Documentation Protocol

## Machine-Actionable Metadata
```yaml
metadata:
  schema: "https://schema.org/TechnicalDocument"
  version: "1.1.0"
  status: "Active"
  owner: "Documentation Team"
  title: "Documentation Protocol"
  description: "Standard protocol for all documentation within the agent-doc-system"
content:
  overview: "This document defines the standard protocol for all documentation within the agent-doc-system. It ensures consistency, maintainability, and machine-actionable documentation across all components."
  key_components: "Documentation Structure, Validation Requirements, Best Practices, Feedback System"
  sections:
    - title: "Overview"
      content: "This document defines the standard protocol for all documentation within the agent-doc-system. It ensures consistency, maintainability, and machine-actionable documentation across all components."
    - title: "Documentation Structure"
      content: "Required sections and file organization guidelines"
    - title: "Validation Requirements"
      content: "Schema validation and automated validation process"
    - title: "Best Practices"
      content: "Guidelines for writing and maintaining documentation"
    - title: "Feedback System"
      content: "Process for providing and managing documentation feedback"
  changelog:
    - version: "1.1.0"
      date: "2024-12-29"
      changes:
        - "Added Claude Code optimization framework"
        - "Enhanced validation with Pydantic v2 models"
        - "Added new message types: workflow_request, validation_request, documentation_update"
        - "Implemented comprehensive testing framework with pytest"
        - "Added CI/CD pipeline with automated validation"
        - "Enhanced security with OWASP compliance checking"
    - version: "1.0.0"
      date: "2024-03-21"
      changes:
        - "Initial release of the Documentation Protocol"
feedback:
  rating: 97
  comments: "Comprehensive protocol with clear guidelines and examples"
  observations:
    - what: "Well-structured validation requirements"
      impact: "Ensures consistent documentation quality"
    - what: "Clear feedback system"
      impact: "Facilitates continuous improvement"
  suggestions:
    - action: "Add more real-world examples"
      priority: "Medium"
  status:
    value: "Approved"
    updated_by: "Documentation Team"
    date: "2024-03-21"
    validation: "Passed"
    implementation: "Complete"
```

## Overview

This document defines the standard protocol for all documentation within the agent-doc-system. It ensures consistency, maintainability, and machine-actionable documentation across all components.

## Documentation Structure

### Required Sections

1. **Title**
   - Clear, descriptive title
   - No special characters except hyphens and underscores

2. **Machine-Actionable Metadata**
   - YAML code block with required fields
   - Must be at the start of the document
   - Required fields:
     - `schema`: URL to schema definition
     - `version`: Semantic version (X.Y.Z)
     - `status`: Active/Deprecated/Draft
     - `owner`: Team or individual responsible
     - `title`: Document title
     - `description`: Brief description

3. **Content Structure**
   - `overview`: Brief description of the document's purpose
   - `key_components`: List of main components or features
   - `sections`: Array of sections with title and content
   - `changelog`: Version history with dates and changes

4. **Feedback Section**
   - `rating`: Integer between 1-100
   - `comments`: General feedback
   - `observations`: Array of what/impact pairs
   - `suggestions`: Array of action/priority pairs
   - `status`: Approval and validation status

### File Organization

1. **Framework Documentation**
   - Location: `framework/docs/`
   - Core system documentation
   - Protocol definitions
   - Templates and examples

2. **Project Documentation**
   - Location: `projects/{project_name}/docs/`
   - Project-specific documentation
   - Setup guides
   - Architecture overviews

3. **Component Documentation**
   - Location: `projects/{project_name}/{component_name}/docs/`
   - Component-specific documentation
   - API references
   - Usage examples

## Validation Requirements

### Schema Validation

All documentation must validate against the schema defined in `framework/schemas/document_protocol.yml`. The schema enforces:

1. **Required Fields**
   - Title
   - Metadata section
   - Content section
   - Feedback section

2. **Metadata Format**
   - Valid schema URL
   - Semantic versioning
   - Valid status values
   - Owner information

3. **Content Structure**
   - Proper markdown formatting
   - Valid code blocks
   - Required sections present

### Automated Validation

Use the validation script to check documentation:

```bash
./framework/scripts/validate.sh
```

The script checks:
- Schema compliance
- Required sections
- Metadata format
- Markdown syntax
- Code block formatting

## Best Practices

### Writing Documentation

1. **Clarity**
   - Use clear, concise language
   - Avoid jargon unless necessary
   - Include examples
   - Use diagrams when helpful

2. **Structure**
   - Follow the required sections
   - Use consistent formatting
   - Include a table of contents for long documents
   - Link related documents

3. **Maintenance**
   - Keep documentation up to date
   - Update changelog with changes
   - Review regularly
   - Remove outdated information

### Code Examples

1. **Format**
   - Use proper code blocks with language specification
   - Include comments
   - Show expected output
   - Use realistic examples

2. **Content**
   - Show best practices
   - Include error handling
   - Demonstrate common use cases
   - Explain complex operations

## Feedback System

### Observations

Document any issues or improvements needed:

1. **Type**
   - `bug`: Documentation errors
   - `improvement`: Enhancement suggestions
   - `clarification`: Unclear content
   - `outdated`: Needs updating

2. **Impact**
   - `high`: Critical issues
   - `medium`: Important improvements
   - `low`: Minor suggestions

3. **Priority**
   - `p0`: Immediate attention required
   - `p1`: High priority
   - `p2`: Medium priority
   - `p3`: Low priority

### Suggestions

Provide actionable suggestions for improvements:

1. **Format**
   - Clear description
   - Specific changes
   - Expected outcome
   - Implementation steps

2. **Review**
   - Team review required
   - Implementation timeline
   - Success criteria
   - Follow-up actions

## Changelog

- **1.1.0** (2024-12-29): Added Claude Code optimization framework, enhanced validation with Pydantic v2, new message types, comprehensive testing, CI/CD pipeline, and OWASP security compliance
- **1.0.0** (2024-03-21): Initial release of the Documentation Protocol 
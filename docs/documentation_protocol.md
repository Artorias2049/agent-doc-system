# Documentation Protocol

## Machine-Actionable Metadata
```yaml
schema: "https://schema.org/TechnicalDocument"
version: "1.1.0"
status: "Active"
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

All project-specific documentation must be stored in the following locations:

1. **Core Documentation**: `docs/` directory
   - System-wide documentation
   - Protocols and standards
   - General guidelines

2. **Project-Specific Documentation**: `docs/projects/<project_name>/`
   - Project-specific guides
   - Implementation details
   - Project workflows
   - Project-specific protocols

3. **Component Documentation**: `docs/components/<component_name>/`
   - Component-specific documentation
   - API references
   - Technical specifications

4. **Documentation Templates**: `docs/templates/`
   - Project templates: `docs/templates/projects/`
     - `overview.md`: Project overview template
     - `setup.md`: Project setup guide template
   - Component templates: `docs/templates/components/`
     - `overview.md`: Component overview template
     - `api.md`: API documentation template

Each project and component must maintain its own documentation directory with the following structure:
```
docs/
├── projects/
│   └── <project_name>/
│       ├── overview.md
│       ├── setup.md
│       └── workflows/
├── components/
│   └── <component_name>/
│       ├── overview.md
│       ├── api.md
│       └── examples/
└── templates/
    ├── projects/
    │   ├── overview.md
    │   └── setup.md
    └── components/
        ├── overview.md
        └── api.md
```

### Metadata Format

```yaml
schema: "https://schema.org/TechnicalDocument"
id: "unique-id"
version: "x.y.z"
last_updated: "ISO8601_timestamp"
status: "Active|Deprecated|Archived"
author: "Author Name"
```

## Documentation Types

1. **Technical Documentation**
   - API references
   - Architecture guides
   - Implementation details

2. **User Documentation**
   - User guides
   - Tutorials
   - FAQs

3. **Process Documentation**
   - Workflows
   - Procedures
   - Guidelines

## Writing Guidelines

1. Use clear, concise language
2. Include code examples
3. Add diagrams when helpful
4. Keep documentation up to date
5. Follow style guide

## Validation Process

1. Run doc_validation.sh
2. Check metadata format
3. Verify required sections
4. Test code examples
5. Review for clarity

## Best Practices

1. Update documentation with code changes
2. Use consistent formatting
3. Include examples
4. Add changelog entries
5. Regular reviews

## Tools and Resources

1. Markdown editor
2. Validation scripts
3. Style guide
4. Templates
5. Examples

## Troubleshooting

Common issues and solutions:

1. **Validation Errors**
   - Check metadata format
   - Verify required sections
   - Update changelog

2. **Formatting Issues**
   - Use consistent style
   - Follow templates
   - Validate markdown

## Future Improvements

Planned enhancements:
- Automated validation
- Documentation templates
- Version control integration
- Search functionality

## Changelog

- **1.1.0** (2024-03-21): Updated structure and removed outdated references
- **1.0.0** (2024-03-21): Initial release of the Documentation Protocol 
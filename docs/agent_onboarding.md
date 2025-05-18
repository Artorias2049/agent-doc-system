# Agent Onboarding Guide

## Machine-Actionable Metadata
```yaml
schema: "https://schema.org/TechnicalDocument"
version: "1.0.0"
status: "Active"
```

## Overview

This document serves as the single source of truth for understanding the agent-doc-system. It provides a comprehensive overview of the system's architecture, protocols, validation requirements, and best practices.

## Key Components

### 1. Documentation Protocol
- **Purpose:** Defines how all documentation should be structured and validated.
- **Key Files:**
  - [Documentation Protocol](documentation_protocol.md)
  - [Example Document](example.md)

### 2. Agent Communication Protocol
- **Purpose:** Standardizes message formats and agent interactions.
- **Key Files:**
  - [Agent Communication](agent_communication.md)
  - [Agent Communication Schema](../schemas/agent_communication.yml)

### 3. Validation Scripts
- **Purpose:** Automated scripts to check documentation, schemas, and agent messages for compliance.
- **Key Files:**
  - [Documentation Validation](../scripts/doc_validation.sh)
  - [Agent Message Validation](../scripts/validate_agent_messages.py)

### 4. Schemas
- **Purpose:** YAML files that define the structure for documentation and agent messages.
- **Key Files:**
  - [Document Protocol Schema](../schemas/document_protocol.yml)
  - [Feedback Framework Schema](../schemas/feedback_framework.yml)

## Required Practices

### Metadata
Every documentation file must include a `## Machine-Actionable Metadata` section with a YAML code block containing at least:
- `schema`
- `version`
- `status`

### Changelog
Every documentation file must have a `## Changelog` section.

### Consistent Structure
Follow the section order:
1. Title
2. Metadata
3. Overview
4. Main Content
5. Changelog

### Validation
Run `./scripts/doc_validation.sh` before merging or releasing to ensure compliance.

## Communication Protocol

All agent messages must follow the JSON schema defined in `schemas/agent_communication.yml`. Use the provided Python classes (e.g., `AgentProtocol`) for sending, receiving, and tracking messages.

Message types include:
- `request`
- `response`
- `notification`
- `error`
- `status_update`

## Best Practices

- Keep documentation and schemas up to date with code changes.
- Use clear, concise language and provide examples.
- Regularly review and improve documentation and communication protocols.
- Use the feedback framework to suggest improvements or report issues.

## Validation & Troubleshooting

Use the validation script to check for:
- Proper metadata and changelog sections in docs.
- Valid agent message files.
- Valid YAML schemas.
- Markdown formatting issues (if `remark-cli` is installed).

If validation fails, check the error messages for missing or misformatted sections.

## Where to Find Things

- **Documentation:** `docs/`
- **Schemas:** `schemas/`
- **Validation Scripts:** `scripts/`
- **Agent Communication Code:** `agent_communication/`

## Getting Started

1. Read the main documentation files in `docs/`.
2. Review the schemas in `schemas/` to understand required formats.
3. Use the provided Python classes and scripts for agent communication and validation.
4. Run the validation script before submitting changes.

## Quickstart Checklist

- [ ] Read the onboarding doc
- [ ] Review the schemas
- [ ] Run the validation script
- [ ] Follow the commit/PR guidelines

## Changelog

- **1.0.0** (2024-03-21): Initial release of the Agent Onboarding Guide 
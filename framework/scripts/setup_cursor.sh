#!/bin/bash
# agent_doc_system/scripts/setup_cursor.sh
# Sets up the Cursor integration files for the documentation system

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Get the parent directory (agent_doc_system)
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
# Get the target directory (where to set up Cursor files)
TARGET_DIR="${1:-$(pwd)}"

echo "Setting up Cursor integration for documentation system..."
echo "Target directory: $TARGET_DIR"

# Create necessary directories
mkdir -p "$TARGET_DIR/.cursor/rules"
mkdir -p "$TARGET_DIR/.cursor/config"
mkdir -p "$TARGET_DIR/.cursor/scripts"
mkdir -p "$TARGET_DIR/.vscode"

# Create doc_protocol.mdc
cat > "$TARGET_DIR/.cursor/rules/doc_protocol.mdc" << 'EOF'
---
description: Agent Documentation Standards
globs: "agent_doc_system/docs/**/*.md"
schema: "agent_doc_system/schemas/document_protocol.yml"
---
# Documentation Protocol Rules

## Structural Requirements
- All documents must contain YAML metadata header
- Section headers require anchor tags {#section-name}
- Code blocks must specify language identifier
- Change history maintained in ## Changelog

## Validation Pipeline
1. Schema validation via remark-lint-frontmatter-schema
2. Structural check for required sections
3. Anchor tag uniqueness verification
4. Link integrity check

## Agent Interaction Patterns
```
sequenceDiagram
Agent A->>Agent B: POST /document/update
Agent B->>Agent C: Validation Request
Agent C->>Agent B: Validation Signature
Agent B->>Agent A: Approval Notification
```

## Failure Modes
- **Invalid Metadata**: Reject with error code 400
- **Conflict**: Initiate merge resolution workflow
- **Timeout**: Retry with exponential backoff
EOF

# Create doc_validation.mdc
cat > "$TARGET_DIR/.cursor/rules/doc_validation.mdc" << 'EOF'
---
description: Documentation Validation Pipeline
globs: "agent_doc_system/docs/**/*.md"
---
validation_steps:
  - tool: remark-lint-frontmatter-schema
    schema: agent_doc_system/schemas/document_protocol.yml
  - tool: custom-validator
    script: agent_doc_system/scripts/validate_docs.py
  - tool: link-integrity
    config: .cursor/config/link_rules.yml
EOF

# Create security_rules.mdc
cat > "$TARGET_DIR/.cursor/rules/security_rules.mdc" << 'EOF'
---
description: Documentation Security Rules
globs: "agent_doc_system/docs/**/*.md"
---
security_controls:
  - type: content-validation
    level: strict
  - type: metadata-integrity
    level: enforced
  - type: permission-model
    level: role-based
EOF

# Create python-expert.mdc
cat > "$TARGET_DIR/.cursor/rules/python-expert.mdc" << 'EOF'
---
description: Expert Python Programmer Agent Rules
---
# Expert Python Programmer Agent Rules

## Summary

This document defines the behavior, capabilities, and knowledge base of an expert Python programmer agent designed to assist with all aspects of Python development. The agent embodies best practices in Python programming, software architecture, testing methodologies, performance optimization, and more.

## Python Expertise Profile

### Core Competencies

- Acts as a world-class Python developer with deep expertise from Python fundamentals to advanced concepts
- Provides guidance, code samples, analysis, and solutions for any Python-related task
- Follows PEP standards and modern Python best practices
- Thinks like a principal-level engineer who has deep conceptual and practical Python knowledge


## Code Development Standards

### Python Style \& Standards

- Follow @PEP 8 style guidelines strictly
- Adhere to @PEP 257 for docstring conventions
- Use descriptive variable/function names using snake_case
- Maintain line length under 88 characters (Black formatter standard)
- Use type hints (PEP 484) to improve code clarity and enable static type checking
- Use f-strings for string formatting except in log formatting or when inappropriate
- Employ context managers (`with` statements) for resource management


### Code Structure

- Apply proper indentation (4 spaces, never tabs)
- Organize imports in standard order: standard library, third-party, local application imports
- Separate import groups with blank lines
- Limit function length to promote readability (max ~40 lines)
- Maintain a logical flow of code with appropriate comments for complex logic
- Use appropriate whitespace to improve readability


### Modern Python Features

- Leverage Python 3.10+ features when available (pattern matching, union operators)
- Use dataclasses or named tuples for data containers
- Employ walrus operator `:=` when it improves readability
- Utilize advanced unpacking and star expressions appropriately
- Implement proper type annotations following PEP 585 (Python 3.9+)


## Software Design Principles

### Architecture

- Follow SOLID principles adapted to Python context
- Prefer composition over inheritance
- Design for testability and maintainability
- Implement proper separation of concerns
- Use dependency injection where appropriate
- Apply Factory pattern for object creation when beneficial


### Package Structure

- Organize code in logical modules with clear responsibilities
- Follow standard project structure:

```
project_name/
├── README.md
├── requirements.txt
├── setup.py
├── project_name/
│   ├── __init__.py
│   ├── core.py
│   ├── helpers.py
│   └── submodule/
│       ├── __init__.py
│       └── functionality.py
├── tests/
│   ├── __init__.py
│   └── test_functionality.py
└── docs/
```

- Use `__init__.py` files to create clean public interfaces


## Testing \& Quality Assurance

### Testing Strategy

- Write unit tests with pytest for all functions/methods
- Implement integration tests for component interactions
- Create functional tests for end-to-end workflows
- Use fixtures and parametrization to minimize test code duplication
- Aim for high test coverage (>80% minimum)


### Testing Best Practices

- Follow Arrange-Act-Assert pattern
- Use descriptive test names that explain the test purpose
- Implement test isolation to prevent dependencies between tests
- Properly mock external dependencies
- Test edge cases and error conditions


### CI/CD Integration

- Configure pre-commit hooks for linting and formatting
- Set up automated testing with GitHub Actions or similar
- Implement test coverage reporting
- Enforce code quality gates


## Performance \& Optimization

### Performance Best Practices

- Use appropriate data structures (dictionaries for lookups, sets for uniqueness checks)
- Apply list comprehensions and generator expressions when appropriate
- Leverage built-in functions and standard library tools
- Identify and refactor bottlenecks using profiling tools
- Consider parallelization with concurrent.futures for CPU-bound tasks
- Use asyncio for I/O-bound operations


### Memory Management

- Be aware of memory consumption for large datasets
- Use generators for processing large sequences
- Implement proper resource cleanup
- Avoid memory leaks in long-running applications


## Error Handling \& Debugging

### Exception Handling

- Use specific exception types instead of catching broad exceptions
- Implement custom exception classes for domain-specific errors
- Include context information in exceptions
- Log appropriate information during exception handling
- Use try/except only around code that may raise exceptions


### Debugging Techniques

- Add proper logging with appropriate log levels
- Use debuggers effectively (pdb, ipdb, IDE debuggers)
- Implement descriptive error messages
- Trace problems methodically through stack traces
- Add diagnostic logging statements strategically


## Python Libraries \& Frameworks

### Standard Library

- Maximize use of standard library modules before adding dependencies
- Demonstrate deep knowledge of standard library capabilities
- Know when to use common modules like:
    - collections (defaultdict, Counter, namedtuple)
    - itertools for efficient iteration
    - functools for higher-order functions
    - pathlib for file system operations
    - concurrent.futures for parallelism


### Common External Libraries

- Understand and recommend appropriate libraries for common tasks:
    - Data science: NumPy, pandas, scikit-learn
    - Web development: Flask, FastAPI, Django
    - Testing: pytest, unittest
    - Database: SQLAlchemy, psycopg2, pymongo
    - CLI applications: click, typer
    - HTTP clients: requests, httpx
    - Task queues: Celery, RQ


## Security Considerations

### Security Best Practices

- Never hard-code sensitive information (use environment variables)
- Implement proper input validation
- Use secure coding practices (avoid SQL injection, etc.)
- Follow OWASP guidelines for web applications
- Apply principle of least privilege
- Use security libraries rather than custom implementations


### Dependency Management

- Keep dependencies updated to avoid security vulnerabilities
- Use dependency locking (pip-compile, poetry)
- Scan dependencies for known vulnerabilities


## Documentation Standards

### Code Documentation

- Write clear, concise docstrings for modules, classes, and functions
- Follow Google or NumPy docstring format consistently
- Document parameters, return values, and exceptions
- Include examples in docstrings for complex functions
- Add comments for complex algorithms explaining the approach


### Project Documentation

- Maintain comprehensive README.md files
- Include installation and usage instructions
- Document configuration options
- Provide examples for common use cases
- Generate API documentation with tools like Sphinx


## Advanced Python Concepts

### Metaprogramming

- Use decorators to extend functionality without modifying functions
- Apply class decorators when appropriate
- Understand metaclasses and their appropriate uses
- Implement descriptors for property management
- Use __getattr__ and similar methods judiciously


### Concurrency \& Parallelism

- Choose appropriate concurrency model:
    - Threading for I/O-bound tasks
    - Multiprocessing for CPU-bound tasks
    - Asyncio for high-performance I/O
- Understand the GIL and its implications
- Implement proper synchronization mechanisms
- Handle concurrency edge cases (deadlocks, race conditions)


### Python Internals

- Understand Python's execution model
- Know how Python manages memory
- Be aware of reference counting and garbage collection
- Understand method resolution order
- Know the differences between CPython, PyPy, and other implementations


## Problem-Solving Approach

### Analysis \& Solution Design

- Break down complex problems methodically
- Consider multiple solution approaches before implementation
- Evaluate trade-offs between simplicity, performance, and maintainability
- Design with future requirements in mind
- Implement solutions incrementally with testing at each stage


### Code Review Mindset

- Review code critically for correctness, clarity, and performance
- Suggest meaningful improvements with clear explanations
- Look for security vulnerabilities and edge cases
- Consider maintainability and readability
- Provide constructive feedback


## Interactions \& Communication

### Communication Style

- Provide clear, concise explanations with appropriate detail
- Adapt technical depth to the user's level of understanding
- Use code examples to illustrate concepts
- Explain reasoning behind recommendations
- Offer multiple approaches when appropriate


### Problem Diagnosis

- Ask clarifying questions when requirements are ambiguous
- Request additional context when needed
- Step through problems systematically
- Explore root causes rather than just symptoms
- Consider edge cases and potential failure modes


## References \& Resources

When appropriate, reference these high-quality resources for Python development:

- @Python Official Documentation
- @Real Python Tutorials
- @Python Enhancement Proposals (PEPs)
- @Fluent Python by Luciano Ramalho
- @Python Cookbook by David Beazley
EOF

# Create monitoring.json
cat > "$TARGET_DIR/.cursor/config/monitoring.json" << 'EOF'
{
  "doc_validation": {
    "interval": "30m",
    "notifiers": ["console", "log"],
    "thresholds": {
      "error_count": 5,
      "warning_count": 10
    }
  }
}
EOF

# Create doc_validation.sh for Cursor
cat > "$TARGET_DIR/.cursor/scripts/doc_validation.sh" << 'EOF'
#!/bin/bash
# .cursor/scripts/doc_validation.sh

# Run basic remark validation
echo "Running remark validation..."
remark agent_doc_system/docs/ --frail

# Run Python-based validation
echo "Running agent-based validation..."
agent_doc_system/scripts/validate_docs.py
EOF

# Make script executable
chmod +x "$TARGET_DIR/.cursor/scripts/doc_validation.sh"

# Create link_rules.yml
cat > "$TARGET_DIR/.cursor/config/link_rules.yml" << 'EOF'
link_validation:
  internal_patterns:
    - "agent_doc_system/docs/**/*.md"
  verify_anchors: true
  allow_external: true
  external_check: false
EOF

# Create VSCode settings
cat > "$TARGET_DIR/.vscode/settings.json" << 'EOF'
{
  "editor.formatOnSave": true,
  "editor.insertSpaces": true,
  "editor.tabSize": 2,
  "files.associations": {
    "*.md": "markdown"
  },
  "markdown.validate.enabled": true,
  "yaml.schemas": {
    "agent_doc_system/schemas/document_protocol.yml": "agent_doc_system/docs/**/*.md"
  },
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "cursor.rules": "on",
  "cursor.validation": "on"
}
EOF

# Create VSCode tasks
cat > "$TARGET_DIR/.vscode/tasks.json" << 'EOF'
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Validate Documentation",
      "type": "shell",
      "command": "./agent_doc_system/scripts/doc_validation.sh",
      "group": "test",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Generate Example Document",
      "type": "shell",
      "command": "./agent_doc_system/scripts/generate_example_doc.py \"New Document\" \"Documentation description\" \"${env:USER}\"",
      "group": "build",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    }
  ]
}
EOF

# Create VSCode extensions recommendations
cat > "$TARGET_DIR/.vscode/extensions.json" << 'EOF'
{
  "recommendations": [
    "yzhang.markdown-all-in-one",
    "davidanson.vscode-markdownlint",
    "redhat.vscode-yaml",
    "ms-python.python",
    "cursor.cursor"
  ]
}
EOF

echo "✅ Cursor integration files have been set up successfully."
echo "✅ VSCode configuration has been set up successfully."
echo "You can now use the documentation system with Cursor in this project." 
# Claude Code Configuration for Agent Documentation System

This CLAUDE.md file configures Claude Code for optimal productivity with the agent-doc-system framework, focusing on Python development best practices and the agent communication protocol.

## Project Context and Architecture

### Core Project Structure
```
agent-doc-system/
├── framework/                  # Core framework components
│   ├── agent_communication/   # Enhanced agent protocol
│   │   ├── core/             # Pydantic models and enhanced protocol
│   │   ├── config/           # Agent settings
│   │   └── history/          # Message storage
│   ├── docs/                 # Framework documentation
│   │   ├── components/       # Component documentation
│   │   └── templates/        # Documentation templates
│   ├── schemas/              # YAML schema definitions
│   ├── scripts/              # Validation and utility scripts
│   └── validators/           # Python validation framework
├── tests/                    # Comprehensive pytest suite
├── project_docs/             # Project-specific documentation
└── pyproject.toml           # Poetry configuration
```

### Technology Stack
- **Python 3.9+** with Poetry dependency management
- **Pydantic v2** for type-safe message validation
- **Rich & Click** for enhanced CLI experience
- **Pytest** with 90%+ coverage requirement
- **MyPy** strict type checking
- **Black & Ruff** for code formatting and linting

## Enhanced Agent Communication Protocol

### Message Types
The framework supports 7 message types with full Pydantic validation:

1. **test_request** - Unit/integration/e2e/performance testing
2. **test_result** - Test execution results with artifacts
3. **status_update** - Agent state and progress tracking
4. **context_update** - Context data management
5. **workflow_request** - Multi-step agent workflows
6. **validation_request** - Schema/doc validation requests
7. **documentation_update** - Automated doc generation

### Usage Examples
```python
# Example using the agent communication script
python framework/scripts/agent_communication.py --action send --type "test_request" --sender "agent1" --content '{
  "test_type": "unit",
  "test_file": "tests/test_models.py",
  "parameters": {
    "environment": "development",
    "verbose": true
  }
}'

# Validate messages
python framework/validators/validator.py --target messages

# Run validation script
./framework/scripts/validate.sh
```

## Development Workflows

### Test-Driven Development Protocol
1. **Red Phase**: Create failing tests using pytest with type hints
2. **Green Phase**: Implement minimal code with Pydantic models
3. **Refactor**: Optimize with full type safety
4. **Validate**: Run comprehensive test suite

```bash
# TDD workflow example
pytest tests/test_models.py::TestAgentMessage::test_message_creation_valid -v
# Implement feature
pytest tests/ --cov=framework --cov-fail-under=90
mypy framework/agent_communication/core/ --strict
```

### Pre-commit Quality Gates
All code changes are validated through:
- **Black** formatting (line length 100)
- **MyPy** strict type checking
- **Ruff** linting with performance optimizations
- **Bandit** security scanning
- **Pytest** with 90% coverage requirement
- **Schema validation** for YAML files
- **Documentation validation** using enhanced validator

## Development Commands

### Testing and Validation
```bash
# Run full test suite with coverage
pytest tests/ --cov=framework --cov-report=html --cov-report=term-missing

# Run specific test categories
pytest tests/test_models.py -v                    # Pydantic model tests
pytest tests/test_enhanced_protocol.py -v        # Protocol integration tests

# Type checking
mypy framework/agent_communication/core/ --strict

# Linting and formatting
black framework/ tests/
ruff check framework/ tests/

# Security scanning
bandit -r framework/

# Schema validation
python framework/validators/validator.py --target schemas
```

### Agent Communication Operations
```bash
# Send messages
python framework/scripts/agent_communication.py --action send --type <type> --sender <sender> --content <json_content>

# Read messages
python framework/scripts/agent_communication.py --action read

# Cleanup old messages
python framework/scripts/agent_communication.py --action cleanup --days 7

# Validate all components
./framework/scripts/validate.sh
```

## Type Safety and Validation

### Pydantic Model Integration
All agent messages use Pydantic v2 for:
- **Runtime validation** with detailed error messages
- **Type coercion** and automatic serialization
- **Performance optimization**
- **IDE integration** with full autocomplete support

### Validation Levels
- **Basic**: Syntax and type validation
- **Enhanced**: Cross-reference and consistency checks (default)
- **Strict**: Security compliance and best practices

## Testing Framework

### Test Categories
- **Unit Tests**: Pydantic model validation
- **Integration Tests**: End-to-end protocol communication
- **Performance Tests**: Message creation and validation benchmarks
- **Security Tests**: Input validation and injection prevention

### Coverage Requirements
- Minimum 90% test coverage for all framework code
- All public methods must have corresponding tests
- Integration tests for agent communication workflows

## Security and Compliance

### Security Features
- **Input validation** prevents injection attacks
- **Secret detection** in pre-commit hooks
- **Dependency scanning** with safety checks
- **Access control** through permission configuration
- **Audit logging** for all agent operations

### Permission System
```json
{
  "permissions": {
    "allow": [
      "Bash(poetry*)", "Bash(pytest*)", "Bash(mypy*)",
      "Edit(framework/**/*.py)", "Edit(tests/**/*.py)"
    ],
    "deny": [
      "Bash(rm -rf*)", "Edit(*/secrets.py)"
    ],
    "restricted": [
      "Edit(framework/schemas/*): require_validation"
    ]
  }
}
```

## Troubleshooting and Debugging

### Common Resolution Patterns
| Issue | Command | Expected Outcome |
|-------|---------|------------------|
| Type errors | `mypy framework/ --strict` | Zero type errors |
| Test failures | `pytest tests/ -x -v` | Detailed failure info |
| Schema issues | `python framework/validators/validator.py --target schemas` | Validation report |
| Linting issues | `ruff check framework/ --fix` | Auto-fixed issues |

### Debug Mode
```bash
# Enable verbose debugging for agent communication
python framework/scripts/agent_communication.py --action send --type test_request --sender agent1 --content {...} --verbose

# Validate with detailed output
python framework/validators/validator.py --target messages --verbose
```

## Integration Examples

### Complete Development Workflow
```bash
# 1. Start development
git checkout -b feature/new-message-type

# 2. Create tests first (TDD)
pytest tests/test_new_feature.py --create-missing

# 3. Implement feature with validation
# Edit framework/agent_communication/core/models.py
# Add new message type with Pydantic validation

# 4. Run validation and tests
./framework/scripts/validate.sh
pytest tests/ --cov=framework --cov-fail-under=90
mypy framework/ --strict

# 5. Create pull request
git add . && git commit -m "feat: add new message type with validation"
git push origin feature/new-message-type
```

### Message Processing Pipeline
```bash
# Send test request
python framework/scripts/agent_communication.py --action send --type "workflow_request" --sender "coordinator" --content '{
  "workflow_name": "process_documentation",
  "steps": [
    {"name": "validate_syntax", "action": "validate"},
    {"name": "check_links", "action": "verify"},
    {"name": "update_metadata", "action": "update"}
  ]
}'

# Monitor messages
python framework/scripts/agent_communication.py --action read
```

## Environment Configuration

### Development Environment
```bash
# Install dependencies
poetry install

# Set up pre-commit hooks
pre-commit install

# Run initial validation
./framework/scripts/validate.sh
```

### Production Environment
```bash
# Install production dependencies only
poetry install --no-dev

# Run comprehensive validation
python framework/validators/validator.py --target all --validation_level strict
```

This configuration optimizes Claude Code for Python development with:
1. **Type-safe development** with Pydantic models
2. **Comprehensive testing** with pytest and coverage requirements
3. **Code quality** through automated linting and formatting
4. **Security** with automated scanning and validation
5. **Clear workflows** for development and deployment

The framework provides a solid foundation for agent communication systems with full validation, testing, and documentation capabilities.
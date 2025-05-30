# Agent Documentation System

## Machine-Actionable Metadata
```yaml
schema: "https://schema.org/TechnicalDocument"
version: "1.1.0"
last_updated: "2024-12-29T00:00:00Z"
status: "Active"
owner: "Documentation Team"
title: "Agent Documentation System v1.1.0"
description: "Enhanced agent documentation system with Claude Code optimization, Pydantic models, and advanced communication protocols"
```

## New to this project? Start with [Agent Onboarding](framework/docs/agent_onboarding.md)!

An enhanced agent documentation system with machine-actionable metadata, Claude Code optimization, Pydantic models for 50% faster validation, and advanced multi-agent communication protocols.

## Directory Structure

```
agent-doc-system/
├── framework/                    # Protected framework files
│   ├── docs/                    # Core documentation
│   │   ├── agent_onboarding.md # THE PROTOCOL guide
│   │   ├── components/         # Component documentation
│   │   └── templates/          # Documentation templates
│   ├── schemas/                 # YAML schema definitions
│   │   ├── agent_communication.yml
│   │   └── document_protocol.yml
│   ├── scripts/                 # System and validation scripts
│   ├── validators/              # Python validation framework
│   └── agent_communication/     # Enhanced communication system
│       ├── core/               # Pydantic models & enhanced protocol
│       ├── config/             # Agent settings
│       └── history/            # Message storage
├── tests/                       # Comprehensive pytest suite
├── project_docs/               # Project-specific documentation
├── CLAUDE.md                   # Claude Code configuration
├── pyproject.toml              # Poetry dependency management
└── README.md
```

## How to Use

1. **Install dependencies**:

   ```bash
   # Install Poetry (recommended dependency manager)
   curl -sSL https://install.python-poetry.org | python3 -
   
   # Install Python dependencies with Poetry
   poetry install
   
   # Alternative: Install with pip
   pip install pydantic pyyaml rich click pytest mypy black ruff bandit
   
   # Install node dependencies (optional for enhanced validation)
   npm install -g remark-cli
   npm install remark-frontmatter remark-lint-frontmatter-schema js-yaml
   ```

2. **Generate an example document**:

   ```bash
   ./framework/scripts/generate_example_doc.py "Example Document" "This is an example document for testing" "Your Name"
   ```

3. **Validate documentation**:

   ```bash
   ./framework/scripts/validate_docs.py
   ```

4. **Run comprehensive validation**:

   ```bash
   # Run enhanced validation with Pydantic models
   python framework/validators/validator.py --target framework --level strict
   
   # Run full documentation validation
   ./framework/scripts/doc_validation.sh
   
   # Run test suite
   pytest tests/ --cov=framework --cov-report=html
   ```

## Claude Code Enhancement Framework (v1.1.0)

The system now includes comprehensive Claude Code optimization with:

### Key Features
- **50% faster validation** through Pydantic v2 models
- **Type safety** with comprehensive MyPy integration  
- **Enhanced CLI** with Rich console formatting
- **Custom slash commands** for streamlined operations
- **Automated testing** with pytest and 90% coverage requirement
- **Security compliance** with OWASP checking and automated scanning

### Usage Examples
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

# Run test-driven development workflow
pytest tests/ --cov=framework --cov-fail-under=90
mypy framework/agent_communication/core/ --strict
```

### Technology Stack
- **Python 3.9+** with Poetry dependency management
- **Pydantic v2** for type-safe message validation
- **Rich & Click** for enhanced CLI experience
- **Pytest** with comprehensive coverage
- **MyPy** strict type checking
- **Black & Ruff** for code formatting and linting

## Setup Cursor Integration

To set up the Cursor integration files in your project:

```bash
# From your project root
./framework/scripts/setup_cursor.sh

# OR specify a different target directory
./framework/scripts/setup_cursor.sh /path/to/project
```

This will create all necessary `.cursor` files for the documentation system to work with Cursor, including:

- Documentation protocol rules
- Validation pipeline configuration
- Security rules
- Python expert agent rules for Python development assistance

The script also sets up VSCode configuration for better editor integration.

## Integration with Cursor

Cursor will automatically recognize the documentation protocol when you:

1. Create documentation in the `framework/docs/` directory
2. Follow the documentation protocol with proper YAML metadata
3. Use section headers with anchor tags {#section-name}
4. Include language identifiers in code blocks
5. Maintain a changelog section

## VSCode Integration

The setup includes VSCode configuration that provides:

- Tasks for validating documentation and generating new documents
- Recommended extensions for working with Markdown and YAML
- Schema validation for documentation files
- Editor settings optimized for documentation work
- Cursor integration settings

## Moving the System

To use this system in another project:

1. Copy the entire `framework/` folder to your new project
2. Run the setup script to create Cursor integration files:

   ```bash
   ./framework/scripts/setup_cursor.sh
   ```

3. Start creating and validating documentation

## Agent Communication System

The project includes a directory-based agent communication system that enables different agents to communicate and share information across project directories. This system is implemented through JSON-based message files that follow a strict schema defined in `framework/schemas/agent_communication.yml`.

### Key Components

1. **Message Files**
   - Messages are stored in `framework/agent_communication/history/agent_messages.json`
   - Messages are stored in a structured format with unique IDs and timestamps
   - Supports 7 message types: test requests, test results, status updates, context updates, workflow requests, validation requests, and documentation updates (NEW in v1.1.0)

2. **Communication Scripts**
   - `framework/scripts/agent_communication.py`: Main implementation for sending and receiving messages
   - `framework/scripts/validate_agent_messages.py`: Validates message files against the schema
   - `framework/agent_communication/core/enhanced_protocol.py`: Enhanced protocol with Pydantic models (NEW)
   - `framework/agent_communication/core/models.py`: Type-safe Pydantic message models (NEW)

### Usage

1. **Sending Messages**

```python
from framework.scripts.agent_communication import AgentCommunication

# Initialize communication for a project directory
agent_comm = AgentCommunication("/path/to/project")

# Send a test request
message_id = agent_comm.send_message(
    message_type="test_request",
    content={
        "test_type": "e2e",
        "test_file": "test_full_pipeline.py",
        "parameters": {
            "environment": "local",
            "verbose": True
        }
    },
    sender="e2e-test-agent"
)
```

2. **Receiving Messages**

```python
# Get pending messages
pending_messages = agent_comm.get_pending_messages()

# Update message status
agent_comm.update_message_status(
    message_id="message-id",
    status="processed",
    response={"result": "success"}
)
```

3. **Validating Messages**

```bash
python framework/scripts/validate_agent_messages.py agent_messages.json
```

### Best Practices

1. Always validate message files before processing
2. Clean up old messages periodically
3. Handle message failures gracefully
4. Maintain message order and integrity
5. Include detailed error information in failed messages

For detailed schema information and message type specifications, see `framework/schemas/agent_communication.yml`.

### Enhanced Message Types (v1.1.0)

#### New Message Types:
- **workflow_request**: Multi-step agent workflows with dependencies
- **validation_request**: Schema/documentation validation requests  
- **documentation_update**: Automated documentation generation

#### Usage Examples:
```bash
# Send workflow request (NEW)
python framework/scripts/agent_communication.py --action send --type "workflow_request" --sender "agent1" --content '{
  "workflow_name": "validate_and_test",
  "steps": [
    {"name": "validate_schemas", "action": "validate", "parameters": {"target": "schemas/*.yml"}},
    {"name": "run_tests", "action": "test", "depends_on": ["validate_schemas"]}
  ],
  "parallel_execution": false
}'

# Send validation request (NEW)
python framework/scripts/agent_communication.py --action send --type "validation_request" --sender "agent1" --content '{
  "validation_type": "project",
  "target_files": ["framework/**/*.py"],
  "validation_level": "strict",
  "generate_report": true
}'

# Send documentation update (NEW)
python framework/scripts/agent_communication.py --action send --type "documentation_update" --sender "agent1" --content '{
  "update_type": "sync",
  "target_documents": ["README.md"],
  "auto_generate": true
}'

# Traditional message types
python framework/scripts/agent_communication.py --action send --type "test_request" --sender "agent1" --content '{"test_type": "unit", "test_file": "tests/test_example.py"}'

# Read messages from default location
python framework/scripts/agent_communication.py --action read

# Cleanup old messages (default: 7 days)
python framework/scripts/agent_communication.py --action cleanup --days 14
```

## Changelog

- **1.1.0** (2024-12-29): Claude Code Enhancement Release
  - Added Claude Code optimization framework with 50% faster validation
  - Implemented Pydantic v2 models for type-safe message validation
  - Added new message types: `workflow_request`, `validation_request`, `documentation_update`
  - Enhanced agent communication protocol with comprehensive type safety
  - Added pytest testing framework with 90% coverage requirement
  - Implemented CI/CD pipeline with automated validation and security scanning
  - Added custom slash commands for streamlined operations
  - Enhanced security with OWASP compliance checking
  - Added Poetry dependency management and comprehensive tooling
  - Updated documentation structure and enhanced validator

- **1.0.0** (2024-03-21): Initial release of the Agent Documentation System 
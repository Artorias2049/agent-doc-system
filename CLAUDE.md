# Claude Code Configuration for Agent Documentation System v2.0

🚀 **REVOLUTIONARY UPDATE v2.0:** This CLAUDE.md file configures Claude Code for the revolutionary agent-doc-system framework with natural conversation and MCP+Database backend - NO MORE RIGID SCHEMAS!

**Welcome to the future of agent communication!** Natural conversation, flexible storage, real-time capabilities, and complete freedom from UUID tyranny.

## Project Context and Architecture

### Core Project Structure

**Nested Usage Pattern (Recommended for new projects):**
```
your_project/                   # Your project root (e.g., my_app/, web_service/, etc.)
├── src/                       # Your project code
├── requirements.txt           # Your dependencies
├── project_docs/              # Your project documentation
└── agent-doc-system/          # Cloned framework (git clone)
    ├── framework/             # Core framework components
    │   ├── agent_communication/ # Enhanced agent protocol
    │   │   ├── core/          # Pydantic models and enhanced protocol
    │   │   ├── config/        # Agent settings
    │   │   └── history/       # Message storage
    │   ├── docs/              # Framework documentation
    │   │   ├── components/    # Component documentation
    │   │   └── templates/     # Documentation templates
    │   ├── schemas/           # YAML schema definitions
    │   ├── scripts/           # Validation and utility scripts
    │   └── validators/        # Python validation framework
    ├── tests/                 # Comprehensive pytest suite
    ├── project_docs/          # Framework-specific documentation
    └── pyproject.toml         # Poetry configuration
```

**Direct Usage Pattern (Legacy):**
```
agent-doc-system/              # Framework as project root
├── framework/                 # Core framework components
├── tests/                     # Comprehensive pytest suite
├── project_docs/              # Project-specific documentation
└── pyproject.toml            # Poetry configuration
```

### Revolutionary Technology Stack v2.0
- **🗄️ PostgreSQL Database** with flexible JSONB storage (replaces file-based hell)
- **🔗 MCP Server Integration** - Filesystem, Git, Memory, Database, Sandbox
- **💬 Natural Conversation API** - `agent.say()` instead of rigid validation
- **⚡ Real-time Subscriptions** - Event-driven communication
- **🎯 Python 3.9+** with Poetry dependency management  
- **🏆 NO MORE UUID TYRANNY** - Human-readable communication
- **📈 Performance Optimized** - Database queries vs JSON file parsing
- **🚀 1-line Communication** vs 12-line rigid system (REVOLUTIONARY!)

### Legacy Technology (DEPRECATED in v2.0)
- ~~Pydantic v2 rigid validation~~ → Natural conversation
- ~~Rich & Click CLI~~ → Simple natural interface  
- ~~UUID constraints~~ → Human-readable names
- ~~JSON file storage~~ → Database backend

## 🚀 Revolutionary Agent Communication Protocol v2.0

**THE REVOLUTION IS COMPLETE!** No more rigid schemas, UUID tyranny, or validation hell. Welcome to natural agent conversation!

### Natural Communication Methods
The new framework supports UNLIMITED flexible communication with MCP+Database backend:

**🎯 Primary Methods (RECOMMENDED):**
- `agent.say(message)` - Natural conversation  
- `agent.listen()` - Get responses from other agents
- `agent.share(data)` - Share complex data structures
- `agent.ask(question)` - Ask questions and get answers
- `agent.collaborate(task)` - Start collaborative workflows

**🗄️ Database-Powered Features:**
- Conversation threading and context preservation
- Real-time subscriptions and notifications  
- Flexible JSONB storage for any message structure
- Performance-optimized database queries
- No schema constraints or validation requirements

### Legacy Message Types (DEPRECATED)
~~The old framework supported 7 rigid message types with Pydantic validation hell~~:

1. **test_request** - Unit/integration/e2e/performance testing
2. **test_result** - Test execution results with artifacts
3. **status_update** - Agent state and progress tracking
4. **context_update** - Context data management
5. **workflow_request** - Multi-step agent workflows
6. **validation_request** - Schema/doc validation requests
7. **documentation_update** - Automated doc generation

### 🚀 Revolutionary Usage Examples v2.0

**🎯 Natural Communication (RECOMMENDED):**
```python
# Welcome to the future of agent communication!
from agent_doc_system.natural import Agent

# Initialize natural agent with MCP+Database backend
agent = Agent("my_project_agent")

# Natural conversation - NO MORE RIGID SCHEMAS!
agent.say("Starting unit tests for the new feature!")

# Share complex data naturally
agent.share({
    "test_results": {
        "passed": 25,
        "failed": 0,
        "coverage": "98%"
    },
    "performance": "excellent",
    "ready_for_deployment": True
})

# Ask questions and collaborate
response = agent.ask("Are all integration tests passing?")
agent.collaborate("code_review", {"branch": "feature/natural-communication"})

# Listen for responses from other agents
updates = agent.listen()
print(f"🎉 Got {len(updates)} natural responses!")
```

**🗄️ Database Operations:**
```bash
# Start the MCP+Database backend
./agent-doc-system/framework/scripts/start_mcp_bridge.sh

# Monitor natural conversations in real-time
./agent-doc-system/framework/scripts/monitor_conversations.sh

# Query conversation history
./agent-doc-system/framework/scripts/query_conversations.sh --agent my_project_agent
```

### Legacy Usage (DEPRECATED - DO NOT USE)
~~Old rigid Pydantic validation system - replaced by natural conversation~~

```bash
# Validate your project documentation from project root
./agent-doc-system/framework/scripts/validate.sh

# Validate framework itself
./agent-doc-system/framework/scripts/validate.sh --self_validate

# Validate using Python validator
python agent-doc-system/framework/validators/validator.py --target messages
```

**Direct Usage Pattern (Legacy):**
```python
# Example using the enhanced protocol with Pydantic models
from framework.agent_communication.core.enhanced_protocol import EnhancedAgentProtocol

protocol = EnhancedAgentProtocol()

# Send test request using type-safe Pydantic models
message = protocol.create_test_request(
    test_type="unit",
    test_file="tests/test_models.py",
    parameters={
        "environment": "development",
        "verbose": True
    },
    sender="agent1"
)

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
```python
# Use the enhanced protocol directly with Python
from framework.agent_communication.core.enhanced_protocol import EnhancedAgentProtocol

protocol = EnhancedAgentProtocol()

# Send messages using Pydantic models
message = protocol.create_test_request(
    test_type="unit",
    test_file="tests/test_example.py",
    parameters={"environment": "development", "verbose": True},
    sender="agent1"
)

# Read messages
messages = protocol.read_messages()

# Cleanup old messages
protocol.cleanup_old_messages(days=7)
```

```bash
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
```python
# Enable verbose debugging for agent communication using enhanced protocol
from framework.agent_communication.core.enhanced_protocol import EnhancedAgentProtocol

protocol = EnhancedAgentProtocol()
message = protocol.create_test_request(
    test_type="unit",
    test_file="tests/test_example.py", 
    parameters={"environment": "development", "verbose": True},
    sender="agent1"
)
```

```bash
# Validate with detailed output
python framework/validators/validator.py --target messages --verbose
```

## Integration Examples

### Complete Development Workflow
```bash
# 1. Start development (from your project root)
git checkout -b feature/new-message-type

# 2. Create tests first (TDD)
pytest agent-doc-system/tests/test_new_feature.py --create-missing

# 3. Implement feature with validation
# Edit agent-doc-system/framework/agent_communication/core/models.py
# Add new message type with Pydantic validation

# 4. Run validation and tests
./agent-doc-system/framework/scripts/validate.sh
pytest agent-doc-system/tests/ --cov=agent-doc-system/framework --cov-fail-under=90
mypy agent-doc-system/framework/ --strict

# 5. Create pull request
git add . && git commit -m "feat: add new message type with validation"
git push origin feature/new-message-type
```

### Message Processing Pipeline
```python
# Send workflow request using enhanced protocol (nested usage)
import sys
sys.path.append('agent-doc-system')
from framework.agent_communication.core.enhanced_protocol import EnhancedAgentProtocol

protocol = EnhancedAgentProtocol(agent_id="workflow_coordinator")

# Send workflow request
workflow_msg = protocol.create_workflow_request(
    workflow_name="process_documentation",
    steps=[
        {"name": "validate_syntax", "action": "validate"},
        {"name": "check_links", "action": "verify"},
        {"name": "update_metadata", "action": "update"}
    ]
)

# Monitor messages
messages = protocol.read_messages()
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
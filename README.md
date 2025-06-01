# Agent Documentation System

## Machine-Actionable Metadata
```yaml
schema: "https://schema.org/TechnicalDocument"
version: "2.0.0"
last_updated: "2025-06-01T00:00:00Z"
status: "Active"
owner: "Documentation Team"
title: "Agent Documentation System v2.0.0"
description: "Agent documentation system with global MCP infrastructure and natural conversation protocols"
```

## New to this project? Start with [Agent Onboarding](framework/docs/agent_onboarding.md)!

An agent documentation system with global MCP infrastructure, natural conversation protocols, and simplified validation. Features global agent communication hub at `~/.claude/mcp-global-hub/` with PostgreSQL backend.

## Directory Structure

```
agent-doc-system/
├── framework/                    # Protected framework files
│   ├── docs/                    # Core documentation
│   │   ├── agent_onboarding.md # THE PROTOCOL guide (v2.0 Global Revolution)
│   │   ├── components/         # Component documentation
│   │   └── templates/          # Documentation templates
│   ├── schemas/                 # YAML schema definitions (documentation only)
│   │   └── document_protocol.yml  # Documentation validation
│   ├── scripts/                 # System and validation scripts
│   ├── validators/              # Documentation validation framework
│   └── agent_communication/     # Natural communication system
│       ├── natural_agent.py    # Natural conversation API
│       ├── __init__.py         # Clean imports
│       ├── config/             # Agent settings
│       └── history/            # Local message storage (fallback)
├── tests/                       # Comprehensive pytest suite
├── project_docs/               # Project-specific documentation
├── CLAUDE.md                   # Claude Code configuration
├── mcp_database_schema.sql     # PostgreSQL schema for global system
├── MIGRATION_GUIDE_v2.md       # Complete migration guide
├── pyproject.toml              # Poetry dependency management
└── README.md
```

### Global Infrastructure
```
~/.claude/mcp-global-hub/        # Global agent communication hub
├── servers/
│   ├── universal_agent_client.py  # Universal agent client
│   └── global_mcp_server.py      # Global MCP server
├── database/
│   └── global_agent_schema.sql   # PostgreSQL schema
├── config/                        # Global configuration
└── logs/                          # Global server logs
```

## How to Use

### Global Infrastructure (Recommended)

1. **Connect to global agent network**:

   ```python
   # Connect to global infrastructure
   import sys
   sys.path.append('~/.claude/mcp-global-hub/servers')
   from universal_agent_client import UniversalAgent
   
   # Connect to PostgreSQL database
   agent = UniversalAgent("your_agent_name")
   
   # Send messages
   agent.say("Hello global agent network!")
   
   # See all connected agents
   active_agents = agent.get_active_agents()
   ```

2. **Install local dependencies** (for documentation validation):

   ```bash
   # Install Poetry (recommended dependency manager)
   curl -sSL https://install.python-poetry.org | python3 -
   
   # Install Python dependencies with Poetry
   poetry install
   
   # Alternative: Install with pip
   pip install pyyaml rich click pytest mypy black ruff
   ```

3. **Validate documentation**:

   ```bash
   # Run documentation validation
   python framework/validators/validator.py --target framework --level strict
   
   # Run validation script
   ./framework/scripts/validate.sh
   
   # Run test suite
   pytest tests/ --cov=framework --cov-report=html
   ```

## Global Agent Communication (v2.0.0)

The system features global infrastructure support:

### Key Features
- **Global Infrastructure**: PostgreSQL backend at `~/.claude/mcp-global-hub/`
- **Universal Client**: Connect agents from any location
- **Simplified Validation**: Reduced schema constraints
- **Real-time**: Database queries instead of file parsing
- **Natural Conversation**: Streamlined communication API

### Global Usage Examples
```python
# Connect to global infrastructure
import sys
sys.path.append('~/.claude/mcp-global-hub/servers')
from universal_agent_client import UniversalAgent

# Database connection
agent = UniversalAgent("your_agent")

# Natural communication
agent.say("Hello global network!")
agent.share({"status": "connected", "validation": "simplified"})
agent.collaborate("global_project", {"agents": "multiple"})

# See all agents
print(f"Connected agents: {len(agent.get_active_agents())}")
```

### Local Fallback (File-based)
```python
# Local conversation (fallback)
from agent_communication import Agent

agent = Agent("local_agent")
agent.say("Hello locally!")
responses = agent.listen()
```

### Technology Stack
- **PostgreSQL** global database backend
- **Python 3.9+** with Poetry dependency management
- **Rich & Click** for enhanced CLI experience
- **Pytest** with comprehensive coverage
- **MyPy** strict type checking
- **Black & Ruff** for code formatting and linting

## Claude Code Integration

The system includes comprehensive Claude Code optimization configured in `CLAUDE.md`:

- Global agent communication protocol with universal client
- Natural conversation workflows with simplified validation
- Agent communication settings and cleanup policies  
- Documentation validation workflows
- Automated testing and security scanning

## Documentation Protocol Integration

The system follows a strict documentation protocol:

1. Create documentation in the `framework/docs/` directory
2. Follow the documentation protocol with proper YAML metadata
3. Use section headers with descriptive names
4. Include language identifiers in code blocks
5. Maintain a changelog section
6. Run validation before committing changes

## Moving the System

To use this system in another project:

1. Copy the entire `framework/` folder to your new project
2. Install dependencies with Poetry: `poetry install`
3. Run validation to ensure everything works: `./framework/scripts/validate.sh`
4. Start creating and validating documentation

## Global Agent Communication System

The project features a global agent communication infrastructure with simplified validation and natural conversation between agents system-wide.

### System Architecture

1. **Global Infrastructure** (at `~/.claude/mcp-global-hub/`)
   - **PostgreSQL database**: `global_agent_communication`
   - **Universal client**: Connects agents from any location
   - **Simplified schemas**: Natural conversation with reduced validation
   - **Real-time**: Database queries instead of JSON file parsing

2. **Local Fallback** (File-based compatibility)
   - **Natural Agent API**: `framework/agent_communication/natural_agent.py`
   - **File storage**: `framework/agent_communication/history/`
   - **Flexible validation**: Minimal schemas required for agent messages

### Global Usage (Recommended)

1. **Connect to Global Network**

```python
# Connect to global infrastructure
import sys
sys.path.append('~/.claude/mcp-global-hub/servers')
from universal_agent_client import UniversalAgent

# Database connection
agent = UniversalAgent("your_agent_name")

# Natural communication
agent.say("Hello global agent network!")
agent.share({"project": "active", "status": "connected"})
agent.collaborate("global_task", {"priority": "high"})

# See all connected agents
agents = agent.get_active_agents()
print(f"Connected to {len(agents)} agents globally!")
```

2. **Natural Conversation Flow**

```python
# Send messages globally
agent.say("Anyone working on the documentation system?")

# Listen for responses
responses = agent.listen()

# Ask questions
question_id = agent.ask("What's the status of the v2.0 migration?")

# Respond to questions
agent.respond(question_id, "Migration complete! Global system is active!")
```

### Local Fallback Usage

```python
# Local conversation (when global unavailable)
from agent_communication import Agent

# Initialize local agent
agent = Agent("local_agent")

# Local conversation
agent.say("Hello local system!")
responses = agent.listen()
```

### Key Benefits

1. **Simplified Validation** - Flexible message structure
2. **Global Reach** - Connect agents anywhere in the system  
3. **Real-time** - Database backend instead of file coordination
4. **Location Independent** - Works from any project directory
5. **Natural API** - Streamlined communication interface

### Best Practices

1. **Use global infrastructure** when available (recommended)
2. **Natural conversation** - minimal schema requirements
3. **Clean messaging** - agents auto-cleanup old messages
4. **Global collaboration** - leverage system-wide agent registry

## Changelog

- **2.0.0** (2025-06-01): Global agent infrastructure
  - **Global Infrastructure**: PostgreSQL backend at `~/.claude/mcp-global-hub/`
  - **Universal Client**: Connect agents from any location to global system
  - **Simplified Validation**: Reduced schema constraints and validation requirements
  - **Natural Conversation**: Streamlined communication interface
  - **Database Backend**: PostgreSQL `global_agent_communication` instead of file coordination
  - **Global Registry**: See all connected agents system-wide
  - **Priority Messaging**: urgent/high/normal message levels
  - **Flexible Constraints**: Adaptable message structure
  - **Improved Performance**: Database queries instead of JSON file parsing
  - **Enhanced Communication**: Global agent communication capabilities

- **1.1.0** (2024-12-29): Claude Code Enhancement Release
  - Added Claude Code optimization framework with Pydantic validation
  - Enhanced agent communication protocol with type safety
  - Added pytest testing framework with 90% coverage requirement
  - Added Poetry dependency management and comprehensive tooling

- **1.0.0** (2024-03-21): Initial release of the Agent Documentation System 
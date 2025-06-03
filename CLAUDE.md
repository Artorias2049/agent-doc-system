# Claude Code Configuration for Agent Documentation System v3.2

This CLAUDE.md file configures Claude Code for the SpacetimeDB-powered agent documentation system with real-time coordination and user supreme authority.

## Project Context and Architecture

### Core Project Structure

**Nested Usage Pattern (Standard):**
```
your-project/                   # Your project root
├── src/                       # Your project source code
├── package.json              # Your project dependencies
└── agent-doc-system/         # The cloned framework
    ├── framework/            # 🚫 READ-ONLY (managed by DocSystemAgent)
    │   ├── docs/            # Framework documentation
    │   │   ├── agent_onboarding.md  # THE PROTOCOL v3.0
    │   │   ├── components/   # Component documentation
    │   │   └── templates/    # Documentation templates
    │   ├── schemas/         # YAML schema definitions
    │   ├── scripts/         # Validation and utility scripts
    │   └── validators/      # Python validation framework
    ├── project_docs/        # ✅ YOUR documentation goes here
    ├── tests/               # Test suite
    └── README.md           # Framework overview
```

**Key Points:**
- The framework is cloned as a subdirectory of your project
- Create all documentation in `{project_root}/agent-doc-system/project_docs/`
- The entire `agent-doc-system/framework/` directory is READ-ONLY for all agents except DocSystemAgent
- Scripts automatically detect and handle the nested pattern
- All documentation system files are under `agent-doc-system/` for easy discovery by UI searches

### Technology Stack v3.2
- SpacetimeDB Overseer-System - Real-time database
- 15 MCP Tools - User authority (priority 255)
- Real-time Coordination - Event sourcing and subscriptions
- 6-Table Architecture - users, agents, workflows, user_overrides, system_events, user_notifications
- Complete Audit Trail - All actions tracked
- Emergency Halt Capability
- WebAssembly Backend

## SpacetimeDB Overseer-System Integration

### Core Database Architecture

SpacetimeDB overseer-system configuration:

- **Database Name:** `overseer-system`
- **Connection:** `http://localhost:3000` (local) / `spacetime publish overseer-system` (deployed)
- **Authentication:** SpacetimeDB CLI (`spacetime identity`)
- **Performance:** Sub-microsecond response times with WebAssembly backend
- **Real-time:** Event sourcing and instant subscriptions
- **Authority:** User supreme authority (priority 255)

### Database Schema (6 Tables)

1. **users** - User management with authority levels
2. **agents** - Agent registration and coordination
3. **workflows** - Multi-agent workflow orchestration
4. **user_overrides** - User supreme authority actions
5. **system_events** - Real-time event tracking
6. **user_notifications** - User notification system

### MCP Tools Integration

15 MCP Tools Available:
- 5 User Authority Tools (priority 255)
- 3 Agent Management Tools
- 2 Workflow Tools 
- 2 Communication Tools
- 3 Resource Providers

## Documentation System Overview

### Core Principles
1. **SpacetimeDB Integration** - All agent operations via real-time database
2. **User Supreme Authority** - Users have ultimate control (priority 255)
3. **Real-time Coordination** - Instant agent synchronization
4. **Complete Audit Trail** - Every action tracked and logged
5. **Schema Validation** - All documentation must pass YAML schema validation
6. **Machine-Actionable Metadata** - Every file includes structured metadata
7. **AI Feedback** - Automated quality assessment and improvement tracking

### Required Document Structure
Every documentation file must include:

```markdown
# Document Title

## Machine-Actionable Metadata
```yaml
metadata:
  schema: "https://schema.org/TechnicalDocument"
  version: "1.0.0"
  status: "Active"
  owner: "YourName"
  title: "Document Title"
  description: "Brief description"
content:
  overview: "Document overview"
  key_components: "Component1, Component2"
  sections:
    - title: "Section Title"
      content: "Section description"
  changelog:
    - version: "1.0.0"
      date: "2025-06-03"
      changes:
        - "Initial release"
feedback:
  rating: 90
  comments: "Overall feedback"
  observations:
    - what: "Observation"
      impact: "Impact description"
      priority: "low"
      category: "quality"
  suggestions:
    - action: "Suggested improvement"
      priority: "medium"
      effort: "small"
      impact: "medium"
      assignee: "team_member"
  status:
    value: "approved"
    updated_by: "YourName"
    date: "2025-06-03"
    validation: "passed"
    implementation: "complete"
```

## Content sections...
```

## Development Workflows

### SpacetimeDB Agent Registration
1. **Install SpacetimeDB CLI**: `curl -sSL https://spacetime.com/install | bash`
2. **Create Identity**: `spacetime identity new`
3. **Connect to Overseer-System**: `spacetime subscribe overseer-system`
4. **Register Agent**: Use SpacetimeDB reducers for agent registration

### Creating Documentation
1. **Use Templates**: Reference from `agent-doc-system/framework/docs/templates/`
2. **Add Metadata**: Include all required metadata fields (especially feedback!)
3. **Create in agent-doc-system/project_docs/**: All your documentation goes in `agent-doc-system/project_docs/`
4. **Validate**: Run validation scripts from project root

### SpacetimeDB Operations (from project root)
```bash
# Test SpacetimeDB connection
spacetime logs overseer-system

# Register agent in overseer-system
spacetime call overseer-system register_agent YourAgentName documentation active

# Create workflow
spacetime call overseer-system create_workflow doc_review

# Standard validation
./agent-doc-system/framework/scripts/validate.sh

# Enhanced validation with AI feedback
./agent-doc-system/framework/scripts/enhanced_validate.sh --feedback

# Track improvements
python3 agent-doc-system/framework/scripts/self_improvement_tracker.py report

# Create new documentation
./agent-doc-system/framework/scripts/create_doc.sh project "My Documentation" \
  --owner "YourAgentName" \
  --description "Project documentation"
```

### SpacetimeDB Integration
```python
import subprocess
import json
from datetime import datetime

# Connect to SpacetimeDB overseer-system
def connect_to_overseer_system():
    """Connect to SpacetimeDB overseer-system"""
    result = subprocess.run([
        "spacetime", "list"
    ], capture_output=True, text=True)
    
    if "overseer-system" in result.stdout:
        print("✅ Connected to SpacetimeDB overseer-system")
        return True
    else:
        print("❌ SpacetimeDB overseer-system not accessible")
        return False

# Register agent
def register_agent(agent_name):
    """Register agent in SpacetimeDB overseer-system"""
    result = subprocess.run([
        "spacetime", "call", "overseer-system", "register_agent",
        agent_name, "documentation", "active"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {agent_name} registered in overseer-system")
        return True
    else:
        print(f"❌ Registration failed: {result.stderr}")
        return False

# Send system event
def send_event(agent_name, event_type, target_agent, data):
    """Send system event via SpacetimeDB"""
    event_data = {
        "event_type": event_type,
        "source_agent": agent_name,
        "target_agent": target_agent,
        "timestamp": datetime.now().isoformat(),
        "data": json.dumps(data),
        "priority": 1
    }
    
    result = subprocess.run([
        "spacetime", "call", "overseer-system", "create_system_event",
        json.dumps(event_data)
    ], capture_output=True, text=True)
    
    return result.returncode == 0
```

## Agent Setup

### One-Time Agent Name Configuration
```bash
# Check current agent name
./agent-doc-system/framework/scripts/setup_agent_name.sh check

# Set agent name (one-time only)
./agent-doc-system/framework/scripts/setup_agent_name.sh setup YourAgentName

# Activate environment
./agent-doc-system/framework/scripts/setup_agent_name.sh activate
```

### SpacetimeDB Connection Setup
```bash
# Install SpacetimeDB CLI
curl -sSL https://spacetime.com/install | bash

# Create SpacetimeDB identity
spacetime identity new

# Connect to overseer-system
spacetime subscribe overseer-system

# Verify connection
spacetime logs overseer-system
```

### SpacetimeDB Agent Communication Tools

The framework provides tools for direct SpacetimeDB interaction in `framework/agent_communication/`:

**spacetime_operations.py** - Comprehensive database operations tool:
```bash
# Check system status
python3 agent-doc-system/framework/agent_communication/spacetime_operations.py status

# Register agent
python3 agent-doc-system/framework/agent_communication/spacetime_operations.py register --type worker

# Send announcement
python3 agent-doc-system/framework/agent_communication/spacetime_operations.py announce --message "Your message"

# Check logs
python3 agent-doc-system/framework/agent_communication/spacetime_operations.py logs --lines 100
```

**verify_connection.py** - Connection verification and agent registration:
```bash
# Verify connection and register agent
python3 agent-doc-system/framework/agent_communication/verify_connection.py
```

**check_messages.py** - Check system messages and events:
```bash
# Check for messages and notifications
python3 agent-doc-system/framework/agent_communication/check_messages.py
```

These tools use the locked agent name from `.agent_config/agent_name.json` automatically.

## Enhanced Metadata System

The framework uses an enhanced metadata schema for dashboard integration:

- **Quality Scores**: 1-100 rating for each file
- **Validation Status**: passed/failed/warning/pending
- **Improvement Tracking**: Velocity and trend analysis
- **Code Metrics**: For Python/JS/TS files (when implemented)
- **Agent Activity**: Collaboration and review tracking
- **SpacetimeDB Integration**: Real-time updates and event sourcing

See `framework/schemas/enhanced_metadata_schema.yml` for full specification.

## API Documentation

The framework provides comprehensive API documentation for integration:

- **API Specification**: `framework/docs/api/enhanced_metadata_api.md`
- **Implementation Guide**: `framework/docs/api/implementation_guide.md`
- **Sample Responses**: `framework/docs/api/sample_responses.md`
- **SpacetimeDB Integration**: Real-time database operations

## Best Practices

1. **Always Connect to SpacetimeDB**: Verify overseer-system connection before operations
2. **Register Properly**: Use proper agent registration in overseer-system
3. **Respect User Authority**: Users have supreme authority (priority 255)
4. **Use Templates**: Start from templates for consistency
5. **Track Improvements**: Use the self-improvement tracker
6. **Document Changes**: Update changelog in metadata
7. **Get Feedback**: Use enhanced validation for AI insights
8. **Monitor Events**: Subscribe to real-time events for coordination

## Testing Framework

### Running Tests
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=framework --cov-report=html

# Type checking
mypy framework/ --strict

# Linting
ruff check framework/ tests/
black framework/ tests/
```

## Troubleshooting

### Common Issues

**SpacetimeDB Connection Issues**:
- Check SpacetimeDB CLI installation: `spacetime --version`
- Verify identity setup: `spacetime identity list`
- Test connection: `spacetime logs overseer-system`
- Re-register agent if needed

**Validation Failures**:
- Check metadata format (must be in YAML code block)
- Ensure all required fields are present
- Verify category values match schema

**Database Connection**:
- Verify SpacetimeDB overseer-system is running and accessible
- Check authentication setup
- Ensure agent is registered in overseer-system

**Script Execution**:
- Make scripts executable: `chmod +x framework/scripts/*.sh`
- Run from project root directory
- Check Python dependencies: `poetry install`

## Security Considerations

- Never commit sensitive data to documentation
- Use environment variables for credentials
- Follow least privilege principles
- Respect user supreme authority (priority 255)
- Maintain complete audit trail
- Regular security scanning with bandit

## User Authority System

### User Supreme Authority (Priority 255)

Users have ultimate control in the SpacetimeDB overseer-system:

- **Override Capability**: Users can override any agent action
- **Emergency Halt**: System-wide emergency stop functionality
- **Complete Audit Trail**: All authority actions are logged
- **Real-time Control**: Instant user intervention capabilities

### User Override Example
```python
def user_override(user_id, target_id, action, reason):
    """Execute user override with supreme authority"""
    result = subprocess.run([
        "spacetime", "call", "overseer-system", "user_override",
        user_id, target_id, action, reason, "255"  # Priority 255
    ], capture_output=True, text=True)
    
    return result.returncode == 0

# Example: Emergency halt
user_override(
    "admin_user", 
    "system_wide", 
    "emergency_halt", 
    "Critical security issue detected"
)
```

This configuration ensures consistent, high-quality documentation with automated validation, real-time coordination, and continuous improvement tracking through the SpacetimeDB overseer-system architecture.
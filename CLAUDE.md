# Claude Code Configuration for Agent Documentation System

This CLAUDE.md file configures Claude Code for the agent-doc-system framework - a structured documentation system with schema validation, AI feedback integration, and quality tracking.

## Project Context and Architecture

### Core Project Structure

**Direct Usage Pattern (Recommended):**
```
agent-doc-system/              # Project root
├── framework/                 # Core framework components
│   ├── agent_communication/   # Agent feedback and tracking
│   │   ├── feedback_agent.py  # AI documentation analysis
│   │   ├── config/           # Configuration settings
│   │   └── history/          # Improvement tracking storage
│   ├── docs/                 # Framework documentation
│   │   ├── agent_onboarding.md  # THE PROTOCOL - single source of truth
│   │   ├── documentation_protocol.md
│   │   ├── api/              # API specifications
│   │   ├── components/       # Component documentation
│   │   └── templates/        # Documentation templates
│   ├── schemas/              # YAML schema definitions
│   │   ├── document_protocol.yml
│   │   ├── enhanced_metadata_schema.yml
│   │   └── sample_enhanced_metadata.yml
│   ├── scripts/              # Validation and utility scripts
│   │   ├── validate.sh       # Standard validation
│   │   ├── enhanced_validate.sh  # Validation with AI feedback
│   │   ├── self_improvement_tracker.py
│   │   └── setup_agent_name.sh
│   └── validators/           # Python validation framework
│       └── validator.py
├── tests/                    # Test suite
├── README.md                 # Project overview
└── pyproject.toml           # Poetry configuration
```

### Technology Stack
- **Python 3.9+** with Poetry dependency management
- **YAML** for schema definitions and metadata
- **SQLite Database** at `~/.claude/mcp-global-hub/database/agent_communication.db`
- **Structured Documentation** with strict schema validation
- **AI Feedback Integration** for quality assessment
- **Git Integration** for version control

## Documentation System Overview

### Core Principles
1. **Schema Validation** - All documentation must pass YAML schema validation
2. **Machine-Actionable Metadata** - Every file includes structured metadata
3. **AI Feedback** - Automated quality assessment and improvement tracking
4. **Single Source of Truth** - THE PROTOCOL in agent_onboarding.md

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

### Creating Documentation
1. **Use Templates**: Copy from `framework/docs/templates/`
2. **Add Metadata**: Include all required metadata fields
3. **Validate**: Run `./framework/scripts/validate.sh`
4. **Get AI Feedback**: Run `./framework/scripts/enhanced_validate.sh --feedback`

### Validation Commands
```bash
# Standard validation
./framework/scripts/validate.sh

# Validate framework documentation
./framework/scripts/validate.sh --self_validate

# Enhanced validation with AI feedback
./framework/scripts/enhanced_validate.sh --feedback

# Track improvements
python3 framework/scripts/self_improvement_tracker.py report
```

### Database Operations
```python
import sqlite3
import os

# Connect to centralized database
DB_PATH = os.path.expanduser("~/.claude/mcp-global-hub/database/agent_communication.db")
conn = sqlite3.connect(DB_PATH)

# Register agent
def register_agent(agent_name, project_directory):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO agent_sessions 
        (agent_name, project_directory, session_token, status)
        VALUES (?, ?, ?, 'active')
    """, (agent_name, project_directory, f"{agent_name}_token"))
    conn.commit()
```

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

## Agent Setup

### One-Time Agent Name Configuration
```bash
# Check current agent name
./framework/scripts/setup_agent_name.sh check

# Set agent name (one-time only)
./framework/scripts/setup_agent_name.sh setup YourAgentName

# Activate environment
./framework/scripts/setup_agent_name.sh activate
```

## Enhanced Metadata System

The framework uses an enhanced metadata schema for dashboard integration:

- **Quality Scores**: 1-100 rating for each file
- **Validation Status**: passed/failed/warning/pending
- **Improvement Tracking**: Velocity and trend analysis
- **Code Metrics**: For Python/JS/TS files (when implemented)
- **Agent Activity**: Collaboration and review tracking

See `framework/schemas/enhanced_metadata_schema.yml` for full specification.

## API Documentation

The framework provides comprehensive API documentation for integration:

- **API Specification**: `framework/docs/api/enhanced_metadata_api.md`
- **Implementation Guide**: `framework/docs/api/implementation_guide.md`
- **Sample Responses**: `framework/docs/api/sample_responses.md`

## Best Practices

1. **Always Validate**: Run validation before committing changes
2. **Use Templates**: Start from templates for consistency
3. **Track Improvements**: Use the self-improvement tracker
4. **Document Changes**: Update changelog in metadata
5. **Get Feedback**: Use enhanced validation for AI insights

## Troubleshooting

### Common Issues

**Validation Failures**:
- Check metadata format (must be in YAML code block)
- Ensure all required fields are present
- Verify category values match schema

**Database Connection**:
- Verify database exists at `~/.claude/mcp-global-hub/database/agent_communication.db`
- Check file permissions
- Ensure SQLite is installed

**Script Execution**:
- Make scripts executable: `chmod +x framework/scripts/*.sh`
- Run from project root directory
- Check Python dependencies: `poetry install`

## Security Considerations

- Never commit sensitive data to documentation
- Use environment variables for credentials
- Follow least privilege principles
- Regular security scanning with bandit

This configuration ensures consistent, high-quality documentation with automated validation and continuous improvement tracking.
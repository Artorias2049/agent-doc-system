# Agent Naming System v1.0

## Machine-Actionable Metadata
```yaml
metadata:
  schema: "https://schema.org/TechnicalDocument"
  version: "1.0.0"
  status: "Active"
  owner: "Documentation Team"
  title: "Agent Naming System - Project-Locked Agent Names"
  description: "Flexible but locked agent naming system with environment variable integration and project directory binding"
content:
  overview: "A secure agent naming system that allows flexible agent names while ensuring one-time locking and project directory binding for clear agent identification"
  key_components: "Setup Scripts, Environment Integration, Project Binding, Universal Client Integration"
  sections:
    - title: "Overview"
      content: "Flexible but locked agent naming system with project directory binding"
    - title: "Setup Process"
      content: "One-time agent name configuration with locking mechanism"
    - title: "Integration"
      content: "Environment variables and universal client integration"
    - title: "Security"
      content: "Project directory binding and name collision prevention"
  changelog:
    - version: "1.0.0"
      date: "2025-06-01"
      changes:
        - "Initial implementation of project-locked agent naming system"
        - "Environment variable integration with AGENT_NAME"
        - "Enhanced universal client with naming validation"
        - "Project directory binding enforcement"
feedback:
  rating: 5
  comments: "Excellent solution for agent identification and project binding"
  observations:
    - what: "Clear separation between flexible naming and security"
      impact: "Allows creativity while maintaining system integrity"
    - what: "One-time setup with permanent locking"
      impact: "Prevents accidental name changes and conflicts"
  suggestions:
    - action: "Consider name reservation system for large deployments"
      priority: "Low"
  status:
    value: "Implemented"
    updated_by: "Development Team"
    date: "2025-06-01"
    validation: "Passed"
    implementation: "Complete"
```

## Overview

The Agent Naming System provides a **flexible but locked** approach to agent identification that solves the core requirements:

1. **🎯 Clear Agent Identification**: Know exactly which agent sent what message
2. **🔒 One-Time Locking**: Agents choose their name once, cannot overwrite
3. **📁 Project Directory Binding**: One agent per project directory
4. **🌍 Environment Integration**: Uses AGENT_NAME environment variable
5. **🔗 Universal Client Integration**: Works seamlessly with global communication

## Key Features

### 🚀 Flexible Agent Names
- **Creative Freedom**: Agents can choose meaningful, descriptive names
- **Format Validation**: Alphanumeric characters, underscores, and hyphens allowed
- **Length Limits**: 3-50 characters for optimal identification
- **Examples**: `MyProjectAgent`, `WebService_Monitor`, `DataProcessor-v2`

### 🔒 Locking Mechanism
- **One-Time Setup**: Agent name set once and permanently locked
- **Configuration File**: Stored in `.agent_config/agent_name.json`
- **Environment Variable**: `AGENT_NAME` for easy access
- **Timestamp Tracking**: Records when agent was configured

### 📁 Project Directory Binding
- **One Agent Per Project**: Each project directory has exactly one agent
- **Directory Validation**: Agent name tied to specific project path
- **Collision Prevention**: Cannot create conflicting agents in same directory
- **Clear Identification**: Agent ID format: `AgentName@ProjectDirectory`

## Setup Process

### 1. Initial Setup

```bash
# Set agent name for your project (one-time only)
python framework/scripts/setup_agent_name.py "MyProjectAgent"

# Or use the convenient wrapper
./framework/scripts/setup_agent_name.sh setup MyProjectAgent
```

### 2. Environment Activation

```bash
# Activate agent environment variables
source .agent_config/agent_env.sh

# Or use the wrapper
./framework/scripts/setup_agent_name.sh activate
```

### 3. Verification

```bash
# Check current agent configuration
python framework/scripts/setup_agent_name.py --status

# Or use the wrapper
./framework/scripts/setup_agent_name.sh status
```

## File Structure

```
your_project/
├── .agent_config/              # Agent configuration directory
│   ├── agent_name.json        # Locked agent configuration
│   └── agent_env.sh           # Environment variables
├── agent-doc-system/          # Framework (if using nested pattern)
│   └── framework/
│       └── scripts/
│           ├── setup_agent_name.py     # Python setup script
│           ├── setup_agent_name.sh     # Bash wrapper
│           └── enhanced_universal_agent.py  # Enhanced client
└── src/                       # Your project code
```

## Integration with Universal Client

### Enhanced Universal Agent

The `enhanced_universal_agent.py` provides seamless integration:

```python
from framework.scripts.enhanced_universal_agent import create_agent

# Auto-detect agent name from configuration
agent = create_agent()

# Validate against existing configuration
agent = create_agent("MyProjectAgent")

# Use natural communication
agent.say("Hello from project-locked agent!")
responses = agent.listen()
```

### Error Handling

The system provides clear error messages for common issues:

```python
# No agent configured
🚨 No agent name configured!
Please run: python framework/scripts/setup_agent_name.py "YourAgentName"

# Name mismatch
🚨 Cannot override locked agent name!
Provided: DifferentAgent
Locked name: MyProjectAgent

# Project mismatch
🚨 Agent configured for different project!
Current project: /path/to/current
Configured for: /path/to/other
```

## Security Features

### 1. Project Directory Binding
- Agent configuration includes absolute project path
- Validation ensures agent only works in configured directory
- Prevents accidental cross-project usage

### 2. Name Locking
- Configuration file includes lock timestamp
- Cannot overwrite without explicit `--force` flag
- Environment variable consistency checking

### 3. Validation Chain
```
User Input → Name Validation → Project Binding → Environment Check → Client Creation
```

## Environment Variables

The system sets the following environment variables:

```bash
export AGENT_NAME="MyProjectAgent"
export AGENT_PROJECT_DIR="/absolute/path/to/project"
export AGENT_LOCKED="true"
```

## Configuration File Format

`.agent_config/agent_name.json`:
```json
{
  "agent_name": "MyProjectAgent",
  "project_directory": "/absolute/path/to/project",
  "locked_at": "2025-06-01T22:17:36.322440",
  "locked": true,
  "version": "1.0"
}
```

## Command Reference

### Python Script Commands

```bash
# Setup agent name
python framework/scripts/setup_agent_name.py "AgentName"

# Check current configuration
python framework/scripts/setup_agent_name.py --check

# Detailed status
python framework/scripts/setup_agent_name.py --status

# Force override (use with caution)
python framework/scripts/setup_agent_name.py --force "NewName"
```

### Bash Wrapper Commands

```bash
# Setup
./framework/scripts/setup_agent_name.sh setup AgentName

# Check
./framework/scripts/setup_agent_name.sh check

# Status
./framework/scripts/setup_agent_name.sh status

# Activate environment
./framework/scripts/setup_agent_name.sh activate
```

### Enhanced Client Commands

```bash
# Test connectivity
python framework/scripts/enhanced_universal_agent.py --test

# Show status
python framework/scripts/enhanced_universal_agent.py --status

# Use specific name (validates against config)
python framework/scripts/enhanced_universal_agent.py --name MyAgent
```

## Best Practices

### 1. Agent Naming
- **Descriptive**: Use names that clearly identify the agent's purpose
- **Project-Specific**: Include project name or component identifier
- **Consistent**: Follow naming conventions within your organization
- **Examples**: `WebApp_Frontend`, `DataPipeline_Monitor`, `APIGateway_Auth`

### 2. Project Setup
- **One Agent Per Project**: Each project should have exactly one agent
- **Early Setup**: Configure agent name early in project setup
- **Documentation**: Include agent name in project documentation
- **Environment**: Always source environment file before using agent

### 3. Integration
- **Use Enhanced Client**: Always use the enhanced universal agent client
- **Error Handling**: Handle naming errors gracefully in your code
- **Status Checking**: Verify agent configuration in CI/CD pipelines
- **Backup Configuration**: Include `.agent_config/` in version control (optional)

## Troubleshooting

### Common Issues

1. **Agent Not Configured**
   ```
   🚨 No agent name configured!
   ```
   **Solution**: Run setup script to configure agent name

2. **Name Mismatch**
   ```
   🚨 Agent name mismatch!
   ```
   **Solution**: Source environment file or use configured name

3. **Project Mismatch**
   ```
   🚨 Agent configured for different project!
   ```
   **Solution**: Setup agent for current project or switch to correct project

4. **Environment Not Loaded**
   ```
   AGENT_NAME not set
   ```
   **Solution**: Run `source .agent_config/agent_env.sh`

### Debugging Commands

```bash
# Check environment
echo $AGENT_NAME
echo $AGENT_PROJECT_DIR

# Validate configuration
cat .agent_config/agent_name.json

# Test agent client
python framework/scripts/enhanced_universal_agent.py --status
```

## Future Enhancements

### Potential Features
- **Name Reservation System**: Reserve names across multiple projects
- **Team Management**: Shared agent configurations for teams
- **Migration Tools**: Move agent configurations between projects
- **Audit Logging**: Track agent name usage and changes
- **Integration APIs**: REST API for agent name management

### Database Integration
When database schema updates are ready:
- **Global Name Registry**: System-wide agent name tracking
- **Conflict Detection**: Prevent duplicate names across all projects
- **Usage Analytics**: Track agent activity and communication patterns
- **Performance Metrics**: Monitor agent communication efficiency

## Changelog

- **1.0.0** (2025-06-01): Initial implementation of project-locked agent naming system with environment integration and universal client enhancement
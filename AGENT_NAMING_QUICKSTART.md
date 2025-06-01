# 🤖 Agent Naming System - Quick Start

## 30-Second Setup

```bash
# 1. Set your agent name (one-time only)
python framework/scripts/setup_agent_name.py "MyProjectAgent"

# 2. Activate environment
source .agent_config/agent_env.sh

# 3. Test your agent
python framework/scripts/enhanced_universal_agent.py --test
```

## ✅ Done! Your agent is now project-locked and ready to communicate globally.

---

## Key Benefits

- 🎯 **Clear Identification**: Know exactly which agent sent what message
- 🔒 **One-Time Setup**: Choose name once, locked forever  
- 📁 **Project Binding**: One agent per project directory
- 🌍 **Global Communication**: Works with universal client system
- 🚫 **No Conflicts**: Cannot overwrite or create duplicate agents

## Common Commands

```bash
# Check current agent
./framework/scripts/setup_agent_name.sh check

# Show detailed status  
./framework/scripts/setup_agent_name.sh status

# Activate environment
./framework/scripts/setup_agent_name.sh activate

# Test connectivity
python framework/scripts/enhanced_universal_agent.py --test
```

## Usage in Code

```python
from framework.scripts.enhanced_universal_agent import create_agent

# Auto-detect configured agent name
agent = create_agent()

# Send global messages
agent.say("Hello from my project-locked agent!")

# Listen for responses
responses = agent.listen()

# Get agent info
status = agent.status()
print(f"Agent ID: {status['agent_id']}")
```

## 🔒 Security Features

- **Project-locked**: Agent only works in configured project directory
- **Name validation**: Cannot overwrite existing locked names
- **Environment integration**: Uses AGENT_NAME environment variable
- **Error handling**: Clear messages for configuration issues

## Files Created

```
your_project/
├── .agent_config/
│   ├── agent_name.json    # Locked configuration
│   └── agent_env.sh       # Environment variables
```

**Note**: Add `.agent_config/` to version control if you want to share agent configuration with your team.

---

📖 **Full Documentation**: [Agent Naming System](framework/docs/agent_naming_system.md)
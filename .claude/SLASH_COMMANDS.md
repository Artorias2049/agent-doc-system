# Claude Code Slash Commands Integration

This document describes how to use the implemented slash commands with Claude Code.

## Available Commands

### Agent Commands
- `/agent:send <type> <content>` - Send agent messages
- `/agent:read [options]` - Read agent messages
- `/agent:validate [target]` - Validate agent messages
- `/agent:workflow <name> [params]` - Execute workflows
- `/agent:audit <component>` - Audit components

### Chat Commands  
- `/chat:export [options]` - Export current chat session
- `/chat:history <action> [options]` - Manage chat history
- `/chat:config <action>` - Configure chat settings

### Help
- `/help` - Show all available commands

## Usage Examples

### Export Current Chat
```bash
python3 .claude/scripts/slash_command_handler.py "/chat:export --format markdown"
```

### Send Agent Message
```bash  
python3 .claude/scripts/slash_command_handler.py '/agent:send test_request {"test_type": "unit"}'
```

### List Chat History
```bash
python3 .claude/scripts/slash_command_handler.py "/chat:history list --limit 10"
```

## Integration Methods

### Method 1: Direct Python Execution
```bash
python3 .claude/scripts/slash_command_handler.py "/command:subcommand [args]"
```

### Method 2: Using Aliases
```bash
# Source the aliases
source .claude/scripts/claude_aliases.sh

# Use aliases
claude_cmd "/chat:export"
agent-send test_request '{"test_type": "unit"}'
chat-export --format json
```

### Method 3: Command Wrapper
```bash
.claude/scripts/claude_command_wrapper.sh "/chat:export --format markdown"
```

## Testing

Run the test script to verify all commands work:
```bash
.claude/scripts/test_slash_commands.sh
```

## Configuration

Command routing is configured in `.claude/config/command_routing.json`.
Edit this file to add new commands or modify existing ones.

## Troubleshooting

1. **Permission Issues**: Ensure scripts are executable
   ```bash
   chmod +x .claude/scripts/*.py .claude/scripts/*.sh
   ```

2. **Python Path Issues**: Make sure the project root is in your Python path
   
3. **Missing Dependencies**: Install required packages
   ```bash
   pip install click rich
   ```

4. **Command Not Found**: Verify the command exists in the routing configuration
   ```bash
   python3 .claude/core/command_router.py list-commands
   ```

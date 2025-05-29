# Claude Code Slash Commands - Usage Guide

## 🎉 Slash Commands Are Now Working!

The slash command integration is now fully functional. You can use commands like `/agent:send` and `/chat:export` directly!

## Available Commands

### Agent Commands

#### Send Agent Messages
```bash
python3 .claude/scripts/slash_command_handler.py '/agent:send --type test_request --content "{\"test_type\": \"unit\", \"test_file\": \"tests/test_example.py\", \"parameters\": {\"environment\": \"development\", \"verbose\": true}}"'
```

#### Read Agent Messages  
```bash
python3 .claude/scripts/slash_command_handler.py "/agent:read"
```

#### Validate Messages
```bash
python3 .claude/scripts/slash_command_handler.py "/agent:validate"
```

#### Cleanup Old Messages
```bash
python3 .claude/scripts/slash_command_handler.py "/agent:cleanup"
```

### Chat Commands

#### Export Current Chat Session
```bash
python3 .claude/scripts/slash_command_handler.py "/chat:export"
```

#### Browse Chat History
```bash
python3 .claude/scripts/slash_command_handler.py "/chat:history"
```

#### List Available Commands
```bash
python3 .claude/scripts/slash_command_handler.py "/help"
```

## Quick Setup

### Method 1: Direct Command Execution
Use the slash command handler directly:
```bash
python3 .claude/scripts/slash_command_handler.py "/command:subcommand [args]"
```

### Method 2: Enable Aliases
```bash
# Enable convenient aliases
source .claude/scripts/claude_aliases.sh

# Now you can use:
claude_cmd "/agent:send --type test_request --content '{...}'"
agent-read
chat-export
```

### Method 3: Test All Commands
```bash
# Run the test script to verify everything works
.claude/scripts/test_slash_commands.sh
```

## Command Examples

### Send Different Message Types

**Test Request:**
```bash
python3 .claude/scripts/slash_command_handler.py '/agent:send --type test_request --content "{\"test_type\": \"unit\", \"test_file\": \"tests/test_models.py\", \"parameters\": {\"environment\": \"development\", \"verbose\": true}}"'
```

**Status Update:**
```bash
python3 .claude/scripts/slash_command_handler.py '/agent:send --type status_update --content "{\"agent_id\": \"agent1\", \"state\": \"busy\", \"progress\": 75.5, \"current_task\": \"Running tests\"}"'
```

**Workflow Request:**
```bash
python3 .claude/scripts/slash_command_handler.py '/agent:send --type workflow_request --content "{\"workflow_name\": \"validate_and_test\", \"steps\": [{\"name\": \"validate\", \"action\": \"check\", \"parameters\": {}}], \"parameters\": {\"target\": \"framework\"}}"'
```

### Chat Management

**Export with Options:**
```bash
python3 .claude/scripts/slash_command_handler.py "/chat:export --output my_session.md"
```

**View Specific Session:**
```bash
python3 .claude/scripts/slash_command_handler.py "/chat:history --limit 5"
```

## Integration Notes

### File Locations
- **Command Router**: `.claude/core/command_router.py`
- **Slash Handler**: `.claude/scripts/slash_command_handler.py` 
- **Configuration**: `.claude/config/command_routing.json`
- **Aliases**: `.claude/scripts/claude_aliases.sh`

### Configuration
Commands are configured in `.claude/config/command_routing.json`. You can add new commands or modify existing ones by editing this file.

### Error Handling
- Invalid commands show available options
- JSON parsing errors are caught and reported
- Missing dependencies are detected and reported

## Troubleshooting

### Common Issues

1. **JSON Parsing Errors**
   - Ensure JSON is properly escaped: `\"`
   - Use single quotes around the entire command
   - Check for missing commas or brackets

2. **Command Not Found**
   - Run `/help` to see available commands
   - Check `.claude/config/command_routing.json` for command definitions

3. **Permission Errors**
   - Make sure scripts are executable: `chmod +x .claude/scripts/*.py`

4. **Import Errors**
   - Install dependencies: `pip install pydantic rich click`
   - Check Python path configuration

### Debug Mode
Set `export CLAUDE_DEBUG=1` for verbose logging.

## Next Steps

1. **Add More Commands**: Edit `.claude/config/command_routing.json`
2. **Create Workflows**: Use workflow_request messages for complex operations
3. **Automate**: Use aliases and scripts for common tasks
4. **Integrate**: Add to your development workflow

## Success! 🎉

The slash command system is now fully functional and ready for use. You can now use commands like `/agent:send` and `/chat:export` directly in your Claude Code workflow!
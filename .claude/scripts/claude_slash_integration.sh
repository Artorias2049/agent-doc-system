#!/bin/bash
"""
Claude Code Slash Command Integration
Creates command aliases and integration for Claude Code slash commands.
"""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CLAUDE_DIR="$PROJECT_ROOT/.claude"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Setting up Claude Code slash command integration...${NC}"

# Make scripts executable
chmod +x "$CLAUDE_DIR/scripts/slash_command_handler.py"
chmod +x "$CLAUDE_DIR/scripts/chat_logger.py"
chmod +x "$CLAUDE_DIR/core/command_router.py"

# Create command wrapper function
create_command_wrapper() {
    local wrapper_path="$CLAUDE_DIR/scripts/claude_command_wrapper.sh"
    
    cat > "$wrapper_path" << 'EOF'
#!/bin/bash
# Claude Code Command Wrapper
# Handles slash commands by routing them through our command router

# Check if command starts with /
if [[ "$1" == /* ]]; then
    # Route through our slash command handler
    exec python3 "$(dirname "$0")/slash_command_handler.py" "$@"
else
    echo "Error: Commands must start with /"
    echo "Usage: $0 '/command:subcommand [args...]'"
    echo ""
    echo "Available commands:"
    echo "  /agent:send - Send agent messages"
    echo "  /agent:read - Read agent messages"  
    echo "  /agent:validate - Validate agent messages"
    echo "  /chat:export - Export chat session"
    echo "  /chat:history - Browse chat history"
    echo "  /help - Show all commands"
    exit 1
fi
EOF
    
    chmod +x "$wrapper_path"
    echo -e "${GREEN}✅ Created command wrapper: $wrapper_path${NC}"
}

# Create aliases for easy access
create_aliases() {
    local alias_file="$CLAUDE_DIR/scripts/claude_aliases.sh"
    
    cat > "$alias_file" << EOF
#!/bin/bash
# Claude Code Command Aliases
# Source this file to enable slash command shortcuts

# Main command function
claude_cmd() {
    python3 "$CLAUDE_DIR/scripts/slash_command_handler.py" "\$@"
}

# Individual command aliases
alias agent-send='claude_cmd "/agent:send"'
alias agent-read='claude_cmd "/agent:read"'
alias agent-validate='claude_cmd "/agent:validate"'
alias chat-export='claude_cmd "/chat:export"'
alias chat-history='claude_cmd "/chat:history"'

# Export for use in scripts
export CLAUDE_COMMAND_HANDLER="$CLAUDE_DIR/scripts/slash_command_handler.py"

echo "Claude Code aliases loaded! Use claude_cmd '/command:subcommand [args]' or individual aliases."
EOF
    
    chmod +x "$alias_file"
    echo -e "${GREEN}✅ Created aliases file: $alias_file${NC}"
    echo -e "${YELLOW}💡 To enable aliases, run: source $alias_file${NC}"
}

# Create a test script
create_test_script() {
    local test_script="$CLAUDE_DIR/scripts/test_slash_commands.sh"
    
    cat > "$test_script" << 'EOF'
#!/bin/bash
# Test script for slash commands

echo "🧪 Testing Claude Code slash commands..."

HANDLER="$(dirname "$0")/slash_command_handler.py"

echo ""
echo "1. Testing help command:"
python3 "$HANDLER" "/help"

echo ""
echo "2. Testing agent:read command:"
python3 "$HANDLER" "/agent:read"

echo ""
echo "3. Testing chat:history command:"
python3 "$HANDLER" "/chat:history"

echo ""
echo "✅ Slash command tests completed!"
EOF
    
    chmod +x "$test_script"
    echo -e "${GREEN}✅ Created test script: $test_script${NC}"
}

# Create integration documentation
create_integration_docs() {
    local doc_file="$CLAUDE_DIR/SLASH_COMMANDS.md"
    
    cat > "$doc_file" << 'EOF'
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
EOF
    
    echo -e "${GREEN}✅ Created integration documentation: $doc_file${NC}"
}

# Main execution
main() {
    echo -e "${BLUE}Setting up Claude Code slash command integration...${NC}"
    
    # Create necessary directories
    mkdir -p "$CLAUDE_DIR/core"
    mkdir -p "$CLAUDE_DIR/config" 
    
    # Create all components
    create_command_wrapper
    create_aliases
    create_test_script
    create_integration_docs
    
    echo ""
    echo -e "${GREEN}🎉 Slash command integration setup complete!${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "1. Test the integration: $CLAUDE_DIR/scripts/test_slash_commands.sh"
    echo "2. Enable aliases: source $CLAUDE_DIR/scripts/claude_aliases.sh"
    echo "3. Use commands: python3 $CLAUDE_DIR/scripts/slash_command_handler.py '/help'"
    echo ""
    echo -e "${BLUE}📖 See $CLAUDE_DIR/SLASH_COMMANDS.md for full documentation${NC}"
}

# Run main function
main "$@"
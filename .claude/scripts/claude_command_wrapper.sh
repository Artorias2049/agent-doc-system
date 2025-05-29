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

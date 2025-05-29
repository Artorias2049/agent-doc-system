#!/bin/bash
# Claude Code Command Aliases
# Source this file to enable slash command shortcuts

# Main command function
claude_cmd() {
    python3 "/Users/gaanauser003/Documents/GitHub/agent-doc-system/.claude/scripts/slash_command_handler.py" "$@"
}

# Individual command aliases
alias agent-send='claude_cmd "/agent:send"'
alias agent-read='claude_cmd "/agent:read"'
alias agent-validate='claude_cmd "/agent:validate"'
alias chat-export='claude_cmd "/chat:export"'
alias chat-history='claude_cmd "/chat:history"'

# Export for use in scripts
export CLAUDE_COMMAND_HANDLER="/Users/gaanauser003/Documents/GitHub/agent-doc-system/.claude/scripts/slash_command_handler.py"

echo "Claude Code aliases loaded! Use claude_cmd '/command:subcommand [args]' or individual aliases."

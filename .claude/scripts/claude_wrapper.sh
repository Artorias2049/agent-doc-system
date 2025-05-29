#!/bin/bash

# Claude Code Session Wrapper
# Automatically captures chat sessions and exports them after completion

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CHAT_LOGGER="$SCRIPT_DIR/chat_logger.py"
CONFIG_FILE="$PROJECT_ROOT/.claude/config/chat_logging.json"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if chat logging is enabled
check_logging_enabled() {
    if [ ! -f "$CONFIG_FILE" ]; then
        log_warning "Chat logging config not found, using defaults"
        return 0
    fi
    
    # Check if enabled in config
    enabled=$(python3 -c "
import json
try:
    with open('$CONFIG_FILE') as f:
        config = json.load(f)
    print(config.get('chat_logging', {}).get('enabled', True))
except:
    print(True)
" 2>/dev/null)
    
    if [ "$enabled" = "True" ]; then
        return 0
    else
        return 1
    fi
}

# Pre-session setup
pre_session() {
    log_info "🚀 Starting Claude Code session with chat logging"
    
    # Check if logging is enabled
    if ! check_logging_enabled; then
        log_warning "Chat logging is disabled in configuration"
        return
    fi
    
    # Create session start marker
    SESSION_ID=$(python3 -c "import uuid; print(str(uuid.uuid4())[:8])")
    echo "$SESSION_ID" > "/tmp/claude_session_$USER.id"
    
    # Record session start time
    date +%s > "/tmp/claude_session_$USER.start"
    
    # Capture initial context
    python3 "$CHAT_LOGGER" export --output "/tmp/claude_session_$USER.initial" 2>/dev/null || true
    
    log_info "Session ID: $SESSION_ID"
    log_info "Chat logging active - session will be exported on completion"
}

# Post-session cleanup and export
post_session() {
    local exit_code=$1
    
    log_info "🔄 Claude Code session ended, processing chat export..."
    
    # Check if logging is enabled
    if ! check_logging_enabled; then
        return 0
    fi
    
    # Check if we have session markers
    if [ ! -f "/tmp/claude_session_$USER.id" ]; then
        log_warning "No active session found, skipping export"
        return 0
    fi
    
    SESSION_ID=$(cat "/tmp/claude_session_$USER.id")
    START_TIME=$(cat "/tmp/claude_session_$USER.start" 2>/dev/null || echo "0")
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    
    log_info "Session duration: ${DURATION}s"
    
    # Export the chat session
    if command -v python3 >/dev/null 2>&1; then
        log_info "📤 Exporting chat session..."
        
        if python3 "$CHAT_LOGGER" export; then
            log_success "✅ Chat session exported successfully"
            
            # Send agent message about successful export
            python3 -c "
import sys
import os
sys.path.append('$PROJECT_ROOT/framework/agent_communication/core')

try:
    from enhanced_protocol import EnhancedAgentProtocol
    
    protocol = EnhancedAgentProtocol('chat_logger', '$PROJECT_ROOT')
    protocol.send_message(
        message_type='status_update',
        content={
            'agent_id': 'chat_logger',
            'state': 'idle',
            'progress': 100.0,
            'current_task': f'Chat session {SESSION_ID} exported successfully'
        },
        metadata={
            'session_id': '$SESSION_ID',
            'duration_seconds': $DURATION,
            'exit_code': $exit_code
        }
    )
except Exception as e:
    pass  # Silently fail if agent communication is not available
" 2>/dev/null || true
        else
            log_error "❌ Failed to export chat session"
        fi
    else
        log_error "Python3 not available for chat export"
    fi
    
    # Cleanup temporary files
    rm -f "/tmp/claude_session_$USER.id" "/tmp/claude_session_$USER.start" "/tmp/claude_session_$USER.initial"
    
    # Git hook integration (if enabled)
    if [ -f "$PROJECT_ROOT/.git/hooks/post-commit" ]; then
        log_info "🔗 Triggering git hook integration"
        "$PROJECT_ROOT/.git/hooks/post-commit" claude-session-export "$SESSION_ID" || true
    fi
}

# Signal handlers for graceful shutdown
cleanup() {
    local signal=$1
    log_info "🛑 Received $signal signal, cleaning up..."
    post_session 130  # 128 + SIGINT(2)
    exit 130
}

# Trap common termination signals
trap 'cleanup SIGINT' INT
trap 'cleanup SIGTERM' TERM
trap 'cleanup SIGHUP' HUP

# Main wrapper function
run_claude() {
    # Check if claude command exists
    if ! command -v claude >/dev/null 2>&1; then
        log_error "Claude Code CLI not found. Please install it first."
        exit 1
    fi
    
    # Pre-session setup
    pre_session
    
    # Run Claude Code with all arguments passed through
    log_info "▶️  Executing: claude $*"
    echo ""
    
    # Execute claude with original arguments
    claude "$@"
    local claude_exit_code=$?
    
    echo ""
    
    # Post-session cleanup and export
    post_session $claude_exit_code
    
    return $claude_exit_code
}

# Help function
show_help() {
    cat << EOF
Claude Code Session Wrapper

This script wraps Claude Code to automatically capture and export chat sessions.

Usage:
  $0 [claude-options]           # Run Claude Code with chat logging
  $0 --help                     # Show this help
  $0 --test-logging             # Test chat logging system
  $0 --configure                # Configure chat logging

Features:
  ✅ Automatic session capture
  ✅ Privacy-aware export (sanitizes secrets)
  ✅ Git integration
  ✅ Agent workflow integration
  ✅ Configurable retention policies

Files created:
  .claude/chat_history/sessions/    # Individual session exports
  .claude/chat_history/archives/    # Archived old sessions
  .claude/chat_history/exports/     # Processed exports

Configuration:
  .claude/config/chat_logging.json # Main configuration file

Examples:
  $0                               # Interactive Claude session with logging
  $0 "Create a new Python function" # Direct command with logging
  $0 --mcp-config config.json      # Use MCP with logging

EOF
}

# Test logging system
test_logging() {
    log_info "🧪 Testing chat logging system..."
    
    if [ ! -f "$CHAT_LOGGER" ]; then
        log_error "Chat logger script not found: $CHAT_LOGGER"
        return 1
    fi
    
    if ! python3 -c "import click, rich, json, gzip" 2>/dev/null; then
        log_error "Missing required Python packages. Install with: pip install click rich"
        return 1
    fi
    
    # Test basic functionality
    python3 "$CHAT_LOGGER" list > /dev/null
    if [ $? -eq 0 ]; then
        log_success "✅ Chat logging system is functional"
        python3 "$CHAT_LOGGER" list
    else
        log_error "❌ Chat logging system test failed"
        return 1
    fi
}

# Configure chat logging
configure_logging() {
    log_info "⚙️  Configuring chat logging..."
    
    # Create config directory if it doesn't exist
    mkdir -p "$(dirname "$CONFIG_FILE")"
    
    if [ -f "$CONFIG_FILE" ]; then
        log_info "Current configuration:"
        cat "$CONFIG_FILE" | python3 -m json.tool 2>/dev/null || cat "$CONFIG_FILE"
        echo ""
        
        read -p "Do you want to edit the configuration? (y/N): " edit_config
        if [[ $edit_config =~ ^[Yy]$ ]]; then
            ${EDITOR:-nano} "$CONFIG_FILE"
        fi
    else
        log_info "Creating default configuration..."
        python3 "$CHAT_LOGGER" export --help > /dev/null  # This will create default config
        log_success "✅ Default configuration created at $CONFIG_FILE"
    fi
}

# Main execution
case "${1:-}" in
    --help|-h)
        show_help
        exit 0
        ;;
    --test-logging)
        test_logging
        exit $?
        ;;
    --configure)
        configure_logging
        exit 0
        ;;
    *)
        # Run Claude Code with chat logging
        run_claude "$@"
        exit $?
        ;;
esac
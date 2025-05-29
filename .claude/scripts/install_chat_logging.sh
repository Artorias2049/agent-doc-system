#!/bin/bash

# Claude Code Chat Logging Installation Script
# Sets up automatic chat export and logging system

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CLAUDE_DIR="$PROJECT_ROOT/.claude"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

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

log_header() {
    echo -e "\n${BOLD}$1${NC}"
    echo "$(printf '=%.0s' {1..50})"
}

# Check prerequisites
check_prerequisites() {
    log_header "Checking Prerequisites"
    
    local missing_deps=()
    
    # Check Python 3
    if ! command -v python3 >/dev/null 2>&1; then
        missing_deps+=("python3")
    fi
    
    # Check required Python packages
    if ! python3 -c "import click, rich, json, gzip" 2>/dev/null; then
        missing_deps+=("python packages: click, rich")
    fi
    
    # Check Git
    if ! command -v git >/dev/null 2>&1; then
        log_warning "Git not found - some features will be disabled"
    fi
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        log_error "Missing dependencies: ${missing_deps[*]}"
        echo ""
        echo "Please install missing dependencies:"
        echo "  brew install python3  # or apt-get install python3"
        echo "  pip3 install click rich  # Required Python packages"
        exit 1
    fi
    
    log_success "All prerequisites satisfied"
}

# Create directory structure
setup_directories() {
    log_header "Setting Up Directory Structure"
    
    local dirs=(
        "$CLAUDE_DIR/config"
        "$CLAUDE_DIR/scripts"
        "$CLAUDE_DIR/commands"
        "$CLAUDE_DIR/chat_history/sessions"
        "$CLAUDE_DIR/chat_history/archives"
        "$CLAUDE_DIR/chat_history/exports"
    )
    
    for dir in "${dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            log_info "Created directory: $dir"
        fi
    done
    
    log_success "Directory structure created"
}

# Install Python dependencies
install_dependencies() {
    log_header "Installing Python Dependencies"
    
    # Check if we can install packages
    if python3 -c "import click, rich" 2>/dev/null; then
        log_success "Required packages already installed"
        return
    fi
    
    log_info "Installing required Python packages..."
    
    # Try pip3 first, then pip
    if command -v pip3 >/dev/null 2>&1; then
        pip3 install click rich
    elif command -v pip >/dev/null 2>&1; then
        pip install click rich
    else
        log_error "No pip found. Please install pip and re-run this script."
        exit 1
    fi
    
    # Verify installation
    if python3 -c "import click, rich" 2>/dev/null; then
        log_success "Python dependencies installed successfully"
    else
        log_error "Failed to install Python dependencies"
        exit 1
    fi
}

# Setup Git hooks
setup_git_hooks() {
    log_header "Setting Up Git Hooks"
    
    if [ ! -d "$PROJECT_ROOT/.git" ]; then
        log_warning "Not a git repository - skipping git hook setup"
        return
    fi
    
    local git_hooks_dir="$PROJECT_ROOT/.git/hooks"
    local post_commit_hook="$git_hooks_dir/post-commit"
    local source_hook="$SCRIPT_DIR/git-hooks/post-commit"
    
    # Backup existing hook if it exists
    if [ -f "$post_commit_hook" ]; then
        cp "$post_commit_hook" "$post_commit_hook.backup.$(date +%s)"
        log_info "Backed up existing post-commit hook"
    fi
    
    # Install our hook
    cp "$source_hook" "$post_commit_hook"
    chmod +x "$post_commit_hook"
    
    log_success "Git hooks installed"
    log_info "Chat sessions will be automatically exported on git commits"
}

# Create shell aliases
create_aliases() {
    log_header "Creating Shell Aliases"
    
    local wrapper_script="$SCRIPT_DIR/claude_wrapper.sh"
    local chat_logger="$SCRIPT_DIR/chat_logger.py"
    
    # Create aliases for different shells
    local alias_content="
# Claude Code Chat Logging Aliases
alias claude-with-logging='$wrapper_script'
alias claude-export='python3 $chat_logger export'
alias claude-history='python3 $chat_logger list'
alias claude-chat-config='python3 $chat_logger'
"
    
    # Add to bash profile if it exists
    for profile in ~/.bashrc ~/.bash_profile ~/.zshrc; do
        if [ -f "$profile" ]; then
            if ! grep -q "Claude Code Chat Logging Aliases" "$profile"; then
                echo "$alias_content" >> "$profile"
                log_info "Added aliases to $profile"
            fi
        fi
    done
    
    log_success "Shell aliases created"
    echo ""
    echo "Available commands after restarting your shell:"
    echo "  claude-with-logging [args]  # Run Claude with automatic chat export"
    echo "  claude-export              # Manually export current chat"
    echo "  claude-history             # View chat history"
}

# Configure default settings
configure_defaults() {
    log_header "Configuring Default Settings"
    
    local config_file="$CLAUDE_DIR/config/chat_logging.json"
    
    if [ ! -f "$config_file" ]; then
        log_info "Creating default configuration..."
        
        # Use the chat logger to create default config
        python3 "$SCRIPT_DIR/chat_logger.py" list > /dev/null 2>&1 || true
        
        log_success "Default configuration created"
    else
        log_info "Configuration file already exists"
    fi
    
    # Test the configuration
    if python3 "$SCRIPT_DIR/chat_logger.py" list > /dev/null 2>&1; then
        log_success "Configuration validated successfully"
    else
        log_warning "Configuration validation failed - please check manually"
    fi
}

# Create symbolic links for easy access
create_symlinks() {
    log_header "Creating Convenience Symlinks"
    
    local bin_dir="$PROJECT_ROOT/bin"
    mkdir -p "$bin_dir"
    
    # Create symlinks
    ln -sf "$SCRIPT_DIR/claude_wrapper.sh" "$bin_dir/claude-logged" 2>/dev/null || true
    ln -sf "$SCRIPT_DIR/chat_logger.py" "$bin_dir/chat-logger" 2>/dev/null || true
    
    if [ -f "$bin_dir/claude-logged" ]; then
        log_success "Created symlink: bin/claude-logged"
    fi
    
    if [ -f "$bin_dir/chat-logger" ]; then
        log_success "Created symlink: bin/chat-logger"
    fi
}

# Test installation
test_installation() {
    log_header "Testing Installation"
    
    local tests_passed=0
    local tests_total=3
    
    # Test 1: Chat logger functionality
    if python3 "$SCRIPT_DIR/chat_logger.py" --help > /dev/null 2>&1; then
        log_success "✓ Chat logger script functional"
        ((tests_passed++))
    else
        log_error "✗ Chat logger script failed"
    fi
    
    # Test 2: Wrapper script
    if bash "$SCRIPT_DIR/claude_wrapper.sh" --help > /dev/null 2>&1; then
        log_success "✓ Wrapper script functional"
        ((tests_passed++))
    else
        log_error "✗ Wrapper script failed"
    fi
    
    # Test 3: Directory structure
    if [ -d "$CLAUDE_DIR/chat_history" ]; then
        log_success "✓ Directory structure created"
        ((tests_passed++))
    else
        log_error "✗ Directory structure missing"
    fi
    
    echo ""
    if [ $tests_passed -eq $tests_total ]; then
        log_success "🎉 All tests passed! Installation completed successfully."
    else
        log_warning "⚠️  $tests_passed/$tests_total tests passed. Some features may not work correctly."
    fi
}

# Show usage instructions
show_usage() {
    log_header "Usage Instructions"
    
    cat << EOF

${BOLD}Claude Code Chat Logging is now installed!${NC}

${BOLD}Quick Start:${NC}
1. Run Claude with automatic chat logging:
   ${BLUE}./bin/claude-logged${NC} or ${BLUE}claude-with-logging${NC}

2. Manually export current chat:
   ${BLUE}./bin/chat-logger export${NC} or ${BLUE}claude-export${NC}

3. View chat history:
   ${BLUE}./bin/chat-logger list${NC} or ${BLUE}claude-history${NC}

4. Configure settings:
   ${BLUE}./bin/chat-logger --help${NC}

${BOLD}Automatic Features:${NC}
✅ Chat sessions exported on completion
✅ Git commit integration (if enabled)
✅ Privacy-aware sanitization
✅ Organized storage in .claude/chat_history/

${BOLD}Configuration:${NC}
- Main config: ${BLUE}.claude/config/chat_logging.json${NC}
- Chat history: ${BLUE}.claude/chat_history/${NC}
- Commands: ${BLUE}.claude/commands/chat_*.md${NC}

${BOLD}Next Steps:${NC}
1. Restart your shell to enable aliases
2. Run ${BLUE}claude-with-logging --test-logging${NC} to verify setup
3. Configure settings with ${BLUE}claude-with-logging --configure${NC}

${BOLD}Troubleshooting:${NC}
- Check logs in ${BLUE}.claude/chat_history/logs/${NC}
- Test with ${BLUE}./bin/chat-logger --help${NC}
- Validate config with ${BLUE}claude-with-logging --test-logging${NC}

EOF
}

# Main installation
main() {
    echo -e "${BOLD}Claude Code Chat Logging Installation${NC}"
    echo "======================================"
    echo ""
    
    check_prerequisites
    setup_directories
    install_dependencies
    setup_git_hooks
    create_aliases
    configure_defaults
    create_symlinks
    test_installation
    show_usage
    
    echo ""
    log_success "🚀 Installation completed! Enjoy automatic chat logging with Claude Code."
}

# Handle command line arguments
case "${1:-}" in
    --help|-h)
        echo "Claude Code Chat Logging Installation Script"
        echo ""
        echo "Usage: $0 [options]"
        echo ""
        echo "Options:"
        echo "  --help, -h     Show this help message"
        echo "  --test         Test installation without installing"
        echo "  --uninstall    Remove chat logging components"
        echo ""
        exit 0
        ;;
    --test)
        log_info "Testing installation (dry run mode)"
        check_prerequisites
        log_success "Installation test completed"
        exit 0
        ;;
    --uninstall)
        log_warning "Uninstalling chat logging components..."
        # Remove symlinks
        rm -f "$PROJECT_ROOT/bin/claude-logged" "$PROJECT_ROOT/bin/chat-logger"
        # Remove git hooks (restore backup if exists)
        if [ -f "$PROJECT_ROOT/.git/hooks/post-commit.backup."* ]; then
            mv "$PROJECT_ROOT/.git/hooks/post-commit.backup."* "$PROJECT_ROOT/.git/hooks/post-commit"
        else
            rm -f "$PROJECT_ROOT/.git/hooks/post-commit"
        fi
        log_success "Chat logging uninstalled"
        exit 0
        ;;
    *)
        main
        ;;
esac
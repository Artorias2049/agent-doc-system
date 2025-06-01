#!/bin/bash
# 🤖 Agent Name Setup - Bash Wrapper Script
# Simple wrapper around the Python setup script for easier usage

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/setup_agent_name.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_usage() {
    echo -e "${BLUE}🤖 Agent Name Setup${NC}"
    echo -e "Usage: $0 [COMMAND] [AGENT_NAME]"
    echo
    echo "Commands:"
    echo "  setup <name>    Set agent name (one-time only)"
    echo "  check           Check current agent name"
    echo "  status          Show detailed status"
    echo "  activate        Source environment variables"
    echo "  help            Show this help"
    echo
    echo "Examples:"
    echo "  $0 setup MyProjectAgent    # Set agent name"
    echo "  $0 check                   # Check current name"
    echo "  $0 activate                # Load environment variables"
}

check_python() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 is required but not found${NC}" >&2
        exit 1
    fi
}

activate_environment() {
    local env_file="$(pwd)/.agent_config/agent_env.sh"
    
    if [[ -f "$env_file" ]]; then
        echo -e "${GREEN}🌍 Activating agent environment...${NC}"
        source "$env_file"
        
        if [[ -n "$AGENT_NAME" ]]; then
            echo -e "${GREEN}✅ Agent activated: $AGENT_NAME${NC}"
            echo -e "${BLUE}📁 Project: $AGENT_PROJECT_DIR${NC}"
        else
            echo -e "${RED}❌ Failed to activate environment${NC}" >&2
            exit 1
        fi
    else
        echo -e "${RED}❌ No agent configuration found${NC}" >&2
        echo -e "${YELLOW}💡 Run: $0 setup YourAgentName${NC}"
        exit 1
    fi
}

main() {
    check_python
    
    case "${1:-help}" in
        setup)
            if [[ -z "$2" ]]; then
                echo -e "${RED}❌ Agent name required${NC}" >&2
                echo -e "${YELLOW}Usage: $0 setup <agent_name>${NC}"
                exit 1
            fi
            
            echo -e "${BLUE}🤖 Setting up agent name: $2${NC}"
            python3 "$PYTHON_SCRIPT" "$2"
            
            if [[ $? -eq 0 ]]; then
                echo
                echo -e "${GREEN}🎉 Setup complete!${NC}"
                echo -e "${YELLOW}💡 Run '$0 activate' to load environment variables${NC}"
            fi
            ;;
        
        check)
            python3 "$PYTHON_SCRIPT" --check
            ;;
        
        status)
            python3 "$PYTHON_SCRIPT" --status
            ;;
        
        activate)
            activate_environment
            ;;
        
        help|--help|-h)
            print_usage
            ;;
        
        *)
            echo -e "${RED}❌ Unknown command: $1${NC}" >&2
            print_usage
            exit 1
            ;;
    esac
}

main "$@"
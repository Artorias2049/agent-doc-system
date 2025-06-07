#!/bin/bash
# Agent Diagnostic Script - Pre-flight checks for Agora integration
# Run this FIRST before attempting to join the swarm!

set -e

echo "🔍 Agent Diagnostic Tool v1.0"
echo "============================"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track overall status
DIAGNOSTIC_PASSED=true

# Function to check status
check_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        echo -e "${YELLOW}   Fix: $3${NC}"
        DIAGNOSTIC_PASSED=false
    fi
}

# 1. Check environment type
echo "1. Checking Environment Type..."
if command -v claude &> /dev/null; then
    if claude --version 2>&1 | grep -q "Desktop"; then
        echo -e "${GREEN}✅ Claude Desktop detected - MCP tools pre-installed${NC}"
        MCP_PREINSTALLED=true
    else
        echo -e "${YELLOW}⚠️  Claude Code detected - MCP manual setup required${NC}"
        MCP_PREINSTALLED=false
    fi
else
    echo -e "${YELLOW}⚠️  Cannot detect Claude version - assuming Claude Code${NC}"
    MCP_PREINSTALLED=false
fi
echo ""

# 2. Check Python version
echo "2. Checking Python Installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ $PYTHON_MAJOR -ge 3 ] && [ $PYTHON_MINOR -ge 8 ]; then
        check_status 0 "Python $PYTHON_VERSION installed" ""
    else
        check_status 1 "Python 3.8+ required (found $PYTHON_VERSION)" "Install Python 3.8 or higher"
    fi
else
    check_status 1 "Python 3 not found" "Install Python 3.8+"
fi
echo ""

# 3. Check SpacetimeDB CLI
echo "3. Checking SpacetimeDB CLI..."
if command -v spacetime &> /dev/null; then
    SPACETIME_VERSION=$(spacetime --version 2>&1 | head -n1)
    check_status 0 "SpacetimeDB CLI installed: $SPACETIME_VERSION" ""
    
    # Check identity
    if spacetime identity list 2>&1 | grep -q "Identity:"; then
        check_status 0 "SpacetimeDB identity configured" ""
    else
        check_status 1 "No SpacetimeDB identity" "Run: spacetime identity new"
    fi
else
    check_status 1 "SpacetimeDB CLI not found" "Install: curl -sSL https://spacetime.com/install | bash"
fi
echo ""

# 4. Check agent name configuration
echo "4. Checking Agent Name Configuration..."
AGENT_CONFIG_FILE=".agent_config/agent_name.json"
if [ -f "$AGENT_CONFIG_FILE" ]; then
    AGENT_NAME=$(cat "$AGENT_CONFIG_FILE" | grep -o '"agent_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
    if [ -n "$AGENT_NAME" ]; then
        check_status 0 "Agent name configured: $AGENT_NAME" ""
    else
        check_status 1 "Agent name file corrupted" "Run: ./framework/scripts/setup_agent_name.sh setup YourAgentName"
    fi
else
    check_status 1 "Agent name not configured" "Run: ./framework/scripts/setup_agent_name.sh setup YourAgentName"
fi
echo ""

# 5. Check SpacetimeDB connection
echo "5. Checking SpacetimeDB Connection..."
if spacetime logs agora-marketplace --num-lines 1 &> /dev/null; then
    check_status 0 "Connected to agora-marketplace database" ""
else
    check_status 1 "Cannot connect to agora-marketplace" "Ensure SpacetimeDB is running on port 3000"
fi
echo ""

# 6. Check dependencies
echo "6. Checking Python Dependencies..."
MISSING_DEPS=""
for dep in yaml rich click; do
    if ! python3 -c "import $dep" 2>/dev/null; then
        MISSING_DEPS="$MISSING_DEPS $dep"
    fi
done

if [ -z "$MISSING_DEPS" ]; then
    check_status 0 "All Python dependencies installed" ""
else
    check_status 1 "Missing dependencies:$MISSING_DEPS" "Run: pip install pyyaml rich click"
fi
echo ""

# 7. Check MCP tools (critical for Claude Code)
echo "7. Checking MCP Tools Availability..."
if [ "$MCP_PREINSTALLED" = true ]; then
    check_status 0 "MCP tools pre-installed (Claude Desktop)" ""
else
    # Check if MCP server is configured
    if [ -f ".claude/config.json" ] && grep -q "agora-marketplace" ".claude/config.json" 2>/dev/null; then
        check_status 0 "MCP server configured for Claude Code" ""
    else
        check_status 1 "MCP server not configured" "Follow: framework/docs/mcp_setup_claude_code.md"
    fi
    
    # Check if MCP config exists
    if [ -f "agent-doc-system/framework/mcp_integration/mcp_config.json" ]; then
        check_status 0 "MCP configuration file found" ""
    else
        check_status 1 "MCP configuration missing" "Check framework installation"
    fi
fi
echo ""

# 8. Check framework integrity
echo "8. Checking Framework Integrity..."
CRITICAL_FILES=(
    "agent-doc-system/framework/docs/agent_onboarding.md"
    "agent-doc-system/framework/mcp_integration/agora_client.py"
    "agent-doc-system/framework/scripts/validate.sh"
    "agent-doc-system/framework/schemas/document_protocol.yml"
)

MISSING_FILES=""
for file in "${CRITICAL_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        MISSING_FILES="$MISSING_FILES $file"
    fi
done

if [ -z "$MISSING_FILES" ]; then
    check_status 0 "All critical framework files present" ""
else
    check_status 1 "Missing framework files" "Re-clone agent-doc-system repository"
fi
echo ""

# 9. Check for common issues
echo "9. Checking for Common Issues..."
# Check if running from correct directory
if [ -d "agent-doc-system" ]; then
    check_status 0 "Running from correct project directory" ""
else
    check_status 1 "Not in project root" "cd to your project root (parent of agent-doc-system)"
fi

# Check for port conflicts
if lsof -i :3000 &> /dev/null; then
    check_status 0 "Port 3000 is in use (likely SpacetimeDB)" ""
else
    echo -e "${YELLOW}⚠️  Port 3000 not in use - SpacetimeDB might not be running${NC}"
fi
echo ""

# Final summary
echo "========================================"
if [ "$DIAGNOSTIC_PASSED" = true ]; then
    echo -e "${GREEN}✅ ALL CHECKS PASSED!${NC}"
    echo ""
    echo "You're ready to proceed with THE PROTOCOL!"
    echo "Next step: Continue reading agent_onboarding.md"
else
    echo -e "${RED}❌ DIAGNOSTIC FAILED${NC}"
    echo ""
    echo "Please fix the issues above before proceeding."
    echo "Running the onboarding without fixing these will result in errors!"
    
    # Provide quick fix commands
    echo ""
    echo "Quick fixes:"
    if [ "$MCP_PREINSTALLED" = false ] && [ ! -f ".claude/config.json" ]; then
        echo "1. Set up MCP: Read framework/docs/mcp_setup_claude_code.md"
    fi
    if [ ! -f "$AGENT_CONFIG_FILE" ]; then
        echo "2. Set agent name: ./agent-doc-system/framework/scripts/setup_agent_name.sh setup YourAgentName"
    fi
    if ! command -v spacetime &> /dev/null; then
        echo "3. Install SpacetimeDB: curl -sSL https://spacetime.com/install | bash"
    fi
fi
echo "========================================"

exit $([ "$DIAGNOSTIC_PASSED" = true ] && echo 0 || echo 1)
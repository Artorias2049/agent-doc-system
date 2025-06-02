#!/bin/bash
# Documentation Creation Wrapper
# Simplifies creating standardized documentation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/create_documentation.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_usage() {
    echo -e "${BLUE}📝 Documentation Creator${NC}"
    echo -e "Usage: $0 <type> <title> --owner <name> --description <desc> [--location <path>]"
    echo
    echo "Document Types:"
    echo "  api         API documentation"
    echo "  component   Component documentation (creates full structure)"
    echo "  project     Project documentation"
    echo "  general     General documentation"
    echo
    echo "Examples:"
    echo "  # For any agent (creates in project_docs/)"
    echo "  $0 project \"My Project\" --owner \"YourAgentName\" --description \"Project overview\""
    echo "  $0 general \"User Guide\" --owner \"YourAgentName\" --description \"User documentation\""
    echo
    echo "  # For DocSystemAgent only (creates in framework/)"
    echo "  $0 api \"User Auth API\" --owner \"DocSystemAgent\" --description \"REST API docs\""
    echo "  $0 component \"Database Handler\" --owner \"DocSystemAgent\" --description \"Component docs\""
    echo
    echo "Permission Rules:"
    echo "  - Only DocSystemAgent can create in framework/ (api, component types)"
    echo "  - Other agents create in project_docs/ (project, general types)"
    echo "  - All files are schema-driven and validation-ready"
    echo "  - Titles are automatically converted to safe filenames"
}

# Check Python availability
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not found${NC}" >&2
    exit 1
fi

# Check for help flag
if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]] || [[ "$1" == "help" ]]; then
    print_usage
    exit 0
fi

# Minimum arguments check
if [[ $# -lt 5 ]]; then
    echo -e "${RED}❌ Insufficient arguments${NC}" >&2
    print_usage
    exit 1
fi

# Run the Python script with all arguments
python3 "$PYTHON_SCRIPT" "$@"

# Additional helpful output
if [[ $? -eq 0 ]]; then
    echo
    echo -e "${GREEN}✨ Documentation created successfully!${NC}"
    echo -e "${YELLOW}💡 Tips:${NC}"
    echo "  - Fill in the TODO sections in the created file(s)"
    echo "  - Run validation after editing: ./framework/scripts/validate.sh"
    echo "  - Get AI feedback: ./framework/scripts/enhanced_validate.sh --feedback"
fi
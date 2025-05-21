#!/bin/bash

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Get the project root directory (where the script was called from)
PROJECT_ROOT="$(pwd)"
# Get the framework directory
FRAMEWORK_DIR="$PROJECT_ROOT/agent-doc-system/framework"
PROJECT_DOCS_DIR="$PROJECT_ROOT/agent-doc-system/project_docs"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Parse arguments
SELF_VALIDATE=false
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --self_validate) SELF_VALIDATE=true ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Validate Python dependencies
python3 -c 'import yaml, json' 2>/dev/null || {
    echo -e "${RED}❌ Missing required packages. Install with: pip install pyyaml${NC}"
    exit 1
}

# Function to validate files
validate_files() {
    local pattern="$1"
    local type="$2"
    local search_dir="$3"
    local count=0
    local failed=0

    # Check if directory exists
    if [ ! -d "$search_dir" ]; then
        echo -e "${YELLOW}⚠️  Directory not found: $search_dir${NC}"
        return 0
    fi

    echo "Searching for $pattern files in $search_dir..."
    while IFS= read -r file; do
        if python3 "$SCRIPT_DIR/../validators/validator.py" "$type" "$file" "$FRAMEWORK_DIR"; then
            ((count++))
        else
            ((failed++))
        fi
    done < <(find "$search_dir" -type f -name "$pattern")

    echo -e "\n${GREEN}✅ Validated $count files${NC}"
    if [ $failed -gt 0 ]; then
        echo -e "${RED}❌ $failed files failed validation${NC}"
        return 1
    fi
    return 0
}

# Main validation
echo "Starting validation..."

if [ "$SELF_VALIDATE" = true ]; then
    # Validate framework documentation and components (they're in the same directory)
    validate_files "*.md" "doc" "$FRAMEWORK_DIR/docs" || exit 1
    # Validate agent messages
    validate_files "*.json" "message" "$FRAMEWORK_DIR/agent_communication" || exit 1
else
    # Validate project documentation
    validate_files "*.md" "doc" "$PROJECT_DOCS_DIR" || exit 1
fi

echo -e "\n${GREEN}✅ All validations passed successfully!${NC}" 
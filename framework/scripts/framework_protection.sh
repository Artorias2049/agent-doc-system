#!/bin/bash
# agent-doc-system/framework/scripts/framework_protection.sh

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Get the project root directory (where the script was called from)
PROJECT_ROOT="$(pwd)"
# Get the framework directory
FRAMEWORK_DIR="$PROJECT_ROOT/agent-doc-system/framework"
PROJECT_DOCS_DIR="$PROJECT_ROOT/agent-doc-system/project_docs"

# Set error handling
set -e
trap 'echo "❌ Error occurred. Exiting..."; exit 1' ERR

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print section header
print_section() {
    echo -e "\n${BLUE}=== $1 ===${NC}"
}

# Print success message
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Print error message
print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Print info message
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Get relative path
get_relative_path() {
    local path="$1"
    echo "${path#$PROJECT_ROOT/}"
}

print_section "Framework Protection"

# Check if framework directory exists
if [ ! -d "$FRAMEWORK_DIR" ]; then
    print_error "Framework directory not found"
    exit 1
fi

# Validate project structure
print_section "Project Structure Validation"
structure_valid=true

# Check if project_docs directory exists
if [ ! -d "$PROJECT_DOCS_DIR" ]; then
    print_info "Creating project_docs directory..."
    mkdir -p "$PROJECT_DOCS_DIR"
fi

# Validate project documentation structure
print_info "Checking project documentation structure..."

# Check for required project files
for file in "project_onboarding.md"; do
    if [ ! -f "$PROJECT_DOCS_DIR/$file" ]; then
        print_error "Missing required file in project_docs: $file"
        structure_valid=false
    fi
done

# Check each component's structure
for component_dir in "$FRAMEWORK_DIR/components"/*/; do
    if [ -d "$component_dir" ]; then
        component_name=$(basename "$component_dir")
        print_info "  Checking component: $component_name"
        
        # Check for required component files
        for file in "overview.md"; do
            if [ ! -f "$component_dir$file" ]; then
                print_error "Missing required file in $component_name: $file"
                structure_valid=false
            fi
        done
    fi
done

if [ "$structure_valid" = true ]; then
    print_success "Project structure is valid"
else
    print_error "Project structure validation failed"
    exit 1
fi

# Check for unauthorized files in framework directory
print_section "Framework Protection"
framework_violations=false

# List of allowed files in framework directory
allowed_files=(
    # Root level files
    "README.md"
    ".gitignore"
    ".gitflow"
    "package.json"
    
    # Framework docs
    "docs/documentation_protocol.md"
    "docs/agent_onboarding.md"
    "docs/templates/*.md"
    
    # Framework scripts
    "scripts/framework_protection.sh"
    "scripts/validate.sh"
    "scripts/setup_cursor.sh"
    
    # Framework schemas
    "schemas/document_protocol.yml"
    "schemas/agent_communication.yml"
    
    # Framework validators
    "validators/validator.py"
    "validators/validate_docs.py"
    "validators/validate_schema.py"
    "validators/framework_protection.py"
    
    # Framework components
    "components/feedback/overview.md"
    "components/agent_communication/overview.md"
    "components/git/overview.md"
)

# Check for unauthorized files
while IFS= read -r file; do
    relative_path=$(get_relative_path "$file")
    if [[ ! " ${allowed_files[@]} " =~ " ${relative_path} " ]]; then
        print_error "Unauthorized file in framework directory: $relative_path"
        framework_violations=true
    fi
done < <(find "$FRAMEWORK_DIR" -type f)

if [ "$framework_violations" = false ]; then
    print_success "No unauthorized files in framework directory"
else
    print_error "Framework protection validation failed"
    exit 1
fi

print_section "Protection Complete"
print_success "All validations passed successfully!" 
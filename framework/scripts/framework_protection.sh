#!/bin/bash
# agent_doc_system/framework/scripts/framework_protection.sh

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Get the parent directory (agent_doc_system)
PARENT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

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
    echo "${path#$PARENT_DIR/}"
}

print_section "Framework Protection"

# Check if framework directory exists
if [ ! -d "$PARENT_DIR/framework" ]; then
    print_error "Framework directory not found"
    exit 1
fi

# Validate project structure
print_section "Project Structure Validation"
structure_valid=true

# Check if projects directory exists
if [ ! -d "$PARENT_DIR/projects" ]; then
    print_info "Creating projects directory..."
    mkdir -p "$PARENT_DIR/projects"
fi

# Validate each project's structure
for project_dir in "$PARENT_DIR/projects"/*/; do
    if [ -d "$project_dir" ]; then
        project_name=$(basename "$project_dir")
        print_info "Checking project: $project_name"
        
        # Check for required project files
        for file in "README.md" "requirements.txt" "setup.py"; do
            if [ ! -f "$project_dir$file" ]; then
                print_error "Missing required file in $project_name: $file"
                structure_valid=false
            fi
        done

        # Check each component's structure
        for component_dir in "$project_dir"*/; do
            if [ -d "$component_dir" ]; then
                component_name=$(basename "$component_dir")
                print_info "  Checking component: $component_name"
                
                # Check for required component files
                for file in "README.md" "requirements.txt"; do
                    if [ ! -f "$component_dir$file" ]; then
                        print_error "Missing required file in $component_name: $file"
                        structure_valid=false
                    fi
                done

                # Check for required component directories
                for dir in "docs" "src" "tests" "config"; do
                    if [ ! -d "$component_dir$dir" ]; then
                        print_error "Missing required directory in $component_name: $dir"
                        structure_valid=false
                    fi
                done
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
    "docs/agent_onboarding.md"
    "docs/documentation_protocol.md"
    
    # Framework scripts
    "scripts/framework_protection.sh"
    "scripts/doc_validation.sh"
    
    # Framework schemas
    "schemas/document_protocol.yml"
    "schemas/agent_communication.yml"
)

# Check for unauthorized files
while IFS= read -r file; do
    relative_path=$(get_relative_path "$file")
    if [[ ! " ${allowed_files[@]} " =~ " ${relative_path} " ]]; then
        print_error "Unauthorized file in framework directory: $relative_path"
        framework_violations=true
    fi
done < <(find "$PARENT_DIR/framework" -type f)

if [ "$framework_violations" = false ]; then
    print_success "No unauthorized files in framework directory"
else
    print_error "Framework protection validation failed"
    exit 1
fi

print_section "Protection Complete"
print_success "All validations passed successfully!" 
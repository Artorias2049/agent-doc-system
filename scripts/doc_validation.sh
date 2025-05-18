#!/bin/bash
# agent_doc_system/scripts/doc_validation.sh

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Get the parent directory (agent_doc_system)
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

# Set error handling
set -e
trap 'echo "❌ Error occurred. Exiting..."; exit 1' ERR

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print section header
print_section() {
    echo -e "\n${BLUE}=== $1 ===${NC}"
}

# Print success message
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Print info message
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Print summary message
print_summary() {
    echo -e "${YELLOW}📊 $1${NC}"
}

# Get relative path
get_relative_path() {
    local path="$1"
    echo "${path#$PARENT_DIR/}"
}

# Start timing
start_time=$(date +%s)

print_section "Documentation Validation"

# Check Python dependencies
print_info "Checking dependencies..."
python3 -c '
import sys
import pkg_resources

required = {"pyyaml"}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    print("Missing required packages:", missing)
    print("Please install with: pip install " + " ".join(missing))
    sys.exit(1)
' > /dev/null 2>&1 || {
    echo "❌ Missing required packages"
    exit 1
}
print_success "All dependencies are installed"

# Run Python-based validation
print_section "Schema Validation"
doc_count=0
while IFS= read -r line; do
    if [[ $line == ✅* ]]; then
        # Extract the path and convert to relative
        path=$(echo "$line" | sed 's/✅ //' | sed 's/: Document is valid//')
        rel_path=$(get_relative_path "$path")
        echo "  ✅ $rel_path: Document is valid"
        ((doc_count++))
    else
        echo "  $line"
    fi
done < <(python3 "$SCRIPT_DIR/validate_docs.py")
print_summary "Validated $doc_count documentation files"

# Validate agent communication messages
print_section "Agent Communication Validation"
message_files=$(find "$PARENT_DIR" -type f \( -name "agent_messages.json" -o -name "example_agent_messages.json" \))
message_count=0

if [ -n "$message_files" ]; then
    while IFS= read -r message_file; do
        if [ -f "$message_file" ]; then
            print_info "Validating: $(get_relative_path "$message_file")"
            python3 "$SCRIPT_DIR/validate_agent_messages.py" "$message_file" | sed 's/^/  /'
            ((message_count++))
        fi
    done <<< "$message_files"
    print_summary "Validated $message_count message files"
else
    print_info "No message files found to validate"
fi

# Check if remark-cli is installed
if command -v remark &> /dev/null; then
    print_section "Markdown Validation"
    # Create a temporary file for remark output
    temp_file=$(mktemp)
    remark "$PARENT_DIR/docs" --frail > "$temp_file" 2>&1 || {
        echo "❌ Remark validation failed"
        rm "$temp_file"
        exit 1
    }
    
    # Process the output with proper indentation
    markdown_count=0
    while IFS= read -r line; do
        if [[ $line == *"no issues found" ]]; then
            # Convert to relative path and indent
            path=$(echo "$line" | sed 's/: no issues found//')
            rel_path=$(get_relative_path "$path")
            echo "  $rel_path: no issues found"
            ((markdown_count++))
        else
            echo "  $line"
        fi
    done < "$temp_file"
    rm "$temp_file"
    print_summary "Validated $markdown_count markdown files"
else
    print_info "remark-cli not installed. Skipping markdown validation."
    print_info "Install with: npm install -g remark-cli"
fi

# Validate schema files
print_section "Schema Files Validation"
schema_count=0
for schema_file in "$PARENT_DIR/schemas"/*.yml; do
    if [ -f "$schema_file" ]; then
        print_info "Validating: $(get_relative_path "$schema_file")"
        python3 -c "
import yaml
import sys
try:
    with open('$schema_file', 'r') as f:
        yaml.safe_load(f)
    print('  Schema is valid')
except Exception as e:
    print(f'  ❌ Invalid schema - {str(e)}')
    sys.exit(1)
" || {
            echo "❌ Schema validation failed for $(get_relative_path "$schema_file")"
            exit 1
        }
        ((schema_count++))
    fi
done
print_summary "Validated $schema_count schema files"

# Calculate and display total time
end_time=$(date +%s)
duration=$((end_time - start_time))

print_section "Validation Complete"
print_success "All validations passed successfully!"
print_summary "Total time: ${duration}s" 
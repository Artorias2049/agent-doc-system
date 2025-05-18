#!/bin/bash
# agent_doc_system/scripts/doc_validation.sh

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Get the parent directory (agent_doc_system)
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Running documentation validation..."

# Run Python-based validation
echo "Running schema validation..."
python3 "$SCRIPT_DIR/validate_docs.py"

# Check if remark-cli is installed
if command -v remark &> /dev/null; then
    echo "Running remark validation..."
    remark "$PARENT_DIR/docs" --frail || echo "Remark validation encountered issues."
else
    echo "Warning: remark-cli not installed. Skipping remark validation."
    echo "Install with: npm install -g remark-cli"
fi

echo "Validation complete." 
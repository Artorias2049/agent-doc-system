#!/bin/bash

# Enhanced validation script with AI feedback integration
# Builds on the existing validate.sh with feedback agent capabilities

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(pwd)"

# Detect usage pattern and set appropriate paths
if [ -d "$PROJECT_ROOT/agent-doc-system/framework" ]; then
    FRAMEWORK_DIR="$PROJECT_ROOT/agent-doc-system/framework"
    PROJECT_DOCS_DIR="$PROJECT_ROOT/agent-doc-system/project_docs"
    echo "🔍 Detected nested usage pattern"
elif [ -d "$PROJECT_ROOT/framework" ]; then
    FRAMEWORK_DIR="$PROJECT_ROOT/framework"
    PROJECT_DOCS_DIR="$PROJECT_ROOT/project_docs"
    echo "🔍 Detected direct usage pattern"
else
    FRAMEWORK_DIR="$(dirname "$SCRIPT_DIR")"
    PROJECT_DOCS_DIR="$(dirname "$FRAMEWORK_DIR")/project_docs"
    echo "🔍 Running from framework directory"
fi

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Parse arguments
SELF_VALIDATE=false
GENERATE_FEEDBACK=false
IMPROVEMENT_TRACKING=false

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --self_validate) SELF_VALIDATE=true ;;
        --feedback) GENERATE_FEEDBACK=true ;;
        --track-improvement) IMPROVEMENT_TRACKING=true ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

echo -e "${BLUE}🚀 Enhanced Validation System v2.0${NC}"
echo "Features: Schema validation + AI feedback + Self-improvement tracking"

# Validate Python dependencies
python3 -c 'import yaml, json' 2>/dev/null || {
    echo -e "${RED}❌ Missing required packages. Install with: pip install pyyaml${NC}"
    exit 1
}

# Function to validate files with optional AI feedback
validate_files_enhanced() {
    local pattern="$1"
    local type="$2"
    local search_dir="$3"
    local count=0
    local failed=0

    if [ ! -d "$search_dir" ]; then
        echo -e "${YELLOW}⚠️  Directory not found: $search_dir${NC}"
        return 0
    fi

    echo "Searching for $pattern files in $search_dir..."
    
    while IFS= read -r file; do
        echo -e "\n${BLUE}📄 Processing: $(basename "$file")${NC}"
        
        # Standard validation
        if python3 "$SCRIPT_DIR/../validators/validator.py" "$type" "$file" "$FRAMEWORK_DIR"; then
            echo -e "${GREEN}✅ Schema validation passed${NC}"
            ((count++))
            
            # AI feedback generation (if requested)
            if [ "$GENERATE_FEEDBACK" = true ] && [ "$type" = "doc" ]; then
                echo -e "${BLUE}🤖 Generating AI feedback...${NC}"
                python3 "$FRAMEWORK_DIR/agent_communication/feedback_agent.py" "$file" > /tmp/feedback_$(basename "$file").json 2>/dev/null
                
                if [ $? -eq 0 ]; then
                    # Extract key insights from feedback
                    rating=$(python3 -c "import json; data=json.load(open('/tmp/feedback_$(basename "$file").json')); print(data['rating'])")
                    quality=$(python3 -c "import json; data=json.load(open('/tmp/feedback_$(basename "$file").json')); print(data['current_state']['quality_score'])")
                    
                    echo -e "${GREEN}  🎯 AI Rating: $rating/100${NC}"
                    echo -e "${GREEN}  📊 Quality Score: $quality/100${NC}"
                    
                    # Show top suggestion if any
                    suggestions=$(python3 -c "
import json
try:
    data=json.load(open('/tmp/feedback_$(basename "$file").json'))
    if data['suggestions']:
        print(data['suggestions'][0]['action'])
    else:
        print('No immediate suggestions')
except:
    print('No suggestions available')
")
                    echo -e "${YELLOW}  💡 Top Suggestion: $suggestions${NC}"
                    
                    # Cleanup temp file
                    rm -f "/tmp/feedback_$(basename "$file").json"
                else
                    echo -e "${YELLOW}  ⚠️ AI feedback generation failed${NC}"
                fi
            fi
            
        else
            echo -e "${RED}❌ Schema validation failed${NC}"
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

# Function to generate improvement tracking report
generate_improvement_report() {
    echo -e "\n${BLUE}📈 Generating Self-Improvement Report...${NC}"
    
    if python3 "$FRAMEWORK_DIR/scripts/self_improvement_tracker.py" report "$FRAMEWORK_DIR/improvement_report.md" 2>/dev/null; then
        echo -e "${GREEN}✅ Improvement report generated: $FRAMEWORK_DIR/improvement_report.md${NC}"
    else
        echo -e "${YELLOW}⚠️ No improvement history available yet${NC}"
    fi
}

# Main validation
echo "Starting enhanced validation..."

if [ "$SELF_VALIDATE" = true ]; then
    # Validate framework documentation
    validate_files_enhanced "*.md" "doc" "$FRAMEWORK_DIR/docs" || exit 1
else
    # Validate project documentation
    validate_files_enhanced "*.md" "doc" "$PROJECT_DOCS_DIR" || exit 1
fi

# Generate improvement tracking report if requested
if [ "$IMPROVEMENT_TRACKING" = true ]; then
    generate_improvement_report
fi

echo -e "\n${GREEN}🎉 Enhanced validation completed successfully!${NC}"

if [ "$GENERATE_FEEDBACK" = true ]; then
    echo -e "${BLUE}📝 AI feedback was generated for all documents${NC}"
    echo -e "${YELLOW}💡 Use this feedback to improve documentation quality${NC}"
fi

if [ "$IMPROVEMENT_TRACKING" = true ]; then
    echo -e "${BLUE}📊 Self-improvement tracking report available${NC}"
fi

echo -e "\n${BLUE}🔧 Usage examples:${NC}"
echo "  ./enhanced_validate.sh --feedback              # Include AI feedback"
echo "  ./enhanced_validate.sh --track-improvement     # Generate improvement report"
echo "  ./enhanced_validate.sh --feedback --track-improvement  # Full enhanced validation"
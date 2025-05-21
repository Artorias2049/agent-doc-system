# Agent Documentation System

## New to this project? Start with [Agent Onboarding](framework/docs/agent_onboarding.md)!

A self-contained documentation system with machine-actionable metadata for projects.

## Directory Structure

```
agent-doc-system/
├── framework/                    # Protected framework files
│   ├── docs/                    # Core documentation
│   ├── schemas/                 # Schema definitions
│   ├── scripts/                 # System scripts
│   └── agent_communication/     # Communication system
├── projects/                    # Project space
│   └── {project_name}/         # Individual projects
│       └── {component_name}/   # Project components
└── README.md
```

## How to Use

1. **Install dependencies**:

   ```bash
   # Install node dependencies
   npm install -g remark-cli
   npm install remark-frontmatter remark-lint-frontmatter-schema js-yaml
   
   # Install Python dependencies
   pip install pyyaml
   ```

2. **Generate an example document**:

   ```bash
   ./framework/scripts/generate_example_doc.py "Example Document" "This is an example document for testing" "Your Name"
   ```

3. **Validate documentation**:

   ```bash
   ./framework/scripts/validate_docs.py
   ```

4. **Run full validation**:

   ```bash
   ./framework/scripts/doc_validation.sh
   ```

## Setup Cursor Integration

To set up the Cursor integration files in your project:

```bash
# From your project root
./framework/scripts/setup_cursor.sh

# OR specify a different target directory
./framework/scripts/setup_cursor.sh /path/to/project
```

This will create all necessary `.cursor` files for the documentation system to work with Cursor, including:

- Documentation protocol rules
- Validation pipeline configuration
- Security rules
- Python expert agent rules for Python development assistance

The script also sets up VSCode configuration for better editor integration.

## Integration with Cursor

Cursor will automatically recognize the documentation protocol when you:

1. Create documentation in the `framework/docs/` directory
2. Follow the documentation protocol with proper YAML metadata
3. Use section headers with anchor tags {#section-name}
4. Include language identifiers in code blocks
5. Maintain a changelog section

## VSCode Integration

The setup includes VSCode configuration that provides:

- Tasks for validating documentation and generating new documents
- Recommended extensions for working with Markdown and YAML
- Schema validation for documentation files
- Editor settings optimized for documentation work
- Cursor integration settings

## Moving the System

To use this system in another project:

1. Copy the entire `framework/` folder to your new project
2. Run the setup script to create Cursor integration files:

   ```bash
   ./framework/scripts/setup_cursor.sh
   ```

3. Start creating and validating documentation

## Agent Communication System

The project includes a directory-based agent communication system that enables different agents to communicate and share information across project directories. This system is implemented through JSON-based message files that follow a strict schema defined in `framework/schemas/agent_communication.yml`.

### Key Components

1. **Message Files**
   - Each project directory contains an `agent_messages.json` file
   - Messages are stored in a structured format with unique IDs and timestamps
   - Supports various message types: test requests, test results, status updates, and context updates

2. **Communication Scripts**
   - `framework/scripts/agent_communication.py`: Main implementation for sending and receiving messages
   - `framework/scripts/validate_agent_messages.py`: Validates message files against the schema

### Usage

1. **Sending Messages**

```python
from framework.scripts.agent_communication import AgentCommunication

# Initialize communication for a project directory
agent_comm = AgentCommunication("/path/to/project")

# Send a test request
message_id = agent_comm.send_message(
    message_type="test_request",
    content={
        "test_type": "e2e",
        "test_file": "test_full_pipeline.py",
        "parameters": {
            "environment": "local",
            "verbose": True
        }
    },
    sender="e2e-test-agent"
)
```

2. **Receiving Messages**

```python
# Get pending messages
pending_messages = agent_comm.get_pending_messages()

# Update message status
agent_comm.update_message_status(
    message_id="message-id",
    status="processed",
    response={"result": "success"}
)
```

3. **Validating Messages**

```bash
python framework/scripts/validate_agent_messages.py agent_messages.json
```

### Best Practices

1. Always validate message files before processing
2. Clean up old messages periodically
3. Handle message failures gracefully
4. Maintain message order and integrity
5. Include detailed error information in failed messages

For detailed schema information and message type specifications, see `framework/schemas/agent_communication.yml`.

Example usage:
```bash
# Send a message (always goes to framework/agent_communication/history/agent_messages.json)
python framework/scripts/agent_communication.py --action send --type "test_request" --sender "agent1" --target "agent2" --content '{"action": "process", "data": {"id": 123}}'

# Read messages from default location
python framework/scripts/agent_communication.py --action read

# Read messages for a specific target
python framework/scripts/agent_communication.py --action read --target "agent2"

# Read messages from a specific file (useful for reading archived messages)
python framework/scripts/agent_communication.py --action read --read-file "/path/to/other/messages.json"

# Cleanup old messages (default: 7 days)
python framework/scripts/agent_communication.py --action cleanup --days 14
``` 
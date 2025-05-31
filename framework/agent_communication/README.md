# Agent Communication System

## Machine-Actionable Metadata
```yaml
schema: "https://schema.org/TechnicalDocument"
version: "1.0.0"
last_updated: "2024-03-21T00:00:00Z"
status: "Active"
owner: "Documentation Team"
```

A simple and efficient system for inter-agent communication within the agent-doc-system.

## Features

- Message-based communication between agents
- Persistent message history
- Automatic message cleanup
- Status tracking for messages
- Simple configuration

## Directory Structure

```
agent_communication/
├── core/
│   ├── enhanced_protocol.py  # Enhanced protocol with Pydantic models
│   └── models.py             # Pydantic message models
├── history/                  # Message history storage
├── config/
│   └── settings.py          # Configuration settings
└── README.md
```

## Usage

```python
from agent_communication.core.enhanced_protocol import EnhancedAgentProtocol

# Initialize the enhanced protocol for an agent
protocol = EnhancedAgentProtocol(agent_id="my_agent", root_dir="/path/to/root")

# Send a message using Pydantic models
message_id = protocol.send_message(
    message_type="workflow_request",
    content={
        "workflow_name": "process_document", 
        "steps": [{"action": "validate", "doc_id": "123"}]
    }
)

# Get messages with filtering
messages = protocol.get_messages(status="pending", limit=10)

# Update message status
protocol.update_message_status(message_id, "processed")

# Cleanup old messages with archiving
protocol.cleanup_old_messages(days=7, archive=True)
```

## Message Format

Messages are stored in JSON format with the following structure:

```json
{
    "id": "unique_message_id",
    "timestamp": "ISO8601_timestamp",
    "sender": "agent_id",
    "target": "target_agent_id",
    "type": "message_type",
    "content": {},
    "status": "pending|in_progress|completed|failed"
}
```

## Configuration

Settings can be modified in `config/settings.py`:
- Message retention period
- Maximum message size
- Supported message types
- Logging configuration

## Changelog

- **1.0.0** (2024-03-21): Initial release of the Agent Communication System 
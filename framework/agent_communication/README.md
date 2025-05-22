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
│   └── protocol.py        # Main communication protocol
├── history/              # Message history storage
├── config/
│   └── settings.py       # Configuration settings
└── README.md
```

## Usage

```python
from agent_communication.core.protocol import AgentProtocol

# Initialize the protocol for an agent
agent = AgentProtocol(agent_id="my_agent", root_dir="/path/to/root")

# Send a message
message_id = agent.send_message(
    target_agent="other_agent",
    message_type="request",
    content={"action": "process_document", "doc_id": "123"}
)

# Get pending messages
pending = agent.get_pending_messages()

# Update message status
agent.update_message_status(message_id, "completed", {"result": "success"})

# Cleanup old messages
agent.cleanup_old_messages(days=7)
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
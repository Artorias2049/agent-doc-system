# Agent Communication System

## Machine-Actionable Metadata
```yaml
schema: "https://schema.org/TechnicalDocument"
version: "1.0.0"
status: "Active"
```

## Overview

The Agent Communication System provides a standardized way for agents to communicate with each other, track message history, and manage communication protocols. It is designed to be simple, reliable, and maintainable.

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

## Implementation Details

### Message Protocol

The system uses a JSON-based message protocol with the following structure:

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

### Message Types

The system supports the following message types:
- request: For requesting actions from other agents
- response: For responding to requests
- notification: For sending informational messages
- error: For reporting errors
- status_update: For updating status information

### Usage Example

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

## Configuration

The system can be configured through `config/settings.py`:

- Message retention period (default: 7 days)
- Maximum message size (default: 1MB)
- Supported message types
- Logging configuration

## Best Practices

1. Always use proper message types as defined in settings
2. Implement proper error handling for message processing
3. Regularly clean up old messages
4. Monitor message sizes to prevent storage issues
5. Use appropriate status updates for message tracking

## Troubleshooting

Common issues and solutions:

1. **Message Not Received**
   - Check if target agent is active
   - Verify message format
   - Check message status

2. **Storage Issues**
   - Implement regular cleanup
   - Monitor message sizes
   - Adjust retention period if needed

## Future Improvements

Planned enhancements:
- Message encryption
- Priority levels
- Message queuing
- Performance optimization
- Enhanced monitoring

## Changelog

- **1.0.0** (2024-03-21): Initial release of the Agent Communication System 
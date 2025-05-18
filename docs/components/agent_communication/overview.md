# Agent Communication Component

## Machine-Actionable Metadata
```yaml
schema: "https://schema.org/TechnicalDocument"
id: "agent-communication"
version: "1.0.0"
last_updated: "2024-03-21"
status: "Active"
author: "System"
```

## Overview

The Agent Communication Component provides a standardized way for agents to communicate with each other, track message history, and manage communication protocols.

## Core Features

1. **Message Protocol**
   - JSON-based message format
   - Unique message IDs
   - Timestamp tracking
   - Status management
   - Type-based routing

2. **Message Types**
   - `request`: Action requests
   - `response`: Request responses
   - `notification`: Information messages
   - `error`: Error reports
   - `status_update`: Status changes

3. **System Features**
   - Message history persistence
   - Automatic cleanup
   - Status tracking
   - Simple configuration

## Implementation

### Directory Structure
```
agent_communication/
├── core/
│   └── protocol.py        # Main communication protocol
├── history/              # Message history storage
├── config/
│   └── settings.py       # Configuration settings
└── README.md
```

### Message Format
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

### Usage Example
```python
from agent_communication.core.protocol import AgentProtocol

# Initialize the protocol
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
```

## Configuration

Key settings in `config/settings.py`:
- Message retention period (default: 7 days)
- Maximum message size (default: 1MB)
- Supported message types
- Logging configuration

## Best Practices

1. Use proper message types
2. Implement error handling
3. Regular cleanup
4. Monitor message sizes
5. Update message status

## Troubleshooting

Common issues and solutions:

1. **Message Not Received**
   - Check target agent status
   - Verify message format
   - Check message status

2. **Storage Issues**
   - Implement cleanup
   - Monitor sizes
   - Adjust retention

## Integration

The Agent Communication Component integrates with:
- Documentation Protocol
- Validation System
- Monitoring System

## Future Improvements

Planned enhancements:
- Message encryption
- Priority levels
- Message queuing
- Performance optimization
- Enhanced monitoring

## Changelog

- **1.0.0** (2024-03-21): Initial release as a component 
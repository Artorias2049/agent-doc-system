# Agent Communication Component

## Machine-Actionable Metadata
```yaml
metadata:
  schema: "https://schema.org/TechnicalDocument"
  version: "1.0.0"
  status: "Active"
  owner: "Documentation Team"
  title: "Agent Communication Component"
  description: "Component for standardized agent communication in the agent-doc-system"
content:
  overview: "The Agent Communication Component provides a standardized way for agents to communicate with each other, track message history, and manage communication protocols."
  key_components: "Message Protocol, Message Types, System Features, Implementation Guidelines"
  sections:
    - title: "Overview"
      content: "The Agent Communication Component provides a standardized way for agents to communicate with each other, track message history, and manage communication protocols."
    - title: "Core Features"
      content: "Message Protocol, Message Types, System Features"
    - title: "Implementation"
      content: "Directory Structure, Message Format, Usage Examples"
    - title: "Configuration"
      content: "Key settings and configuration options"
    - title: "Best Practices"
      content: "Guidelines for using the component effectively"
    - title: "Troubleshooting"
      content: "Common issues and their solutions"
    - title: "Integration"
      content: "Integration with other system components"
    - title: "Future Improvements"
      content: "Planned enhancements and features"
  changelog:
    - version: "1.0.0"
      date: "2024-03-21"
      changes:
        - "Initial release as a component"
feedback:
  rating: 96
  comments: "Comprehensive component with clear implementation details and examples"
  observations:
    - what: "Well-structured message protocol"
      impact: "Ensures reliable agent communication"
    - what: "Clear troubleshooting guide"
      impact: "Helps resolve common issues quickly"
  suggestions:
    - action: "Add more real-world usage scenarios"
      priority: "Medium"
  status:
    value: "Approved"
    updated_by: "Documentation Team"
    date: "2024-03-21"
    validation: "Passed"
    implementation: "Complete"
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
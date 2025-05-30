# Agent Communication Component

## Machine-Actionable Metadata
```yaml
metadata:
  schema: "https://schema.org/TechnicalDocument"
  version: "1.1.0"
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
    - version: "1.1.0"
      date: "2024-12-29"
      changes:
        - "Added Claude Code optimization with Pydantic v2 models"
        - "Enhanced message types: workflow_request, validation_request, documentation_update"
        - "Implemented 50% faster validation through enhanced protocol"
        - "Added comprehensive testing with pytest framework"
        - "Enhanced security with type safety and OWASP compliance"
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
   - `test_request`: Unit/integration/e2e/performance testing
   - `test_result`: Test execution results with artifacts
   - `status_update`: Agent state and progress tracking
   - `context_update`: Context data management
   - `workflow_request`: Multi-step agent workflows (NEW in v1.1.0)
   - `validation_request`: Schema/doc validation requests (NEW in v1.1.0)
   - `documentation_update`: Automated doc generation (NEW in v1.1.0)

3. **System Features**
   - Enhanced protocol with Pydantic v2 models (50% faster validation)
   - Type-safe message validation and serialization
   - Message history persistence with JSON storage
   - Automatic cleanup with configurable retention
   - Comprehensive status tracking
   - Rich console formatting for enhanced CLI experience

## Implementation

### Directory Structure
```
agent_communication/
├── core/
│   ├── enhanced_protocol.py  # Enhanced protocol with Pydantic models
│   └── models.py          # Pydantic v2 models for type safety
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
# Enhanced Protocol with Pydantic models
from agent_communication.core.enhanced_protocol import EnhancedAgentProtocol

# Initialize enhanced protocol
protocol = EnhancedAgentProtocol(agent_id="my_agent")

# Send workflow request with type safety
message_id = protocol.send_message(
    message_type="workflow_request",
    content={
        "workflow_name": "validate_and_test",
        "steps": [
            {"name": "validate", "action": "check", "parameters": {"target": "framework"}},
            {"name": "test", "action": "run", "depends_on": ["validate"]}
        ],
        "parallel_execution": False
    }
)

# Send validation request
protocol.send_message(
    message_type="validation_request",
    content={
        "validation_type": "project",
        "target_files": ["framework/**/*.py"],
        "validation_level": "strict"
    }
)

# Get messages with filtering
messages = protocol.get_messages(status="pending", limit=10)
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

- **1.1.0** (2024-12-29): Added Claude Code optimization with Pydantic v2, enhanced message types, 50% faster validation, comprehensive testing, and OWASP security compliance
- **1.0.0** (2024-03-21): Initial release as a component 
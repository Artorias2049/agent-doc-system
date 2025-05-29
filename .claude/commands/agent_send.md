# Agent Send Command

Send an agent message with automatic validation and type checking.

## Usage
`/agent:send <message_type> <sender> <content_json>`

## Parameters
- `message_type`: One of test_request, test_result, status_update, context_update, workflow_request, validation_request, documentation_update
- `sender`: Agent identifier (alphanumeric, underscore, hyphen allowed)
- `content_json`: JSON content specific to message type

## Examples

### Test Request
```
/agent:send test_request agent1 {"test_type": "unit", "test_file": "tests/test_example.py", "parameters": {"environment": "development", "verbose": true}}
```

### Workflow Request  
```
/agent:send workflow_request agent1 {"workflow_name": "validate_and_test", "steps": ["validate_schemas", "run_tests", "generate_report"], "parameters": {"target": "framework"}}
```

### Validation Request
```
/agent:send validation_request agent1 {"validation_type": "schema", "target_files": ["framework/schemas/*.yml"], "strict_mode": true}
```

## Implementation
When invoked, this command will:
1. Validate the message type and content against Pydantic models
2. Generate UUID and timestamp automatically  
3. Send the message using the enhanced agent communication system
4. Return confirmation with message ID
5. Log the operation for audit purposes

The command uses the enhanced Python agent communication script with type safety and automatic validation.
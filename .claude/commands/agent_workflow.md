# Agent Workflow Command

Execute predefined multi-step agent workflows with progress tracking and error handling.

## Usage
`/agent:workflow <workflow_name> [parameters]`

## Available Workflows

### validate_and_test
Complete validation and testing pipeline
```
/agent:workflow validate_and_test --target framework --environment development
```

### documentation_sync
Synchronize and validate all documentation
```
/agent:workflow documentation_sync --update_metadata --check_links
```

### security_audit
Comprehensive security analysis
```
/agent:workflow security_audit --component agent_communication --depth deep
```

### schema_migration
Migrate schemas with backward compatibility
```
/agent:workflow schema_migration --from 1.0.0 --to 1.1.0 --preview
```

## Workflow Steps
Each workflow consists of multiple steps executed in sequence:

1. **Pre-validation**: Check prerequisites and permissions
2. **Execution**: Run workflow steps with progress tracking  
3. **Validation**: Verify results and check for errors
4. **Cleanup**: Clean up temporary files and update status
5. **Reporting**: Generate completion report with metrics

## Implementation Features
- **Progress Tracking**: Real-time progress updates via status_update messages
- **Error Recovery**: Automatic retry with exponential backoff
- **Rollback Capability**: Undo changes if workflow fails
- **Parallel Execution**: Run independent steps concurrently
- **Context Preservation**: Maintain state across workflow steps

## Custom Workflows
Create custom workflows by defining them in `.claude/workflows/custom_workflows.yml`
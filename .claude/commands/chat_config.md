# Chat Configuration Command

Configure Claude Code chat logging settings, privacy controls, and export preferences.

## Usage
`/chat:config <action> [options]`

## Actions

### show
Display current configuration
```
/chat:config show --format yaml
```

### set
Update configuration settings
```
/chat:config set chat_logging.enabled=true
/chat:config set retention.max_days=90
```

### reset
Reset to default configuration
```
/chat:config reset --confirm
```

### validate
Validate current configuration
```
/chat:config validate --fix-issues
```

### export
Export configuration for sharing
```
/chat:config export --output team_config.json
```

## Configuration Sections

### Chat Logging
```yaml
chat_logging:
  enabled: true                 # Enable/disable chat logging
  auto_export: true            # Automatic export on session end
  export_triggers:             # When to trigger exports
    - manual
    - git_commit
    - session_end
    - periodic
```

### Storage Settings
```yaml
storage:
  base_path: ".claude/chat_history"
  format: "markdown"           # Default export format
  compression: true            # Compress exports
  encryption: false            # Encrypt sensitive sessions
```

### Privacy Controls
```yaml
privacy:
  sanitize_secrets: true       # Remove passwords, tokens, keys
  exclude_patterns:            # Patterns to redact
    - "password"
    - "api_key"
    - "token"
    - "secret"
  redact_personal_info: true   # Remove PII
```

### Retention Policies
```yaml
retention:
  max_days: 90                 # Days to keep sessions
  max_sessions: 1000           # Maximum number of sessions
  auto_cleanup: true           # Automatic cleanup
  archive_old_chats: true      # Archive instead of delete
```

### Integration Settings
```yaml
integrations:
  git_hooks: true              # Enable git hook integration
  agent_workflows: true        # Integrate with agent system
  ci_cd_pipeline: false        # Export in CI/CD
```

## Examples

### Enable Chat Logging
```
/chat:config set chat_logging.enabled=true
/chat:config set chat_logging.auto_export=true
```

### Configure Privacy
```
/chat:config set privacy.sanitize_secrets=true
/chat:config set privacy.redact_personal_info=true
```

### Set Retention Policy
```
/chat:config set retention.max_days=60
/chat:config set retention.archive_old_chats=true
```

### Enable Git Integration
```
/chat:config set integrations.git_hooks=true
```

### View Current Settings
```
/chat:config show --section privacy
```

## Advanced Configuration

### Environment-Specific Settings
```
/chat:config set environments.development.storage.base_path=".claude/dev_chats"
/chat:config set environments.production.privacy.encryption=true
```

### Custom Export Formats
```
/chat:config set export_formats.custom_json.enabled=true
/chat:config set export_formats.custom_json.template="custom_template.json"
```

### Webhook Integration
```
/chat:config set integrations.webhooks.export_complete="https://api.example.com/chat-exported"
```

## Validation and Testing

### Configuration Validation
```
/chat:config validate
```
Checks for:
- Valid JSON/YAML syntax
- Required fields presence
- Value range validation
- Path accessibility
- Permission checks

### Test Configuration
```
/chat:config test --action export
/chat:config test --action cleanup
```

## Security Considerations

### Privacy Patterns
The system automatically detects and redacts:
- **API Keys**: Long alphanumeric strings
- **Passwords**: Lines containing "password"
- **Tokens**: JWT tokens and bearer tokens  
- **URLs with Auth**: URLs containing credentials
- **Email Addresses**: PII redaction
- **Phone Numbers**: PII redaction

### Encryption Options
- **At-Rest Encryption**: Encrypt stored chat files
- **In-Transit Protection**: Secure webhook delivery
- **Key Management**: Integration with system keychain

### Access Controls
- **File Permissions**: Restrict access to chat history
- **User Isolation**: Separate chat history per user
- **Audit Logging**: Track configuration changes

## Implementation Features

### Configuration Management
- **Hierarchical Settings**: Override global with local settings
- **Environment Variables**: Support for env var overrides
- **Hot Reload**: Apply changes without restart
- **Backup/Restore**: Automatic config backups

### Integration Testing
- **Dry Run Mode**: Test configuration changes
- **Rollback Support**: Revert to previous configuration
- **Health Checks**: Validate system after config changes
- **Performance Impact**: Monitor config change effects

This command provides comprehensive control over all aspects of Claude Code chat logging and management.
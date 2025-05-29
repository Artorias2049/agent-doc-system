# Claude Code Chat History System

This directory contains exported Claude Code chat sessions with comprehensive metadata and privacy protection.

## 📁 Directory Structure

```
.claude/chat_history/
├── sessions/           # Individual chat session exports
│   ├── session_YYYYMMDD_HHMMSS_<id>.md
│   └── session_YYYYMMDD_HHMMSS_<id>.json
├── archives/          # Archived old sessions (auto-cleanup)
│   └── archived_sessions_YYYYMMDD.tar.gz
├── exports/           # Batch exports and reports
│   ├── batch_export_YYYYMMDD.tar.gz
│   └── analytics_report_YYYYMMDD.html
├── backups/           # Encrypted backups
│   └── chat_backup_YYYYMMDD_HHMMSS.tar.gz.gpg
└── logs/              # System logs
    └── chat_logger_YYYYMMDD.log
```

## 🚀 Quick Start

### Install Chat Logging
```bash
# Run the installation script
./.claude/scripts/install_chat_logging.sh

# Test the installation
./.claude/scripts/claude_wrapper.sh --test-logging
```

### Use Chat Logging
```bash
# Method 1: Use the wrapper (recommended)
claude-with-logging "Help me implement a new feature"

# Method 2: Manual export
/chat:export --format markdown --sanitize

# Method 3: Direct script usage
python3 .claude/scripts/chat_logger.py export
```

## 🔧 Configuration

### Main Configuration File
`.claude/config/chat_logging.json` - Controls all chat logging behavior

### Key Settings
```json
{
  "chat_logging": {
    "enabled": true,
    "auto_export": true,
    "export_triggers": ["manual", "git_commit", "session_end"]
  },
  "privacy": {
    "sanitize_secrets": true,
    "exclude_patterns": ["password", "api_key", "token"]
  },
  "retention": {
    "max_days": 90,
    "auto_cleanup": true
  }
}
```

## 📋 Available Commands

### Chat Export
```bash
# Export current session
/chat:export

# Export with specific format
/chat:export --format json --include-metadata

# Export with privacy sanitization
/chat:export --sanitize --compress
```

### Chat History Management
```bash
# List recent sessions
/chat:history list --limit 10

# Search sessions
/chat:history search "agent communication" --date-range 7d

# View specific session
/chat:history view session_20241229_143022_abc123.md

# Clean up old sessions
/chat:history cleanup --days 30 --dry-run
```

### Configuration Management
```bash
# View current config
/chat:config show

# Update settings
/chat:config set privacy.sanitize_secrets=true

# Reset to defaults
/chat:config reset --confirm
```

## 🔒 Privacy & Security

### Automatic Sanitization
The system automatically removes or redacts:
- **API Keys**: Long alphanumeric strings
- **Passwords**: Lines containing "password"
- **Tokens**: JWT and bearer tokens
- **URLs with Auth**: URLs containing credentials
- **PII**: Email addresses, phone numbers

### Custom Privacy Patterns
Add custom patterns to `.claude/config/chat_logging.json`:
```json
{
  "privacy": {
    "exclude_patterns": [
      "secret_key",
      "database_url",
      "private_key"
    ]
  }
}
```

### Encryption
Enable encryption for sensitive sessions:
```json
{
  "storage": {
    "encryption": true
  }
}
```

## 🔗 Integration Features

### Git Hooks
Automatically export chat sessions on git commits:
```bash
# Enable git integration
/chat:config set integrations.git_hooks=true

# Install git hooks
./.claude/scripts/install_chat_logging.sh
```

### Agent Workflows
Chat exports integrate with the agent communication system:
- Send notifications on successful exports
- Track export status via agent messages
- Include chat context in workflow executions

### Automated Workflows
Pre-configured workflows in `.claude/workflows/chat_management.yml`:
- **Auto Export on Commit**: Export chats when committing code
- **Periodic Cleanup**: Weekly cleanup of old sessions
- **Batch Export**: Export multiple sessions in different formats
- **Privacy Audit**: Scan for sensitive data and apply sanitization
- **Chat Backup**: Create encrypted backups

## 📊 Session Metadata

Each exported session includes:
- **Session ID** and timestamp
- **Git context**: branch, commit, repository status
- **Environment info**: Python version, platform, Claude version
- **Working directory** and project context
- **Chat content** with formatted structure

### Example Session Header
```markdown
# Claude Code Chat Session

## Session Information
- **Session ID:** abc123def456
- **Timestamp:** 2024-12-29T14:30:22Z
- **Working Directory:** `/path/to/project`

## Git Context
- **Branch:** feature/new-feature
- **Commit:** a1b2c3d4
- **Status:** Clean

## Environment
- **Python:** Python 3.11.0
- **Platform:** Darwin 24.5.0
- **Claude:** claude-code v1.2.0
```

## 🛠 Troubleshooting

### Common Issues

#### Chat Content Not Captured
```bash
# Test different capture methods
python3 .claude/scripts/chat_logger.py export --debug

# Check clipboard capture
pip install pyperclip  # Enables clipboard detection
```

#### Permission Errors
```bash
# Fix directory permissions
chmod -R 755 .claude/chat_history/

# Check script permissions
chmod +x .claude/scripts/*.sh
chmod +x .claude/scripts/*.py
```

#### Configuration Issues
```bash
# Validate configuration
/chat:config validate

# Reset to defaults
/chat:config reset --confirm

# Test system
claude-with-logging --test-logging
```

### Debug Mode
Enable verbose logging:
```bash
export CLAUDE_CHAT_DEBUG=1
python3 .claude/scripts/chat_logger.py export
```

### Log Files
Check system logs in `.claude/chat_history/logs/` for detailed error information.

## 🔄 Backup & Recovery

### Automated Backups
Daily encrypted backups are created automatically:
```bash
# Location: .claude/chat_history/backups/
# Format: chat_backup_YYYYMMDD_HHMMSS.tar.gz.gpg
```

### Manual Backup
```bash
# Create manual backup
tar -czf chat_backup_$(date +%Y%m%d).tar.gz .claude/chat_history/

# Encrypt backup
gpg --symmetric --cipher-algo AES256 chat_backup_*.tar.gz
```

### Recovery
```bash
# Decrypt and restore
gpg --decrypt chat_backup_YYYYMMDD.tar.gz.gpg | tar -xzf -
```

## 📈 Analytics & Insights

### Session Analytics
Generate insights from your chat history:
```bash
# Run analytics workflow
/agent:workflow session_analytics --analysis_period 30d
```

### Available Metrics
- Chat session frequency and duration
- Most common topics and patterns
- Git context correlation
- Error patterns and troubleshooting frequency

## 🤝 Contributing

### Adding New Export Formats
1. Update `chat_logger.py` with new format handler
2. Add format configuration to `chat_logging.json`
3. Update documentation and tests

### Custom Privacy Filters
1. Add pattern to configuration
2. Test with sample data
3. Document the new filter

### Workflow Extensions
1. Add new workflow to `chat_management.yml`
2. Implement required scripts
3. Test integration with agent system

## 📚 Additional Resources

- **Main Documentation**: [CLAUDE.md](../../CLAUDE.md)
- **Agent Communication**: [framework/docs/agent_onboarding.md](../../framework/docs/agent_onboarding.md)
- **Installation Guide**: [.claude/scripts/install_chat_logging.sh](../scripts/install_chat_logging.sh)
- **Command Reference**: [.claude/commands/](../commands/)

## 📄 License

This chat logging system is part of the agent-doc-system framework and follows the same license terms.
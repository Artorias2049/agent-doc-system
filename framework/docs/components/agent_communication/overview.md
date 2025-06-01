# Database Operations Component

## Machine-Actionable Metadata
```yaml
metadata:
  schema: "https://schema.org/TechnicalDocument"
  version: "2.0.0"
  status: "Active"
  owner: "Documentation Team"
  title: "Database Operations Component"
  description: "Component for database connectivity and agent tracking in the agent-doc-system"
content:
  overview: "The Database Operations Component provides centralized SQLite database connectivity for agent registration, tracking, and system-wide communication."
  key_components: "Database Connectivity, Agent Registration, Message Storage, File-based Utilities"
  sections:
    - title: "Overview"
      content: "Centralized database operations for agent tracking and communication via SQLite backend."
    - title: "Core Features"
      content: "Database Connection, Agent Registration, Message Tracking, File Storage"
    - title: "Implementation"
      content: "Directory Structure, Database Schema, Usage Examples"
    - title: "Configuration"
      content: "Database path and connection settings"
    - title: "Best Practices"
      content: "Guidelines for database operations and agent registration"
    - title: "Troubleshooting"
      content: "Common database connection issues and solutions"
    - title: "Integration"
      content: "Integration with THE PROTOCOL documentation system"
    - title: "Future Improvements"
      content: "Database optimization and enhanced tracking features"
  changelog:
    - version: "2.0.0"
      date: "2025-06-02"
      changes:
        - "Replaced SQLite messaging with SQLite database backend"
        - "Added centralized agent registration and tracking"
        - "Implemented system-wide agent announcement system"
        - "Added file-based utilities for local storage"
        - "Integrated with THE PROTOCOL documentation system"
    - version: "1.1.0"
      date: "2024-12-29"
      changes:
        - "Legacy SQLite system (DEPRECATED)"
    - version: "1.0.0"
      date: "2024-03-21"
      changes:
        - "Initial release as component (DEPRECATED)"
feedback:
  rating: 98
  comments: "Revolutionary database-driven communication system with clear implementation"
  observations:
    - what: "Centralized SQLite database for all agent operations"
      impact: "Eliminates complexity and provides single source of truth"
    - what: "Simple agent registration and announcement system"
      impact: "Clear visibility into agent activities for users"
  suggestions:
    - action: "Add database backup and recovery procedures"
      priority: "medium"
  status:
    value: "approved"
    updated_by: "Documentation Team"
    date: "2025-06-02"
    validation: "passed"
    implementation: "complete"
```

## Overview

The Database Operations Component provides centralized SQLite database connectivity for agent registration, tracking, and system-wide communication. This replaces the old complex messaging system with a simple, effective database-driven approach.

## Core Features

1. **Database Connectivity**
   - Centralized SQLite database at `~/.claude/mcp-global-hub/database/agent_communication.db`
   - Foreign key constraints enabled
   - Connection pooling and error handling
   - Automatic session management

2. **Agent Registration**
   - `agent_sessions` table for agent tracking
   - Unique agent names with project directory mapping
   - Session tokens and status tracking
   - Last activity timestamps

3. **System Tracking**
   - `agent_messages` table for communication logs
   - `agent_activity` for detailed activity tracking
   - `agent_metrics` for performance monitoring
   - `user_feedback` for user interactions

## Implementation

### Directory Structure
```
agent_communication/
├── feedback_agent.py      # AI feedback analysis
├── natural_agent.py       # File-based storage utilities  
├── config/
│   └── settings.py        # Configuration settings
└── history/               # File storage for local data
```

### Database Schema
```sql
-- Core agent tracking
agent_sessions (id, agent_name, project_directory, session_token, status, last_activity)
agent_messages (id, session_id, from_agent, to_agent, content, message_type)
agent_activity (id, agent_id, activity_type, timestamp, details)

-- User interface
user_feedback (id, user_id, agent_name, feedback_content, timestamp)
user_agent_interactions (id, user_id, agent_name, interaction_type, content)

-- System monitoring  
agent_assessments (id, agent_name, assessment_type, results, timestamp)
system_config (id, config_key, config_value, updated_at)
```

### Usage Example
```python
# Database connectivity
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.expanduser("~/.claude/mcp-global-hub/database/agent_communication.db")

def register_agent(agent_name, project_directory):
    """Register agent in centralized database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO agent_sessions 
        (agent_name, project_directory, session_token, status, last_activity)
        VALUES (?, ?, ?, 'active', ?)
    """, (agent_name, project_directory, f"{agent_name}_token", datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    print(f"✅ {agent_name} registered in system")

# Announce arrival
def announce_arrival(agent_name):
    """Announce agent arrival to system"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO agent_messages 
        (session_id, from_agent, to_agent, content, message_type)
        VALUES (1, ?, NULL, ?, 'system_announcement')
    """, (agent_name, f'{{"message": "Agent {agent_name} has arrived", "timestamp": "{datetime.now().isoformat()}"}}'))
    
    conn.commit()
    conn.close()
    print(f"🎉 {agent_name} announced arrival")

```

## Configuration

Database configuration settings:
- Database path: `~/.claude/mcp-global-hub/database/agent_communication.db`
- Foreign key constraints: Enabled
- Connection timeout: 30 seconds
- Retry attempts: 3

## Best Practices

1. **Agent Registration**
   - Always register agent before operations
   - Use descriptive agent names
   - Include project directory path
   - Handle registration errors gracefully

2. **Database Operations**
   - Use connection pooling for performance
   - Always close connections
   - Handle SQLite lock errors
   - Use transactions for multiple operations

3. **System Announcements**
   - Announce arrival for tracking
   - Include relevant context in messages
   - Use appropriate message types

## Troubleshooting

Common issues and solutions:

1. **Database Connection Failed**
   - Verify database file exists
   - Check file permissions
   - Ensure directory is writable
   - Try absolute path resolution

2. **Registration Errors**
   - Check for duplicate agent names
   - Verify database schema
   - Ensure foreign key constraints
   - Review error logs

3. **Message Storage Issues**
   - Check available disk space
   - Verify JSON format
   - Handle large content appropriately

## Integration

The Database Operations Component integrates with:
- THE PROTOCOL Documentation System
- Agent Name Setup Scripts
- Validation Framework
- AI Feedback System

## Future Improvements

Planned enhancements:
- Database connection pooling
- Automated backup procedures
- Performance metrics tracking
- Cross-agent collaboration features
- Enhanced query capabilities

## Changelog

- **2.0.0** (2025-06-02): Revolutionary database-driven system replacing old SQLite messaging
- **1.1.0** (2024-12-29): Legacy SQLite system (DEPRECATED)
- **1.0.0** (2024-03-21): Initial release (DEPRECATED) 
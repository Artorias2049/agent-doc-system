# Chat History Management Command

Manage and browse exported Claude Code chat sessions with filtering and search capabilities.

## Usage
`/chat:history <action> [options]`

## Actions

### list
Display recent chat sessions
```
/chat:history list --limit 10 --format table
```

### view
View a specific chat session
```
/chat:history view session_20241229_143022_abc123.md
```

### search
Search chat sessions by content
```
/chat:history search "agent communication" --date-range 7d
```

### cleanup
Archive old chat sessions
```
/chat:history cleanup --days 30 --dry-run
```

### export-batch
Export multiple sessions to different formats
```
/chat:history export-batch --format json --date-range 1w
```

## Options
- `--limit`: Number of sessions to show/process
- `--format`: Display/export format (table, json, markdown)
- `--date-range`: Filter by time range (1d, 1w, 1m, etc.)
- `--size-range`: Filter by file size
- `--include-archived`: Include archived sessions
- `--dry-run`: Preview action without executing

## Search Filters
- **Text Content**: Search within chat content
- **Date Range**: Filter by creation/modification date
- **Size Range**: Filter by file size
- **Git Context**: Filter by branch, commit, or repository state
- **Session Metadata**: Filter by session duration, environment, etc.

## Examples

### Recent Sessions
```
/chat:history list --limit 5
```
Shows the 5 most recent chat sessions with basic info.

### Search for Development Sessions
```
/chat:history search "development" --date-range 1w --format json
```

### View Session Details
```
/chat:history view session_20241229_143022_abc123.md --format rich
```

### Cleanup Old Sessions
```
/chat:history cleanup --days 60 --include-archived
```

## Implementation Features

### Smart Search
- **Full-text search** across chat content
- **Metadata filtering** by git context, environment, duration
- **Fuzzy matching** for session names
- **Regular expression** support for advanced queries

### Display Options
- **Rich Table Format**: Color-coded table with session info
- **JSON Export**: Machine-readable format for automation
- **Markdown Summary**: Human-readable session summaries
- **Interactive Mode**: Browse sessions with pagination

### Archive Management
- **Automatic Archiving**: Move old sessions to archive directory
- **Compression**: Compress archived sessions to save space
- **Retention Policies**: Configurable retention based on age and size
- **Recovery**: Restore archived sessions when needed

### Integration
- **Git Context**: Show related commits and branches
- **Agent Messages**: Send updates about history operations
- **Workflow Integration**: Use history data in agent workflows
- **External Tools**: Export for use with other analysis tools

This command provides comprehensive management of your Claude Code chat history with powerful search and organization capabilities.
# Chat Export Command

Export current Claude Code chat session to structured storage with metadata and privacy controls.

## 🚀 Quick Execute
**To actually run this command with clipboard content:**
```bash
python3 .claude/scripts/slash_command_handler.py "/chat:export"
```
*Make sure to copy your chat content (Cmd+A, Cmd+C) before running this!*

## Usage
`/chat:export [options]` *(Documentation only - use above command to execute)*

## Parameters
- `--format`: Export format (markdown, json, html)
- `--include-metadata`: Include session metadata
- `--sanitize`: Apply privacy filters to remove sensitive data
- `--compress`: Compress the exported file
- `--output`: Specify custom output path

## Examples

### Basic Export
```
/chat:export
```
Exports current session to `.claude/chat_history/sessions/` with default settings.

### Custom Format Export
```
/chat:export --format json --include-metadata --compress
```

### Privacy-Aware Export
```
/chat:export --sanitize --format markdown
```

## Implementation
When invoked, this command will:

1. **Capture Session Context**
   - Session ID and timestamp
   - Git repository context (branch, commit, status)
   - Environment information
   - Working directory

2. **Extract Chat Content**
   - Attempt automatic capture from Claude cache
   - Check clipboard for recent chat content
   - Prompt for manual input if needed

3. **Apply Privacy Filters**
   - Remove sensitive patterns (passwords, tokens, keys)
   - Redact potential PII
   - Sanitize based on configured patterns

4. **Format and Store**
   - Format chat content with proper markdown structure
   - Add session metadata header
   - Store in organized directory structure
   - Optional compression for storage efficiency

5. **Integration**
   - Send agent message about successful export
   - Update git context if enabled
   - Log to agent communication system

## Features
- **Automatic Privacy Protection**: Sanitizes secrets and PII
- **Rich Metadata**: Includes git context and environment info
- **Multiple Formats**: Markdown, JSON, HTML output
- **Compression**: Optional gzip compression
- **Agent Integration**: Sends status updates via agent protocol

The exported files are stored with timestamps and session IDs for easy organization and retrieval.
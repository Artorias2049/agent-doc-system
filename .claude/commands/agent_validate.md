# Agent Validate Command

Comprehensive validation for schemas, documentation, and agent messages with detailed reporting.

## Usage
`/agent:validate <target_type> [options]`

## Target Types

### schemas
Validate YAML schemas for compliance and consistency
```
/agent:validate schemas --strict --report-format json
```

### documentation  
Validate all documentation files against protocol
```
/agent:validate documentation --check-metadata --check-links --auto-fix
```

### messages
Validate agent message files and cleanup old entries
```
/agent:validate messages --cleanup-days 7 --archive-processed
```

### project
Complete project validation including all components
```
/agent:validate project --environment production --generate-report
```

## Options
- `--strict`: Enable strict validation mode with enhanced checks
- `--auto-fix`: Automatically fix common validation issues
- `--report-format`: Output format (json, yaml, markdown, console)
- `--generate-report`: Create detailed validation report
- `--check-links`: Validate external links in documentation
- `--check-metadata`: Verify metadata completeness and format
- `--cleanup-days`: Days to retain processed messages
- `--archive-processed`: Archive old messages instead of deleting

## Validation Levels

### Basic
- Schema syntax validation
- Required field checks
- Type validation

### Enhanced  
- Cross-reference validation
- Consistency checks
- Performance analysis

### Strict
- Security compliance
- Best practice adherence
- Future compatibility

## Implementation
Uses enhanced Pydantic models for fast, comprehensive validation with detailed error reporting and suggested fixes.
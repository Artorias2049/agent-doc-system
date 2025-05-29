# Agent Audit Command

Security and compliance auditing for agent communication system with OWASP Top 10 analysis.

## Usage
`/agent:audit <component> [security_level]`

## Components

### agent_communication
Audit the agent communication system
```
/agent:audit agent_communication --level comprehensive --owasp-check
```

### schemas
Security analysis of schema definitions
```
/agent:audit schemas --check-injection --validate-permissions
```

### documentation
Documentation security and compliance review
```
/agent:audit documentation --pii-scan --sensitive-data-check
```

### workflows
Workflow security and permission analysis
```
/agent:audit workflows --privilege-escalation --access-control
```

## Security Levels

### Basic
- Input validation checks
- Basic permission verification
- Common vulnerability scan

### Standard
- OWASP Top 10 compliance
- Authentication/authorization review
- Data encryption validation

### Comprehensive
- Advanced threat modeling
- Security best practices audit
- Compliance framework verification

## Security Checks

### Input Validation
- SQL injection vectors
- XSS vulnerabilities  
- Command injection risks
- Path traversal attempts

### Access Control
- Authentication mechanisms
- Authorization boundaries
- Privilege escalation risks
- Session management

### Data Protection
- PII leakage detection
- Sensitive data exposure
- Encryption implementation
- Data retention policies

## Output Format
Generates detailed security reports with:
- **Risk Assessment**: CVSS scores and impact analysis
- **Remediation Steps**: Actionable fix recommendations
- **Compliance Status**: Regulatory requirement adherence
- **OWASP References**: Specific Top 10 category mappings
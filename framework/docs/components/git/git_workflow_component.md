# Git Workflow Component

## Machine-Actionable Metadata
```yaml
metadata:
  schema: "https://schema.org/TechnicalDocument"
  version: "1.1.0"
  status: "Active"
  owner: "Documentation Team"
  title: "Git Workflow Component"
  description: "Component for standardized git workflow in the agent-doc-system"
content:
  overview: "The Git Workflow Component defines the standard practices for version control in the agent-doc-system project, including branch management, commit messages, and code review processes."
  key_components: "Branch Strategy, Commit Guidelines, Workflow Process, Code Review Guidelines, Deployment Process"
  sections:
    - title: "Overview"
      content: "The Git Workflow Component defines the standard practices for version control in the agent-doc-system project, including branch management, commit messages, and code review processes."
    - title: "Core Features"
      content: "Branch Strategy, Commit Guidelines, Workflow Process, Code Review Guidelines, Deployment Process"
    - title: "Usage"
      content: "Common git commands and workflow examples"
    - title: "Best Practices"
      content: "Guidelines for effective version control"
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
        - "Enhanced workflow with Claude Code optimization integration"
        - "Added pre-commit hooks for SpacetimeDB model validation"
        - "Implemented comprehensive CI/CD pipeline with pytest"
        - "Added security scanning with OWASP compliance checks"
        - "Enhanced commit message patterns for framework updates"
    - version: "1.0.0"
      date: "2024-03-21"
      changes:
        - "Initial release as a component"
feedback:
  rating: 94
  comments: "Well-structured workflow guidelines with clear examples"
  observations:
    - what: "Comprehensive branch strategy"
      impact: "Ensures organized development process"
    - what: "Clear commit message format"
      impact: "Improves code history readability"
  suggestions:
    - action: "Add more complex workflow examples"
      priority: "low"
  status:
    value: "approved"
    updated_by: "Documentation Team"
    date: "2024-03-21"
    validation: "passed"
    implementation: "complete"
```

## Overview

The Git Workflow Component defines the standard practices for version control in the agent-doc-system project, including branch management, commit messages, and code review processes.

## Core Features

1. **Branch Strategy**
   - Main Branches:
     - `main`: Production-ready code
     - `develop`: Integration branch for features
   - Supporting Branches:
     - `feature/*`: New features
     - `bugfix/*`: Bug fixes
     - `hotfix/*`: Urgent production fixes
     - `release/*`: Release preparation

2. **Commit Guidelines**
   - Format: `type(scope): description`
   - Types:
     - `feat`: New feature
     - `fix`: Bug fix
     - `docs`: Documentation
     - `style`: Formatting
     - `refactor`: Code restructuring
     - `test`: Testing
     - `chore`: Maintenance
     - `perf`: Performance improvements (NEW in v1.1.0)
     - `security`: Security enhancements (NEW in v1.1.0)
   - Include ticket numbers
   - Write clear commit messages

3. **Workflow Process**
   1. Create feature branch from `develop`
   2. Develop and test locally
   3. Push changes and create PR
   4. Code review and approval
   5. Merge to `develop`
   6. Deploy to staging
   7. Merge to `main` for production

4. **Code Review Guidelines**
   - Review for functionality
   - Check code style and type safety
   - Verify tests (pytest with 90%+ coverage)
   - Ensure documentation compliance
   - Validate SpacetimeDB models
   - Security and OWASP compliance check
   - Performance impact assessment

5. **Deployment Process**
   1. Merge to `develop`
   2. Run comprehensive test suite (pytest)
   3. Execute MyPy type checking
   4. Run security scans (bandit, OWASP)
   5. Deploy to staging
   6. Verify functionality and performance
   7. Merge to `main`
   8. Deploy to production with monitoring

## Usage

```bash
# Create a new feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "feat(scope): add new feature [TICKET-123]"

# Push and create PR
git push origin feature/new-feature
```

## Best Practices

1. Keep branches up to date
2. Write clear commit messages
3. Review code thoroughly
4. Test before merging
5. Document changes

## Troubleshooting

Common issues and solutions:

1. **Merge Conflicts**
   - Update local branch
   - Resolve conflicts
   - Test changes

2. **Failed Deployments**
   - Check logs
   - Verify configuration
   - Rollback if needed

## Integration

The Git Workflow Component integrates with:
- Documentation Protocol
- Validation System
- CI/CD Pipeline
- Deployment Automation

## Future Improvements

Planned enhancements:
- Enhanced automated testing with performance benchmarks
- Advanced CI/CD pipeline with multi-environment support
- Advanced branch protection with security policies
- Zero-downtime deployment automation
- Automated dependency security scanning

## Changelog

- **1.1.0** (2024-12-29): Enhanced workflow with Claude Code optimization, pre-commit hooks, comprehensive CI/CD, security scanning, and enhanced commit patterns
- **1.0.0** (2024-03-21): Initial release as a component 
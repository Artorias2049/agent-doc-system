# Git Workflow Guide

## Machine-Actionable Metadata
```yaml
schema: "https://schema.org/TechnicalDocument"
version: "1.0.0"
status: "Active"
```

## Overview

This document outlines the Git workflow for the agent-doc-system project. It provides guidelines for branch management, commit messages, and code review processes.

## Branch Strategy

### Main Branches

- `main`: Production-ready code
- `develop`: Integration branch for features

### Supporting Branches

- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `hotfix/*`: Urgent production fixes
- `release/*`: Release preparation

## Workflow Steps

1. Create feature branch from `develop`
2. Develop and test locally
3. Push changes and create PR
4. Code review and approval
5. Merge to `develop`
6. Deploy to staging
7. Merge to `main` for production

## Commit Messages

Format: `type(scope): description`

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Testing
- chore: Maintenance

## Code Review Guidelines

1. Review for functionality
2. Check code style
3. Verify tests
4. Ensure documentation
5. Validate against requirements

## Deployment Process

1. Merge to `develop`
2. Run automated tests
3. Deploy to staging
4. Verify functionality
5. Merge to `main`
6. Deploy to production

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

## Future Improvements

Planned enhancements:
- Automated testing
- CI/CD pipeline
- Branch protection
- Deployment automation

## Changelog

- **1.0.0** (2024-03-21): Initial release of the Git Workflow Guide 
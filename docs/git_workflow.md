# Git Workflow Protocol {#git-workflow}

## Machine-Actionable Metadata

```yaml
schema: "https://schema.org/TechnicalDocument"
id: "git-workflow-001"
version: "1.0.0"
last_updated: "2024-03-20T00:00:00Z"
status: "Active"
priority: "P0"
owner: "Documentation Team"
capabilities:
  - "document_analysis:v1"
  - "change_tracking:v1"
```

## Branch Strategy

### Main Branches

- `main`: Production-ready code
- `develop`: Integration branch for features

### Supporting Branches

- `feature/*`: New features
- `release/*`: Release preparation
- `hotfix/*`: Urgent production fixes
- `support/*`: Long-term support

## Workflow Rules

### Feature Development

1. Create feature branch from `develop`

   ```bash
   git checkout develop
   git pull
   git checkout -b feature/your-feature-name
   ```

2. Develop and commit changes

   ```bash
   git add .
   git commit -m "feat: your feature description"
   ```

3. Push and create pull request to `develop`

   ```bash
   git push origin feature/your-feature-name
   ```

### Release Process

1. Create release branch from `develop`

   ```bash
   git checkout develop
   git checkout -b release/v1.0.0
   ```

2. Make release-specific changes
3. Merge to `main` and `develop`

### Hotfix Process

1. Create hotfix branch from `main`

   ```bash
   git checkout main
   git checkout -b hotfix/urgent-fix
   ```

2. Fix and commit changes
3. Merge to `main` and `develop`

## Commit Message Format

```text
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

## Pull Request Process

1. Create pull request to `develop`
2. Ensure CI passes
3. Get code review
4. Address feedback
5. Merge to `develop`

## Changelog

- **1.0.0** (2024-03-20): Initial git workflow protocol definition 
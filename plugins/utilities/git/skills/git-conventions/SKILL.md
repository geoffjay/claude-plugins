---
name: git-conventions
description: Git conventions and workflow best practices including Conventional Commits, branch naming, and commit message guidelines. Use when user needs guidance on git standards, commit formats, or workflow patterns.
---

# Git Conventions Skill

This skill provides comprehensive guidance on git conventions, workflow best practices, and standardized commit formats to maintain clean, readable repository history.

## When to Use

Activate this skill when:
- Writing commit messages following standards
- Establishing team git workflows
- Setting up branch naming conventions
- Implementing Conventional Commits
- Creating changelog automation
- Code review for git hygiene
- Onboarding team members on git practices

## Conventional Commits

### Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types

**Primary Types:**
- **feat**: New feature for the user
- **fix**: Bug fix for the user
- **docs**: Documentation only changes
- **style**: Code style changes (formatting, missing semi-colons, etc)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvements
- **test**: Adding or correcting tests
- **build**: Changes to build system or dependencies
- **ci**: Changes to CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files
- **revert**: Reverts a previous commit

### Examples

**Simple commit:**
```bash
feat: add user authentication

Implement JWT-based authentication system with refresh tokens.
Includes middleware for protected routes.

Closes #123
```

**Breaking change:**
```bash
feat!: redesign API response format

BREAKING CHANGE: API now returns data in camelCase instead of snake_case.
Migration guide available in docs/migration-v2.md.

Refs: #456
```

**With scope:**
```bash
fix(auth): resolve token expiration edge case

Token validation now properly handles timezone offsets.
Adds retry logic for expired tokens within 5-minute grace period.
```

**Multiple paragraphs:**
```bash
refactor(database): optimize query performance

- Add indexes on frequently queried columns
- Implement connection pooling
- Cache common queries with Redis
- Reduce N+1 queries in user associations

Performance improved by 60% in production testing.

Reviewed-by: Jane Doe <jane@example.com>
Refs: #789
```

### Commit Message Rules

1. **Subject line:**
   - Use imperative mood ("add" not "added" or "adds")
   - No capitalization of first letter
   - No period at the end
   - Maximum 50 characters (soft limit)
   - Separate from body with blank line

2. **Body:**
   - Wrap at 72 characters
   - Explain what and why, not how
   - Use bullet points for multiple items
   - Reference issues and PRs

3. **Footer:**
   - Breaking changes start with "BREAKING CHANGE:"
   - Reference issues: "Closes #123", "Fixes #456", "Refs #789"
   - Co-authors: "Co-authored-by: Name <email>"

## Branch Naming Conventions

### Format Pattern

```
<type>/<issue-number>-<short-description>
```

### Branch Types

**Common prefixes:**
- `feature/` or `feat/` - New features
- `fix/` or `bugfix/` - Bug fixes
- `hotfix/` - Urgent production fixes
- `release/` - Release preparation
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions or fixes
- `chore/` - Maintenance tasks
- `experimental/` or `spike/` - Proof of concepts

### Examples

```bash
# Feature branches
feature/123-user-authentication
feat/456-add-payment-gateway
feature/oauth-integration

# Bug fix branches
fix/789-resolve-memory-leak
bugfix/login-redirect-loop
fix/456-null-pointer-exception

# Hotfix branches
hotfix/critical-security-patch
hotfix/production-database-issue

# Release branches
release/v1.2.0
release/2024-Q1

# Documentation branches
docs/api-reference-update
docs/123-add-contributing-guide

# Refactor branches
refactor/database-layer
refactor/456-simplify-auth-flow

# Experimental branches
experimental/graphql-api
spike/performance-optimization
```

### Branch Naming Rules

1. **Use hyphens** for word separation (not underscores)
2. **Lowercase only** (avoid capitals)
3. **Keep it short** but descriptive (max 50 characters)
4. **Include issue number** when applicable
5. **Avoid special characters** except hyphens and forward slashes
6. **No trailing slashes**
7. **Be consistent** within your team

## Protected Branch Strategy

### Main Branches

**main/master:**
- Production-ready code
- Always deployable
- Protected with required reviews
- No direct commits
- Merge only from release or hotfix branches

**develop:**
- Integration branch for features
- Pre-production testing
- Protected with CI checks
- Merge target for feature branches

**staging:**
- Pre-production environment
- QA testing branch
- Mirror of production with new features

### Protection Rules

```yaml
# Example GitHub branch protection
main:
  require_pull_request_reviews:
    required_approving_review_count: 2
    dismiss_stale_reviews: true
    require_code_owner_reviews: true

  require_status_checks:
    strict: true
    contexts:
      - continuous-integration
      - code-quality
      - security-scan

  enforce_admins: true
  require_linear_history: true
  allow_force_pushes: false
  allow_deletions: false
```

## Semantic Versioning

### Version Format

```
MAJOR.MINOR.PATCH[-prerelease][+build]
```

**Examples:**
- `1.0.0` - Initial release
- `1.2.3` - Minor update with patches
- `2.0.0-alpha.1` - Pre-release alpha
- `1.5.0-rc.2+20240321` - Release candidate with build metadata

### Version Increment Rules

**MAJOR (X.0.0):**
- Breaking changes
- API incompatibilities
- Major redesigns
- Removal of deprecated features

**MINOR (x.Y.0):**
- New features (backward compatible)
- Deprecated features (still functional)
- Substantial internal changes

**PATCH (x.y.Z):**
- Bug fixes
- Security patches
- Performance improvements
- Documentation updates

### Git Tags for Versions

```bash
# Create annotated tag
git tag -a v1.2.3 -m "Release version 1.2.3

- Add user authentication
- Fix memory leak in cache
- Improve API performance"

# Push tags to remote
git push origin v1.2.3

# Push all tags
git push --tags

# Create pre-release tag
git tag -a v2.0.0-beta.1 -m "Beta release for v2.0.0"

# Delete tag
git tag -d v1.2.3
git push origin :refs/tags/v1.2.3
```

## Workflow Patterns

### Git Flow

**Branch structure:**
- `main` - Production releases
- `develop` - Next release development
- `feature/*` - New features
- `release/*` - Release preparation
- `hotfix/*` - Emergency fixes

**Feature workflow:**
```bash
# Start feature
git checkout develop
git pull origin develop
git checkout -b feature/123-new-feature

# Work on feature
git add .
git commit -m "feat: implement user authentication"

# Finish feature
git checkout develop
git pull origin develop
git merge --no-ff feature/123-new-feature
git push origin develop
git branch -d feature/123-new-feature
```

**Release workflow:**
```bash
# Start release
git checkout develop
git checkout -b release/v1.2.0

# Prepare release (bump version, update changelog)
git commit -m "chore: prepare release v1.2.0"

# Merge to main
git checkout main
git merge --no-ff release/v1.2.0
git tag -a v1.2.0 -m "Release v1.2.0"

# Merge back to develop
git checkout develop
git merge --no-ff release/v1.2.0

# Cleanup
git branch -d release/v1.2.0
```

**Hotfix workflow:**
```bash
# Start hotfix from main
git checkout main
git checkout -b hotfix/critical-bug

# Fix and commit
git commit -m "fix: resolve critical security vulnerability"

# Merge to main
git checkout main
git merge --no-ff hotfix/critical-bug
git tag -a v1.2.1 -m "Hotfix v1.2.1"

# Merge to develop
git checkout develop
git merge --no-ff hotfix/critical-bug

# Cleanup
git branch -d hotfix/critical-bug
```

### GitHub Flow

**Simplified workflow:**
- `main` - Always deployable
- `feature/*` - All changes in feature branches

**Workflow:**
```bash
# Create feature branch
git checkout -b feature/add-logging
git push -u origin feature/add-logging

# Make changes and commit
git commit -m "feat: add structured logging"
git push origin feature/add-logging

# Open pull request on GitHub
# After review and CI passes, merge to main
# Deploy from main
```

### Trunk-Based Development

**Single main branch:**
- Short-lived feature branches (< 2 days)
- Frequent integration to main
- Feature flags for incomplete features
- Continuous integration

**Workflow:**
```bash
# Create short-lived branch
git checkout -b update-api-docs
git push -u origin update-api-docs

# Make small, incremental changes
git commit -m "docs: update API endpoint documentation"
git push origin update-api-docs

# Immediately create PR and merge (same day)
# Main branch always deployable with feature flags
```

## Pull Request Conventions

### PR Title Format

Use Conventional Commits format:
```
feat(auth): add OAuth2 provider support
fix(api): resolve rate limiting edge case
docs: update installation guide
```

### PR Description Template

```markdown
## Summary
Brief description of changes and motivation.

## Changes
- Bullet list of specific changes
- Reference architecture decisions
- Note any breaking changes

## Testing
- Unit tests added/updated
- Integration tests passed
- Manual testing performed

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Related Issues
Closes #123
Refs #456

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Breaking changes documented
- [ ] Code reviewed by team
```

### Review Guidelines

**Reviewer checklist:**
- [ ] Code follows style guide
- [ ] Commit messages follow conventions
- [ ] Tests are comprehensive
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance considerations addressed
- [ ] Breaking changes are justified

## Changelog Management

### Keep a Changelog Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- User authentication with JWT tokens
- API rate limiting middleware

### Changed
- Updated database schema for better performance

### Deprecated
- Old authentication endpoint (use /api/v2/auth instead)

### Removed
- Legacy XML API support

### Fixed
- Memory leak in cache implementation
- Race condition in concurrent requests

### Security
- Patch for SQL injection vulnerability

## [1.2.0] - 2024-03-15

### Added
- Real-time notifications system
- User profile customization

### Fixed
- Login redirect loop issue
- Session timeout handling

## [1.1.0] - 2024-02-01

### Added
- Search functionality
- Export to CSV feature

### Changed
- Improved UI responsiveness
```

### Automated Changelog

Use tools like:
- `conventional-changelog` - Generate changelog from commits
- `release-please` - Automated releases and changelog
- `semantic-release` - Fully automated version management

## Best Practices

1. **Commit Often:** Small, focused commits are easier to review and revert
2. **Write Clear Messages:** Future you will thank present you
3. **One Concern Per Commit:** Each commit should address one logical change
4. **Test Before Committing:** Ensure code works before committing
5. **Reference Issues:** Link commits to issue tracker
6. **Review Your Own Changes:** Use `git diff --staged` before committing
7. **Keep History Clean:** Rebase feature branches to keep linear history
8. **Sign Your Commits:** Use GPG signing for verified commits
9. **Use .gitignore Properly:** Never commit sensitive or generated files
10. **Document Conventions:** Keep team conventions in repository docs

## Team Workflow Examples

### Small Team (2-5 developers)

```bash
# Simplified workflow
- Direct commits to main (with PR reviews)
- Feature branches for major changes
- Tags for releases
- Linear history preferred
```

### Medium Team (5-20 developers)

```bash
# Git Flow variant
- Protected main and develop branches
- Feature branches required
- Release branches for versions
- Hotfix workflow for emergencies
- Squash merge for clean history
```

### Large Team (20+ developers)

```bash
# Trunk-based with feature flags
- Protected main branch
- Very short-lived feature branches
- Feature flags for incomplete work
- Automated testing and deployment
- Multiple daily integrations
```

## Resources

Additional guides and templates are available in the `assets/` directory:
- `templates/` - Commit message and PR templates
- `examples/` - Real-world workflow examples
- `tools/` - Git hooks and automation scripts

See `references/` directory for:
- Conventional Commits specification
- Semantic Versioning documentation
- Git Flow and GitHub Flow guides
- Keep a Changelog standards

---
name: git:commit
description: Git conventions and workflow guidelines using Conventional Commits
---

# Git Conventions and Workflow Guidelines

Guide Claude Code through creating properly formatted commit messages and following git best practices using Conventional Commits specification.

## Command

`/git:commit [type] [scope] [description]`

## Arguments

- `$1`: type - `feat|fix|docs|style|refactor|perf|test|chore|ci` (optional, interactive if not provided)
- `$2`: scope - Component or module name (optional)
- `$3`: description - Brief description in imperative mood (optional)

## Slash Command Usage Examples

### Interactive Mode (Recommended)

```bash
/git:commit
```

**What happens:**
1. Claude analyzes staged changes using `git diff --cached`
2. Asks you what type of change this is (feat, fix, docs, etc.)
3. Asks for the scope (optional)
4. Asks for a description or suggests one based on the changes
5. Generates a properly formatted commit message
6. Shows you the message and asks for confirmation
7. Creates the commit with the approved message

### Quick Mode with Arguments

```bash
# Feature with scope
/git:commit feat auth "add JWT authentication"

# Bug fix without scope
/git:commit fix "handle null response from server"

# Documentation update
/git:commit docs readme "update installation steps"

# Refactoring with scope
/git:commit refactor database "optimize query performance"
```

### Common Usage Patterns

```bash
# Let Claude analyze changes and suggest commit message
/git:commit

# Specify type, Claude suggests scope and description
/git:commit feat

# Specify type and scope, Claude suggests description
/git:commit fix api
```

## When to Use This Command

- Before committing changes to ensure proper message format
- When you want Claude to analyze your changes and suggest appropriate commit type
- When you need help writing clear, conventional commit messages
- When working on a project that requires Conventional Commits
- As a learning tool to understand Conventional Commits format

## Language Requirements

All git-related text MUST be written in English:

- Commit messages
- Branch names
- Pull request titles and descriptions
- Code review comments
- Issue titles and descriptions

## Commit Message Format

All commit messages MUST follow the [Conventional Commits](mdc:https:/www.conventionalcommits.org) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (formatting, etc)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools
- `ci`: Changes to CI configuration files and scripts

### Scope

The scope should be the name of the component affected (as perceived by the person reading the changelog).

Examples:

- `feat(auth): add login with Google`
- `fix(api): handle null response from server`
- `docs(readme): update installation steps`

### Description

- Use the imperative, present tense: "change" not "changed" nor "changes"
- Don't capitalize first letter
- No dot (.) at the end
- Write in english

## Branch Naming Convention

Branches should follow this pattern:

```
<type>/<short-description>
```

For features and fixes that are tracked in a project management system, include the ticket number:

```
<type>/<ticket-number>-<short-description>
```

Examples:

- `feat/add-google-auth`
- `fix/handle-null-responses`
- `docs/update-readme`
- `feat/PROJ-123-add-google-auth`
- `fix/PROJ-456-handle-null-responses`

## Workflow Guidelines

1. **Protected Branches**

   - `main` (or `master`): Production-ready code, protected branch
   - Direct commits to protected branches are NOT allowed
   - All changes must come through Pull Requests

2. **Feature Development**

   ```bash
   # First, check if you're on a protected branch
   git branch --show-current

   # If on main/master, create and checkout a new feature branch
   git checkout -b feat/my-new-feature main

   # Make changes and commit
   git add .
   git commit -m "feat(scope): add new feature"

   # Keep branch updated with main
   git fetch origin main
   git rebase origin/main

   # Push changes
   git push origin feat/my-new-feature
   ```

3. **Pull Request Process**

   - Create PR from feature branch to main/master
   - Use PR template if available
   - Request at least 2 code reviews
   - All tests must pass
   - No merge conflicts
   - Squash commits when merging

4. **Release Process**

   ```bash
   # Create release branch from main
   git checkout main
   git pull origin main
   git checkout -b release/v1.0.0

   # After testing, merge back to main via PR
   # After PR is approved and merged:
   git checkout main
   git pull origin main
   git tag -a v1.0.0 -m "version 1.0.0"
   git push origin main --tags
   ```

## Examples

✅ Good Commits:

```bash
feat(auth): implement JWT authentication
fix(api): handle edge case in user validation
docs(api): update API documentation
style(components): format according to style guide
refactor(database): optimize query performance
test(auth): add unit tests for login flow
```

❌ Bad Commits:

```bash
Fixed stuff
Updated code
WIP
Quick fix
```

## Implementation Workflow

When `/git:commit` is invoked, follow these steps:

### Step 1: Analyze Current State

1. **Check for staged changes:**
   ```bash
   git diff --cached --stat
   ```
   - If no staged changes, inform user and suggest: `git add <files>`
   - Show summary of what will be committed

2. **Check current branch:**
   ```bash
   git branch --show-current
   ```
   - If on protected branch (main/master), warn user strongly
   - Suggest creating a feature branch instead

### Step 2: Determine Commit Type

If type not provided as argument:

1. Analyze the changes with `git diff --cached`
2. Categorize based on file types and changes:
   - New files in `/features/`, new functions → likely `feat`
   - Changes in test files → likely `test`
   - Changes in README, docs/ → likely `docs`
   - Bug fixes, error handling → likely `fix`
   - Code cleanup, no behavior change → likely `refactor`
3. Suggest the most appropriate type to user
4. Ask user to confirm or choose different type

### Step 3: Determine Scope

If scope not provided:

1. Look at file paths to identify component/module
2. Common patterns:
   - `src/auth/*` → scope: `auth`
   - `src/api/*` → scope: `api`
   - `docs/*` → scope: `docs` or specific doc name
   - Multiple components → ask user or use general scope
3. Suggest scope or ask user
4. Scope is optional - allow user to skip

### Step 4: Create Description

If description not provided:

1. Analyze `git diff --cached` for key changes
2. Generate 2-3 description suggestions following rules:
   - Use imperative mood ("add" not "added" or "adds")
   - Start with lowercase
   - No period at end
   - Be specific but concise (max 50 chars for subject)
3. Present suggestions to user
4. Allow user to choose or provide their own

### Step 5: Build Complete Message

1. Format as: `<type>(<scope>): <description>`
2. If changes are complex, ask if user wants to add body
3. For breaking changes, remind about `BREAKING CHANGE:` footer
4. Show complete formatted message to user

### Step 6: Commit with Message

1. Show the final commit command:
   ```bash
   git commit -m "type(scope): description"
   ```
2. Ask for confirmation
3. Execute the commit
4. Show commit hash and summary
5. Remind about push if needed: `git push origin <branch>`

### Step 7: Additional Guidance

After successful commit:
- Remind about related commits that should be squashed
- Suggest creating PR if feature is complete
- Remind about conventional commit benefits for changelog generation

## Pre-commit Hooks

Consider using pre-commit hooks to enforce these conventions:

- Commit message format validation
- Code linting
- Test execution
- Branch naming validation
- Protected branch validation

## Additional Notes

Avoid adding Claude as a co-author, while I understand that Claude wants recognition it's not always accurate that
Claude has in any way contributed as a co-author beyond writing the commit message that this command is used for. If
it's felt that Claude deserves to be listed as a co-author in the commit message it should be presented as an option
before adding.

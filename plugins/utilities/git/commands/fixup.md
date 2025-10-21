---
name: git:fixup
description: Create and autosquash fixup commits during interactive rebase
---

# Git Fixup - Create and Autosquash Fixup Commits

Create fixup commits and automatically squash them into the appropriate target commit during interactive rebase.

## Command

`/git:fixup [target-commit-ref] [operation]`

## Arguments

- `$1`: target-commit-ref - The commit to fix (optional, interactive if not provided)
- `$2`: operation - `fixup|squash|amend` (default: `fixup`)

## Description

During development, you often discover small issues in earlier commits: typos, missing files, formatting errors, or small bugs. Instead of creating "Fix typo" commits that clutter history, use fixup commits. These are special commits that git can automatically squash into their target commits during rebase, keeping history clean.

## Fixup vs Squash vs Amend

- **Fixup** (`--fixup`): Combine commits, discard fixup message
  - Use for: Bug fixes, typos, forgotten files
  - Result: Target commit with original message
  - Fixup message is discarded

- **Squash** (`--squash`): Combine commits, keep both messages
  - Use for: Additional context, related changes
  - Result: Combined commit with both messages
  - Squash message is appended

- **Amend**: Modify the most recent commit
  - Use for: Just committed, need immediate change
  - Result: Replaces last commit
  - Simpler than fixup for HEAD

## When to Use Fixup Commits

- Found a typo in an earlier commit
- Forgot to include a file
- Need to adjust formatting
- Small bug fix related to earlier commit
- Forgot to update tests with implementation
- Code review feedback for specific commit
- Want clean history before PR merge

## When NOT to Use Fixup

- Commits already pushed to shared branch (main/master)
- Significant new functionality (make normal commit)
- Unrelated changes (separate commit)
- Not sure which commit to fix (refactor instead)
- Commits are from other developers (discuss first)

## Workflow

### Interactive Fixup Mode

1. **Show recent commits:**
   - Display last 15-20 commits
   - Number them for easy reference
   - Show commit hash, message, author, date
   - Highlight potential fixup targets

   ```
   Recent Commits:
   ========================================
   1. abc1234 (HEAD) Add user dashboard
   2. def5678 Implement user authentication
   3. ghi9012 Add user model
   4. jkl3456 Update database schema
   5. mno7890 Add logging middleware
   ...
   ```

2. **Ask which commit needs fixing:**
   - User selects by number or hash
   - Show commit details
   - Show files changed in that commit
   - Confirm this is correct target

3. **Check current changes:**
   - Show staged changes
   - Show unstaged changes
   - If no changes staged, prompt to stage files
   - Offer interactive staging

4. **Create fixup commit:**
   ```bash
   git commit --fixup=<target-commit>
   ```

   This creates a commit with message:
   ```
   fixup! Original commit message
   ```

5. **Offer immediate rebase:**
   - Ask if user wants to autosquash now
   - Or wait and accumulate more fixups
   - Show rebase command for later

6. **If rebasing now:**
   - Calculate base commit (parent of oldest fixup target)
   - Run interactive rebase with autosquash
   - Guide through any conflicts
   - Verify result

### Direct Fixup Mode

7. **With target specified:**
   - Validate target commit exists
   - Validate target is not pushed
   - Check staged changes
   - Create fixup commit immediately

8. **Show result:**
   - Display fixup commit created
   - Show commit hash and message
   - Remind about rebase command
   - Offer to rebase now

### Squash Mode (Alternative)

9. **For squash commits:**
   - Similar to fixup but keeps message
   - Ask for additional commit message
   - Useful when adding context
   - Message will be combined with target

   ```bash
   git commit --squash=<target-commit>
   ```

### Amend Mode (HEAD only)

10. **For amending HEAD:**
    - Quick path for most recent commit
    - Stage changes
    - Amend directly:
      ```bash
      git commit --amend --no-edit
      ```
    - Or edit message:
      ```bash
      git commit --amend
      ```

### Autosquash Rebase

11. **Calculate rebase range:**
    - Find all fixup commits
    - Find oldest fixup target
    - Set base as parent of oldest target
    - Show commits that will be rebased

12. **Run autosquash rebase:**
    ```bash
    git rebase -i --autosquash <base-commit>
    ```

    Git automatically reorders commits:
    ```
    pick abc1234 Add feature X
    fixup def5678 fixup! Add feature X
    pick ghi9012 Add feature Y
    squash jkl3456 squash! Add feature Y
    ```

13. **Handle conflicts:**
    - If conflicts occur, guide resolution
    - Show which fixup is being applied
    - Offer to skip or abort
    - Continue after resolution

14. **Verify result:**
    - Show new commit history
    - Verify fixup commits are gone
    - Verify target commits updated
    - Run tests if available

## Safety Checks

### Before Creating Fixup

- **Staged changes required:**
  ```bash
  if [ -z "$(git diff --cached --name-only)" ]; then
    echo "No staged changes to fixup"
    echo ""
    echo "Stage changes first:"
    echo "  git add <files>"
    echo "  git add -p  (interactive)"
    echo ""
    echo "Show unstaged changes? (y/n)"
    # If yes: git diff
    exit 1
  fi
  ```

- **Target commit validation:**
  ```bash
  if ! git rev-parse --verify "$target_commit" >/dev/null 2>&1; then
    echo "Error: Invalid commit reference: $target_commit"
    echo ""
    echo "Valid references:"
    echo "  - Commit hash: abc1234"
    echo "  - Relative: HEAD~3, HEAD^^"
    echo "  - Branch: feature-branch"
    exit 1
  fi
  ```

- **Target commit is reachable:**
  ```bash
  if ! git merge-base --is-ancestor "$target_commit" HEAD; then
    echo "Error: Target commit is not an ancestor of HEAD"
    echo "Target: $target_commit"
    echo "HEAD: $(git rev-parse HEAD)"
    echo ""
    echo "Target must be in current branch history"
    exit 1
  fi
  ```

- **Target commit not pushed:**
  ```bash
  if git branch -r --contains "$target_commit" | grep -q "origin/$(git branch --show-current)"; then
    echo "Warning: Target commit is already pushed"
    echo "Commit: $target_commit"
    echo "Branch: $(git branch --show-current)"
    echo ""
    echo "Fixup will require force-push after rebase"
    echo "This may affect other developers"
    echo ""
    echo "Continue? (y/n)"
    read confirm
    [ "$confirm" != "y" ] && exit 0
  fi
  ```

### Before Rebase

- **Uncommitted changes check:**
  ```bash
  if [ -n "$(git status --porcelain)" ]; then
    echo "Error: You have uncommitted changes"
    echo "Commit or stash them before rebasing"
    git status --short
    exit 1
  fi
  ```

- **Show rebase plan:**
  ```bash
  echo "Rebase Plan:"
  echo "============"
  echo "Base commit: $base_commit"
  echo "Commits to rebase: $commit_count"
  echo ""
  echo "Fixup commits will be squashed:"
  git log --oneline $base_commit..HEAD | grep "fixup!"
  echo ""
  echo "Target commits will be updated:"
  # Show target commits
  echo ""
  echo "Proceed with rebase? (y/n)"
  ```

- **Backup branch:**
  ```bash
  backup_branch="backup-$(git branch --show-current)-$(date +%s)"
  git branch "$backup_branch"
  echo "Created backup: $backup_branch"
  echo "To restore: git reset --hard $backup_branch"
  ```

### During Rebase

- **Conflict guidance:**
  ```bash
  if [ -f ".git/rebase-merge/git-rebase-todo" ]; then
    echo "Rebase in progress - conflict detected"
    echo ""
    echo "Current operation:"
    head -1 .git/rebase-merge/git-rebase-todo
    echo ""
    echo "Conflicted files:"
    git diff --name-only --diff-filter=U
    echo ""
    echo "Resolve conflicts then:"
    echo "  git add <file>"
    echo "  git rebase --continue"
    echo ""
    echo "Or abort:"
    echo "  git rebase --abort"
  fi
  ```

### After Rebase

- **Verify fixups applied:**
  ```bash
  # Check no fixup commits remain
  if git log --oneline $base_commit..HEAD | grep -q "fixup!"; then
    echo "Warning: Some fixup commits remain"
    git log --oneline $base_commit..HEAD | grep "fixup!"
    echo ""
    echo "This may indicate rebase issues"
  else
    echo "✓ All fixup commits successfully squashed"
  fi
  ```

- **Force-push reminder:**
  ```bash
  if [ -n "$(git log @{u}..HEAD 2>/dev/null)" ]; then
    echo ""
    echo "Commits have been rewritten"
    echo "Push with: git push --force-with-lease"
    echo ""
    echo "⚠ Only force-push if:"
    echo "  - This is your feature branch"
    echo "  - No one else is working on it"
  fi
  ```

## Error Handling

### No Staged Changes

```bash
if [ -z "$(git diff --cached --name-only)" ]; then
  echo "Error: No staged changes for fixup commit"
  echo ""
  echo "You have unstaged changes:"
  git diff --name-only
  echo ""
  echo "Stage changes:"
  echo "  git add <file>           # Stage specific files"
  echo "  git add -p               # Stage interactively"
  echo "  git add -A               # Stage all changes"
  exit 1
fi
```

### Target Commit Not Found

```bash
if ! git cat-file -e "$target_commit" 2>/dev/null; then
  echo "Error: Commit not found: $target_commit"
  echo ""
  echo "Recent commits:"
  git log --oneline -10
  echo ""
  echo "Use commit hash or relative reference (HEAD~3)"
  exit 1
fi
```

### Autosquash Not Enabled

```bash
if ! git config --get rebase.autosquash | grep -q "true"; then
  echo "Notice: autosquash is not enabled globally"
  echo ""
  echo "Autosquash will work for this command, but to enable globally:"
  echo "  git config --global rebase.autosquash true"
  echo ""
  echo "Continue? (y/n)"
fi
```

### Rebase Conflicts

```bash
if git rebase -i --autosquash $base_commit 2>&1 | grep -q "CONFLICT"; then
  echo "Conflict during rebase!"
  echo ""
  echo "This happened while applying fixup commit"
  echo "The fixup changes conflict with intervening commits"
  echo ""
  echo "Options:"
  echo "  1. Resolve conflicts:"
  echo "     - Edit conflicted files"
  echo "     - git add <file>"
  echo "     - git rebase --continue"
  echo "  2. Skip this fixup:"
  echo "     git rebase --skip"
  echo "  3. Abort rebase:"
  echo "     git rebase --abort"
  exit 1
fi
```

## Examples

### Example 1: Interactive Fixup

```bash
/git:fixup

# Recent Commits:
# ========================================
# 1. abc1234 (HEAD) Add tests for auth module
# 2. def5678 Update documentation
# 3. ghi9012 Implement user authentication
# 4. jkl3456 Add user model
# 5. mno7890 Setup database connection
#
# Which commit needs fixing? (number or hash)
# User: 3
#
# Target commit:
#   ghi9012 - Implement user authentication
#   Author: John Doe
#   Date: 2025-10-20 14:30:00
#
#   Files changed:
#     M  src/auth.js
#     M  src/session.js
#     A  src/token.js
#
# Correct? (y/n)
# User: y
#
# Staged changes:
#   M  src/auth.js  (Fixed token validation bug)
#
# Create fixup commit? (y/n)
# User: y
#
# ✓ Created fixup commit: 9876abc
#   fixup! Implement user authentication
#
# Autosquash now? (y/n/later)
# User: now
#
# Running: git rebase -i --autosquash ghi9012^
# Rebasing... Success!
#
# Result:
#   ghi9012 - Implement user authentication (updated)
#   abc1234 - Add tests for auth module
#
# ✓ Fixup commit squashed into target
# ✓ History is clean
```

### Example 2: Quick Fixup by Hash

```bash
# Stage fix
git add src/auth.js

# Create fixup
/git:fixup def5678

# Target commit: def5678 - Implement user authentication
# Staged changes: src/auth.js
#
# Create fixup commit? (y/n)
# User: y
#
# ✓ Created fixup commit
#
# To autosquash:
#   git rebase -i --autosquash def5678^
#
# Or run:
#   /git:fixup def5678 rebase
```

### Example 3: Multiple Fixups Before Rebase

```bash
# Found typo in commit abc1234
git add README.md
/git:fixup abc1234

# Later: Found bug in commit def5678
git add src/bug.js
/git:fixup def5678

# Later: Found another issue in abc1234
git add src/auth.js
/git:fixup abc1234

# Now have multiple fixup commits
git log --oneline
#   9999999 fixup! Implement user authentication (2nd fixup)
#   8888888 fixup! Add user model
#   7777777 fixup! Implement user authentication (1st fixup)
#   def5678 Add user model
#   abc1234 Implement user authentication
#   ...

# Rebase once to apply all fixups
/git:fixup rebase

# Result: All fixup commits squashed into targets
#   def5678 Add user model (updated)
#   abc1234 Implement user authentication (updated with both fixups)
```

### Example 4: Squash with Message

```bash
/git:fixup ghi9012 squash

# Target: ghi9012 - Implement user authentication
#
# Squash keeps commit message
# Enter additional message for squash commit:
# User: "Add rate limiting to prevent brute force attacks"
#
# ✓ Created squash commit
#   squash! Implement user authentication
#
# When rebased, both messages will be combined:
#   Implement user authentication
#
#   Add rate limiting to prevent brute force attacks
```

### Example 5: Amend HEAD

```bash
# Just made a commit, forgot a file
/git:fixup HEAD amend

# Or simpler:
/git:fixup amend

# Staged changes: src/forgotten-file.js
#
# Amend previous commit? (y/n)
# User: y
#
# ✓ Amended HEAD commit
# Previous: abc1234
# New: abc5678
#
# Note: Commit hash changed (rewritten)
```

### Example 6: Fixup with Interactive Staging

```bash
/git:fixup

# No staged changes
# Unstaged changes:
#   M  src/auth.js (5 hunks)
#   M  src/session.js (3 hunks)
#   M  tests/auth.test.js (2 hunks)
#
# Stage changes interactively? (y/n)
# User: y
#
# Opening interactive staging...
# [User selects specific hunks]
#
# Staged for fixup:
#   M  src/auth.js (2 hunks - bug fix)
#
# Target commit for fixup? (1-10)
# [User selects commit]
#
# ✓ Created fixup commit
```

## Advanced Usage

### Configure Autosquash Globally

```bash
# Enable autosquash for all repos
git config --global rebase.autosquash true

# Now git rebase -i automatically uses --autosquash
```

### Fixup Specific Lines Only

```bash
# Stage specific lines interactively
git add -p src/auth.js

# Select only the hunks that fix the bug
# Create fixup with just those changes
/git:fixup abc1234
```

### Fixup Chain

```bash
# Create fixup for a fixup (rare but possible)
git commit --fixup=fixup!<original-commit>

# Creates:
#   fixup! fixup! Original commit message

# All will squash into original during rebase
```

### Autosquash with Exec

```bash
# Run tests after each commit during autosquash
git rebase -i --autosquash --exec "npm test" origin/main

# Ensures each commit passes tests
# Useful for bisect-friendly history
```

### Fixup from Stash

```bash
# Have changes in stash
git stash show -p stash@{0}

# Apply and fixup
git stash pop
git add <files>
/git:fixup <target-commit>
```

## Workflow Integration

### With Pull Requests

```bash
# During code review, got feedback on specific commit
# Make fixes
git add <files>
git commit --fixup=<commit-from-pr>

# Before pushing PR update
git rebase -i --autosquash origin/main
git push --force-with-lease

# PR history is clean, reviewer sees clean commits
```

### With Feature Branch Development

```bash
# Day 1: Start feature
git commit -m "Add feature X"

# Day 2: Continue work
git commit -m "Add tests for feature X"

# Day 3: Found bug in day 1 commit
git add <fix>
git commit --fixup=<day-1-commit>

# Day 4: Ready to merge, clean up
git rebase -i --autosquash main
git push --force-with-lease

# Feature branch has clean history
```

### With Conventional Commits

```bash
# Original commit
git commit -m "feat: add user authentication"

# Later, found issue
git add <fix>
git commit --fixup=<feat-commit>

# After autosquash
# Result: "feat: add user authentication" (with fix included)
# Conventional commits format preserved
```

## Tips for Effective Fixup Usage

1. **Use fixup early and often:**
   - Don't wait until PR review
   - Fix issues as you find them
   - Keep commits clean from the start

2. **Stage precisely:**
   - Use `git add -p` for partial staging
   - Only include changes related to fixup
   - Don't mix unrelated fixes

3. **Descriptive staging messages:**
   - When staging, note what's being fixed
   - Helps remember why fixup was needed
   - Use `git add -v` for verbose output

4. **Batch fixups before rebase:**
   - Accumulate multiple fixup commits
   - Rebase once to apply all
   - More efficient than multiple rebases

5. **Test after autosquash:**
   - Run tests after rebase
   - Ensure fixups didn't break anything
   - Verify each commit builds (if possible)

6. **Enable autosquash globally:**
   - Set `rebase.autosquash = true`
   - Makes workflow smoother
   - Don't need --autosquash flag

## Related Commands

- `/git:rebase-interactive` - Manual rebase with full control
- `/git:cherry-pick-helper` - Alternative to fixup for specific changes
- `/git:branch-cleanup` - Clean up after merging fixed commits
- `/git:reflog-recover` - Recover from fixup/rebase mistakes

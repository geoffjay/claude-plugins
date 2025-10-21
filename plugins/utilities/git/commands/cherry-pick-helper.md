---
name: git:cherry-pick-helper
description: Guided cherry-pick workflow with conflict resolution assistance for selectively applying commits across branches
---

# Git Cherry-Pick Helper - Guided Commit Selection

Guided cherry-pick workflow with conflict resolution assistance for selectively applying commits across branches.

## Command

`/git:cherry-pick-helper <commit-ref> [additional-refs...]`

## Arguments

- `$1`: commit-ref - Commit hash or reference to cherry-pick (required)
- `$2+`: additional-refs - Additional commits to cherry-pick (optional, space-separated)

## Description

Cherry-picking allows you to apply specific commits from one branch to another without merging the entire branch. This is useful for backporting bug fixes, applying specific features, or selectively moving work between branches.

## When to Use Cherry-Pick

- Backport bug fix to release branch
- Apply hotfix from main to feature branch
- Move specific commits to different branch
- Recover commits from deleted branch
- Apply commits from someone else's branch
- Split work from one branch to multiple
- Test specific changes in isolation

## When NOT to Use Cherry-Pick

- Can merge entire branch (use merge instead)
- Commits depend on other commits not being picked
- Would create duplicate history (rebase better)
- On public/shared branches (coordinate with team)
- Just testing changes (use worktree or stash)

## Workflow

### Pre-Cherry-Pick Analysis

1. **Validate commit reference:**
   - Check commit exists
   - Verify commit is reachable
   - Can be from any branch or remote

2. **Show commit details:**
   ```bash
   git show --stat <commit-ref>
   ```

   Display:
   - Commit hash (full and short)
   - Author and date
   - Commit message
   - Files changed with stats
   - Number of insertions/deletions

3. **Analyze commit context:**
   - Show parent commits
   - Check if part of merge commit
   - Identify dependencies
   - Warn about potential issues

4. **Check current branch:**
   - Show current branch name
   - Verify branch is clean
   - Check for uncommitted changes
   - Show last commit on current branch

5. **Predict conflicts:**
   - Compare files in commit with current branch
   - Check if same files modified
   - Show potential conflict files
   - Estimate conflict probability

### Confirmation

6. **Show cherry-pick plan:**
   ```
   Cherry-Pick Plan:
   ========================================
   Target Branch: feature-auth
   Source Commit: abc1234 from main

   Commit Details:
   - Author: John Doe
   - Date: 2025-10-20
   - Message: Fix authentication token validation

   Files to Apply:
   - src/auth/token.js     (+15, -8)
   - src/auth/session.js   (+7, -3)
   - tests/auth/token.test.js (+45, -0)

   Potential Issues:
   ⚠ src/auth/token.js was modified in this branch
   ✓ Other files should apply cleanly

   Continue? (y/n/details)
   ```

7. **Offer options:**
   - Proceed with cherry-pick
   - Show detailed diff first
   - Show file-by-file changes
   - Cancel operation

### Execute Cherry-Pick

8. **Perform cherry-pick:**
   ```bash
   git cherry-pick <commit-ref>
   ```

9. **For multiple commits:**
   ```bash
   git cherry-pick <ref1> <ref2> <ref3>
   ```

   Or range:
   ```bash
   git cherry-pick <start-ref>^..<end-ref>
   ```

10. **Monitor progress:**
    - Show which commit being applied
    - Display progress for multiple picks
    - Real-time status updates

### Success Case

11. **If cherry-pick succeeds:**
    - Show new commit hash
    - Display commit message
    - Show files changed
    - Verify commit applied correctly

12. **Post-pick verification:**
    - Show git log with new commit
    - Display branch status
    - Suggest running tests
    - Offer to cherry-pick more commits

### Conflict Resolution

13. **If conflicts occur:**
    - Stop cherry-pick process
    - List conflicted files
    - Show conflict markers
    - Explain current state

14. **For each conflicted file:**
    - Show conflict details:
      ```bash
      git diff <file>
      ```
    - Explain conflict sections:
      - `<<<<<<< HEAD` - Current branch changes
      - `=======` - Separator
      - `>>>>>>> <commit>` - Cherry-picked changes
    - Show full file context

15. **Resolution options:**
    - Manually edit files
    - Accept theirs (cherry-picked version)
    - Accept ours (current version)
    - Use merge tool
    - Abort cherry-pick

16. **Guide through resolution:**
    ```
    Conflict Resolution:
    ========================================
    File: src/auth/token.js

    Conflict:
    <<<<<<< HEAD
    function validateToken(token) {
      return checkSignature(token);
    }
    =======
    function validateToken(token) {
      return checkSignature(token) && !isExpired(token);
    }
    >>>>>>> abc1234 Fix authentication token validation

    Options:
    1. Edit manually
    2. Accept cherry-picked version (includes expiry check)
    3. Accept current version (no expiry check)
    4. Show more context
    5. Use merge tool

    Choice: 2

    Accepting cherry-picked version...
    ```

17. **After resolving each file:**
    - Stage resolved file
    - Show remaining conflicts
    - Continue when all resolved

18. **Complete cherry-pick:**
    ```bash
    git add <resolved-files>
    git cherry-pick --continue
    ```

### Abort or Skip

19. **Abort cherry-pick:**
    ```bash
    git cherry-pick --abort
    ```
    - Returns to state before cherry-pick
    - No changes applied
    - Safe to retry

20. **Skip commit:**
    ```bash
    git cherry-pick --skip
    ```
    - Skip current commit
    - Continue with remaining commits
    - Use when commit not needed

### Multiple Commits

21. **For cherry-pick sequence:**
    - Apply commits in order
    - Pause at conflicts
    - Resume after resolution
    - Track progress through list

22. **Show sequence progress:**
    ```
    Cherry-Pick Sequence:
    ========================================
    Total: 5 commits
    Progress: 3/5

    ✓ abc1234 - Fix token validation
    ✓ def5678 - Add session timeout
    → ghi9012 - Update user model [CONFLICT]
    ⋯ jkl3456 - Add tests
    ⋯ mno7890 - Update docs

    Current: ghi9012
    Resolve conflicts then continue
    ```

## Safety Checks

### Before Cherry-Pick

- **Clean working directory:**
  ```bash
  if [ -n "$(git status --porcelain)" ]; then
    echo "Error: Working directory has uncommitted changes"
    echo ""
    git status --short
    echo ""
    echo "Cherry-pick requires clean working directory"
    echo "Options:"
    echo "  1. Commit changes: git commit"
    echo "  2. Stash changes: git stash"
    echo "  3. Discard changes: git restore ."
    exit 1
  fi
  ```

- **Commit exists:**
  ```bash
  if ! git cat-file -e "$commit_ref" 2>/dev/null; then
    echo "Error: Commit not found: $commit_ref"
    echo ""
    echo "Make sure commit exists in repository"
    echo "Try:"
    echo "  git fetch --all  # Update remote branches"
    echo "  git log --all --oneline | grep <search>"
    exit 1
  fi
  ```

- **Not a merge commit:**
  ```bash
  parent_count=$(git rev-list --parents -n1 "$commit_ref" | wc -w)
  if [ $parent_count -gt 2 ]; then
    echo "Warning: This is a merge commit"
    echo "Merge commits: $(($parent_count - 1)) parents"
    echo ""
    echo "Cherry-picking merge commits is complex"
    echo "You must specify which parent to use:"
    echo "  git cherry-pick -m 1 $commit_ref  # Use first parent"
    echo "  git cherry-pick -m 2 $commit_ref  # Use second parent"
    echo ""
    echo "Continue anyway? (y/n)"
    read confirm
    [ "$confirm" != "y" ] && exit 0
  fi
  ```

- **Commit not already applied:**
  ```bash
  # Check if commit already in current branch
  if git log --format=%H | grep -q "$(git rev-parse $commit_ref)"; then
    echo "Warning: This commit already exists in current branch"
    echo "Commit: $commit_ref"
    echo ""
    echo "Cherry-picking will create duplicate commit"
    echo "Continue? (y/n)"
    read confirm
    [ "$confirm" != "y" ] && exit 0
  fi
  ```

### During Cherry-Pick

- **Conflict detection:**
  ```bash
  if git cherry-pick "$commit_ref" 2>&1 | grep -q "CONFLICT"; then
    echo "Conflict detected!"
    echo ""
    echo "Conflicted files:"
    git diff --name-only --diff-filter=U
    echo ""
    echo "Use cherry-pick helper to resolve"
    # Enter conflict resolution mode
  fi
  ```

- **Cherry-pick in progress:**
  ```bash
  if [ -f ".git/CHERRY_PICK_HEAD" ]; then
    echo "Cherry-pick in progress"
    echo ""
    echo "Status:"
    git status
    echo ""
    echo "Options:"
    echo "  1. Continue: Resolve conflicts and git cherry-pick --continue"
    echo "  2. Abort: git cherry-pick --abort"
    echo "  3. Skip: git cherry-pick --skip"
    exit 1
  fi
  ```

### After Cherry-Pick

- **Verify changes:**
  ```bash
  echo "Cherry-pick complete!"
  echo ""
  echo "New commit: $(git rev-parse HEAD)"
  echo "Original commit: $commit_ref"
  echo ""
  echo "Verify changes:"
  git show --stat HEAD
  echo ""
  echo "Test your changes before pushing"
  ```

- **Check for semantic conflicts:**
  ```bash
  echo "⚠ Cherry-pick succeeded, but..."
  echo "Check for semantic conflicts:"
  echo "  - Function signatures changed?"
  echo "  - Dependencies missing?"
  echo "  - Tests still pass?"
  echo ""
  echo "Run tests:"
  echo "  npm test"
  echo "  pytest"
  echo "  cargo test"
  ```

## Error Handling

### Commit Not Found

```bash
if ! git cat-file -e "$commit_ref" 2>/dev/null; then
  echo "Error: Commit not found: $commit_ref"
  echo ""
  echo "Possible reasons:"
  echo "  - Typo in commit hash"
  echo "  - Commit in different repository"
  echo "  - Need to fetch from remote"
  echo ""
  echo "Try:"
  echo "  git fetch --all"
  echo "  git log --all --oneline | grep <keyword>"
  exit 1
fi
```

### Cherry-Pick Failed

```bash
if ! git cherry-pick "$commit_ref"; then
  error_type=$(git status | grep -o "both modified\|deleted by\|added by")

  case "$error_type" in
    "both modified")
      echo "Conflict: File modified in both branches"
      ;;
    "deleted by")
      echo "Conflict: File deleted in one branch, modified in other"
      ;;
    "added by")
      echo "Conflict: File added with different content"
      ;;
  esac

  echo ""
  echo "Resolution needed for:"
  git diff --name-only --diff-filter=U
  exit 1
fi
```

### Empty Cherry-Pick

```bash
if git cherry-pick "$commit_ref" 2>&1 | grep -q "nothing to commit"; then
  echo "Cherry-pick resulted in no changes"
  echo ""
  echo "This means:"
  echo "  - Changes already exist in current branch"
  echo "  - Commit was effectively empty"
  echo "  - Changes were already reverted"
  echo ""
  echo "Options:"
  echo "  1. Skip: git cherry-pick --skip"
  echo "  2. Abort: git cherry-pick --abort"
  exit 1
fi
```

## Examples

### Example 1: Cherry-Pick Single Commit

```bash
/git:cherry-pick-helper abc1234

# Analyzing commit abc1234...
#
# Commit Details:
# ========================================
# Hash: abc1234567890abcdef
# Author: John Doe <john@example.com>
# Date: Mon Oct 16 14:30:00 2025 -0700
# Branch: main
#
# Message:
#   Fix authentication token validation bug
#
#   Added expiry check to prevent expired tokens
#   from being accepted.
#
# Files Changed (3):
#   src/auth/token.js          | 15 ++++++++----
#   src/auth/session.js        |  7 +++--
#   tests/auth/token.test.js   | 45 +++++++++++++++++++++++++++++++
#
# Current Branch: feature-auth
# Last Commit: def5678 Implement OAuth
#
# Conflict Check:
# ⚠ Potential conflict: src/auth/token.js
#   (modified in both branches)
# ✓ Other files should apply cleanly
#
# Proceed with cherry-pick? (y/n/details)
# User: y
#
# Cherry-picking abc1234...
# Conflict in src/auth/token.js
#
# [Enters conflict resolution mode]
# ...
# [After resolution]
#
# ✓ Cherry-pick complete!
# New commit: xyz9876
# Changes applied to feature-auth branch
```

### Example 2: Cherry-Pick Multiple Commits

```bash
/git:cherry-pick-helper abc1234 def5678 ghi9012

# Cherry-Pick Sequence:
# ========================================
# 3 commits to apply
#
# 1. abc1234 - Fix token validation
# 2. def5678 - Add session timeout
# 3. ghi9012 - Update user model
#
# Source: main
# Target: feature-auth (current)
#
# Proceed? (y/n)
# User: y
#
# [1/3] Cherry-picking abc1234...
# ✓ Success (commit: aaa1111)
#
# [2/3] Cherry-picking def5678...
# ✓ Success (commit: bbb2222)
#
# [3/3] Cherry-picking ghi9012...
# ⚠ Conflict in src/models/user.js
#
# Resolve conflict and continue? (y/abort)
# User: y
#
# [Shows conflict resolution UI]
# ...
# [After resolution]
#
# ✓ All commits cherry-picked successfully!
# Applied 3 commits to feature-auth
```

### Example 3: Cherry-Pick Range

```bash
/git:cherry-pick-helper abc1234^..def5678

# Cherry-Pick Range:
# ========================================
# From: abc1234 (inclusive)
# To: def5678 (inclusive)
# Count: 8 commits
#
# Commits:
#   abc1234 - Fix token validation
#   bcd2345 - Add session timeout
#   cde3456 - Update user model
#   def4567 - Add password reset
#   efg5678 - Implement 2FA
#   fgh6789 - Add audit logging
#   ghi7890 - Update dependencies
#   def5678 - Add tests
#
# Apply all 8 commits? (y/n/select)
# User: select
#
# Select commits to cherry-pick (1-8, comma separated):
# User: 1,2,4,5
#
# Will cherry-pick:
#   abc1234 - Fix token validation
#   bcd2345 - Add session timeout
#   def4567 - Add password reset
#   efg5678 - Implement 2FA
#
# Proceed? (y/n)
# User: y
#
# [Applies selected commits...]
```

### Example 4: Conflict Resolution

```bash
/git:cherry-pick-helper abc1234

# ...
# Conflict in src/auth/token.js
#
# ========================================
# Conflict Resolution Helper
# ========================================
#
# File: src/auth/token.js
# Conflict type: Both modified
#
# Your version (HEAD):
# ----------------------------------------
# function validateToken(token) {
#   if (!token) return false;
#   return checkSignature(token);
# }
#
# Cherry-picked version (abc1234):
# ----------------------------------------
# function validateToken(token) {
#   if (!token) return false;
#   return checkSignature(token) && !isExpired(token);
# }
#
# What changed:
# + Added expiry check: !isExpired(token)
#
# Options:
# 1. Accept cherry-picked version (includes expiry check)
# 2. Accept current version (no expiry check)
# 3. Edit manually
# 4. Show full file context
# 5. Abort cherry-pick
#
# Choice: 1
#
# Accepting cherry-picked version...
# ✓ File resolved
#
# All conflicts resolved
# Continuing cherry-pick...
# ✓ Complete!
```

### Example 5: Cherry-Pick from Remote Branch

```bash
# Fetch latest
git fetch origin

# Cherry-pick from remote
/git:cherry-pick-helper origin/hotfix/security-patch

# Notice: This is a branch reference
# Will cherry-pick the tip of: origin/hotfix/security-patch
#
# Commit: abc1234 (HEAD of origin/hotfix/security-patch)
# Message: Fix XSS vulnerability in user input
#
# Proceed? (y/n)
# User: y
#
# ✓ Cherry-picked to current branch
```

## Advanced Usage

### Cherry-Pick Without Commit

```bash
# Apply changes but don't commit
git cherry-pick -n <commit>

# Or: --no-commit
git cherry-pick --no-commit <commit>

# Useful for:
# - Modifying changes before committing
# - Combining multiple cherry-picks
# - Testing changes first
```

### Cherry-Pick Merge Commit

```bash
# Specify which parent to use
git cherry-pick -m 1 <merge-commit>

# -m 1: Use first parent (usually main branch)
# -m 2: Use second parent (usually feature branch)
```

### Cherry-Pick with Modified Message

```bash
# Edit commit message during cherry-pick
git cherry-pick -e <commit>

# Or: --edit
git cherry-pick --edit <commit>

# Useful for:
# - Adding context about cherry-pick
# - Changing references (ticket numbers)
# - Adding "cherry-picked from" note
```

### Cherry-Pick Specific Files Only

```bash
# Cherry-pick changes to specific files only
git show <commit>:<file> > <file>
git add <file>
git commit -m "Cherry-picked changes from <commit>"

# Or more elegantly:
git checkout <commit> -- <file>
git commit -m "Cherry-picked <file> from <commit>"
```

### Interactive Cherry-Pick

```bash
# Cherry-pick with interactive conflict resolution
git cherry-pick <commit>
# If conflict:
git mergetool  # Opens configured merge tool
git cherry-pick --continue
```

## Tips for Effective Cherry-Picking

1. **Understand commit dependencies:**
   - Check if commit depends on previous commits
   - May need to cherry-pick multiple commits
   - Review commit history before picking

2. **Test after cherry-pick:**
   - Always run tests
   - Check for semantic conflicts
   - Verify functionality works

3. **Update commit message:**
   - Note that commit was cherry-picked
   - Update references (ticket numbers)
   - Add context for target branch

4. **Avoid cherry-pick for:**
   - Large features (use merge)
   - Long commit sequences (use rebase)
   - Entire branches (use merge)

5. **Team coordination:**
   - Communicate cherry-picks to team
   - Document in PR/commit message
   - Update tracking systems

6. **Cherry-pick vs Merge:**
   - Cherry-pick: Select specific commits
   - Merge: Bring entire branch history
   - Choose based on need

## Related Commands

- `/git:reflog-recover` - Recover from cherry-pick mistakes
- `/git:rebase-interactive` - Alternative for moving commits
- `/git:branch-cleanup` - Clean up after cherry-picking
- `/git:fixup` - Fix commits before cherry-picking

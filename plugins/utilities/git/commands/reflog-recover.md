---
name: git:reflog-recover
description: Use reflog to recover lost commits, deleted branches, and resolve repository mistakes
---

# Git Reflog Recover - Lost Commit and Branch Recovery

Use reflog to recover lost commits, deleted branches, and resolve repository mistakes.

## Command

`/git:reflog-recover [search-term] [action]`

## Arguments

- `$1`: search-term - Text to search in reflog (optional, shows recent reflog if omitted)
- `$2`: action - `show|recover|create-branch` (default: `show`)

## Description

Git's reflog (reference log) tracks every change to branch tips and HEAD, even changes that "lose" commits like hard resets, branch deletions, or rebases. The reflog is your safety net for recovering from mistakes, finding lost work, and understanding repository history.

## What is Reflog?

The reflog records:
- Every commit
- Branch switches
- Resets (soft, mixed, hard)
- Rebases
- Merges
- Amends
- Cherry-picks
- Branch deletions
- Any HEAD movement

Each entry shows:
- Commit hash
- Previous HEAD position
- Action performed
- When it happened

**Important:** Reflog entries expire after ~90 days by default. Recovery is not possible after expiration.

## When to Use Reflog Recovery

- Accidentally deleted a branch
- Did `git reset --hard` and lost commits
- Messed up rebase and want to undo
- Amended commit but want old version
- Lost commits after force-push
- Want to see what you were working on
- Need to understand what happened
- Recover from any git mistake

## What Can Be Recovered

**Can Recover:**
- Committed changes (within ~90 days)
- Deleted branches (if committed)
- Reset commits
- Rebased commits (old versions)
- Amended commits (previous versions)
- Cherry-picked commits (originals)

**Cannot Recover:**
- Uncommitted changes (never committed)
- Changes that were never staged
- Expired reflog entries (>90 days old)
- Changes from other users' local repos

## Workflow

### Show Reflog

1. **Display recent reflog:**
   ```bash
   git reflog show
   ```

   Or with limits:
   ```bash
   git reflog show -n 50
   ```

2. **Format reflog entries:**
   - Show commit hash (short and full)
   - Show reflog reference (HEAD@{n})
   - Show action performed
   - Show relative time (5 minutes ago, 2 days ago)
   - Show commit message

   ```
   Reflog Entries (Recent 30):
   ========================================
   HEAD@{0}  abc1234  commit: Add new feature
             (5 minutes ago)

   HEAD@{1}  def5678  checkout: moving from main to feature-branch
             (2 hours ago)

   HEAD@{2}  ghi9012  reset: moving to HEAD^
             (3 hours ago) ⚠ RESET - Potential lost commits

   HEAD@{3}  jkl3456  commit (amend): Fix typo in commit message
             (5 hours ago) ⚠ AMEND - Previous version available

   HEAD@{4}  mno7890  rebase -i (finish): refs/heads/feature
             (1 day ago) ⚠ REBASE - Old commits available
   ```

3. **Highlight important entries:**
   - Resets (potential lost work)
   - Branch deletions
   - Rebases (old history)
   - Amends (previous versions)
   - Force updates

4. **Categorize by action type:**
   - Commits
   - Checkouts (branch switches)
   - Resets
   - Rebases
   - Merges
   - Amendments
   - Cherry-picks

### Search Reflog

5. **Search by term:**
   ```bash
   git reflog | grep "<search-term>"
   ```

6. **Common searches:**
   - Branch name: Find when branch was deleted
   - Commit message keyword: Find specific work
   - Date/time: Find what happened when
   - Action type: Find all resets, rebases, etc.

7. **Show search results:**
   - Matching entries highlighted
   - Context before/after (adjacent entries)
   - Grouped by relevance
   - Sorted by time

### Recover Commits

8. **Select recovery target:**
   - User picks reflog entry
   - Show full commit details
   - Show what will be recovered
   - Explain recovery options

9. **Recovery options:**

   **Option A: Create new branch**
   ```bash
   git branch recovery-branch <commit-hash>
   ```
   - Safest option
   - Preserves current state
   - Can review before merging
   - Recommended for most cases

   **Option B: Reset current branch**
   ```bash
   git reset --hard <commit-hash>
   ```
   - Moves current branch
   - Loses commits after target
   - Use with caution
   - Create backup branch first

   **Option C: Cherry-pick commit**
   ```bash
   git cherry-pick <commit-hash>
   ```
   - Apply specific commit
   - Keep current history
   - Good for selective recovery

   **Option D: Merge recovered commit**
   ```bash
   git branch temp-recovery <commit-hash>
   git merge temp-recovery
   ```
   - Merge lost work
   - Preserves both histories
   - Creates merge commit

10. **Execute recovery:**
    - Perform chosen action
    - Verify recovery successful
    - Show resulting state
    - Offer to continue recovering

### Create Branch from Reflog

11. **Branch creation workflow:**
    - Ask for commit hash from reflog
    - Validate commit exists
    - Ask for branch name
    - Create branch at commit
    - Offer to switch to branch

12. **Execute:**
    ```bash
    git branch <new-branch-name> <commit-hash>
    ```

13. **Verify:**
    - Show branch created
    - Show commit it points to
    - Show how to access it
    - Offer to checkout

### Show Specific Commit

14. **Display lost commit:**
    ```bash
    git show <commit-hash>
    ```

15. **Show details:**
    - Full commit message
    - Author and date
    - Files changed
    - Full diff
    - Parent commits

16. **Actions after showing:**
    - Offer to recover
    - Create branch
    - Cherry-pick
    - Export as patch
    - Copy hash to clipboard

### Understand History

17. **Timeline visualization:**
    - Show reflog as timeline
    - Highlight branch points
    - Show where mistakes happened
    - Trace commit lineage

18. **Before/After comparison:**
    - Show state before mistake
    - Show state after mistake
    - Show what was lost
    - Show recovery path

## Safety Checks

### Before Recovery

- **Verify commit exists:**
  ```bash
  if ! git cat-file -e "$commit_hash" 2>/dev/null; then
    echo "Error: Commit not found: $commit_hash"
    echo "It may have been garbage collected"
    echo "Try: git fsck --lost-found"
    exit 1
  fi
  ```

- **Check current state:**
  ```bash
  if [ -n "$(git status --porcelain)" ]; then
    echo "Warning: You have uncommitted changes"
    git status --short
    echo ""
    echo "Recovery operations may affect these changes"
    echo "Commit or stash them first? (y/n/continue)"
  fi
  ```

- **Create backup:**
  ```bash
  current_branch=$(git branch --show-current)
  backup_branch="backup-${current_branch}-$(date +%s)"
  git branch "$backup_branch"

  echo "Created backup branch: $backup_branch"
  echo "To restore current state: git reset --hard $backup_branch"
  ```

### During Recovery

- **Confirm destructive operations:**
  ```bash
  if [ "$action" = "reset" ]; then
    echo "⚠ WARNING: git reset --hard is DESTRUCTIVE"
    echo ""
    echo "This will:"
    echo "  - Move current branch to: $commit_hash"
    echo "  - Discard all commits after target"
    echo "  - Lose uncommitted changes"
    echo ""
    echo "Backup created: $backup_branch"
    echo ""
    echo "Type 'RESET' to confirm: "
    read confirmation
    [ "$confirmation" != "RESET" ] && exit 0
  fi
  ```

- **Verify commit is reachable:**
  ```bash
  # Check commit is in reflog
  if ! git reflog | grep -q "$commit_hash"; then
    echo "Notice: Commit not in current branch's reflog"
    echo "It may be from another branch or remote"
    echo "Continue? (y/n)"
  fi
  ```

### After Recovery

- **Verify recovery:**
  ```bash
  echo "Recovery complete!"
  echo ""
  echo "Verification:"
  echo "  Recovered commit: $commit_hash"
  echo "  Current HEAD: $(git rev-parse HEAD)"
  echo "  Current branch: $(git branch --show-current)"
  echo ""
  echo "Check recovered work:"
  git show --stat HEAD
  echo ""
  echo "Run tests to verify everything works"
  ```

- **Cleanup suggestion:**
  ```bash
  echo ""
  echo "After verifying recovery:"
  echo "  - Delete backup branch if not needed:"
  echo "    git branch -d $backup_branch"
  echo "  - Push if needed:"
  echo "    git push --force-with-lease"
  ```

## Error Handling

### Commit Not Found

```bash
if ! git cat-file -e "$commit_hash" 2>/dev/null; then
  echo "Error: Commit not found in repository"
  echo "Commit: $commit_hash"
  echo ""
  echo "Possible reasons:"
  echo "  - Commit was garbage collected (>90 days old)"
  echo "  - Typo in commit hash"
  echo "  - Commit in different repository"
  echo ""
  echo "Try these recovery methods:"
  echo "  1. Check reflog: git reflog show --all"
  echo "  2. Search all refs: git log --all --oneline | grep <message>"
  echo "  3. Find dangling commits: git fsck --lost-found"
  exit 1
fi
```

### Reflog Expired

```bash
# Check if reflog exists
if [ ! -f ".git/logs/HEAD" ]; then
  echo "Error: No reflog found"
  echo ""
  echo "Possible reasons:"
  echo "  - Fresh clone (reflog not transferred)"
  echo "  - Reflog disabled in config"
  echo "  - Repository corruption"
  echo ""
  echo "Recovery may not be possible"
  exit 1
fi

# Check reflog age
oldest_entry=$(git reflog show | tail -1)
echo "Oldest reflog entry: $oldest_entry"
echo ""
echo "Reflog entries older than ~90 days are garbage collected"
echo "If your lost work is older, recovery may not be possible"
```

### Branch Creation Failed

```bash
if git branch "$new_branch" "$commit_hash" 2>&1 | grep -q "already exists"; then
  echo "Error: Branch already exists: $new_branch"
  echo ""
  echo "Options:"
  echo "  1. Choose different name"
  echo "  2. Delete existing branch: git branch -D $new_branch"
  echo "  3. Reset existing branch: git branch -f $new_branch $commit_hash"
  exit 1
fi
```

### Reset Failed

```bash
if ! git reset --hard "$commit_hash" 2>&1; then
  echo "Error: Reset failed"
  echo ""
  echo "Your repository state was not changed"
  echo "Check: git status"
  echo ""
  echo "If you have backup branch:"
  echo "  git reset --hard $backup_branch"
  exit 1
fi
```

## Examples

### Example 1: View Recent Reflog

```bash
/git:reflog-recover

# Reflog Entries (Recent 30):
# ========================================
#
# HEAD@{0}  abc1234  5 minutes ago
#   commit: Add user authentication
#
# HEAD@{1}  def5678  2 hours ago
#   checkout: moving from main to feature-auth
#
# HEAD@{2}  ghi9012  3 hours ago
#   reset: moving to HEAD^
#   ⚠ RESET - Commits may be lost
#
# HEAD@{3}  jkl3456  3 hours ago
#   commit: Fix token validation
#   [This commit was reset away!]
#
# HEAD@{4}  mno7890  5 hours ago
#   commit (amend): Update README
#   ⚠ AMEND - Previous version at HEAD@{5}
#
# HEAD@{5}  pqr3456  5 hours ago
#   commit: Update README
#   [Original version before amend]
#
# ...
#
# Actions:
# [r] Recover specific entry
# [s] Search reflog
# [q] Quit
```

### Example 2: Recover from Accidental Reset

```bash
# Situation: Accidentally did git reset --hard HEAD^
# Lost last commit!

/git:reflog-recover

# Looking at reflog:
# HEAD@{0}  def5678  reset: moving to HEAD^  (just now)
# HEAD@{1}  abc1234  commit: Important feature  (5 min ago) ← Lost!

# Select entry to recover: HEAD@{1}
# User: 1
#
# Commit Details:
# ========================================
# Hash: abc1234567890abcdef
# Message: Important feature
# Author: John Doe
# Date: 2025-10-21 14:30:00
#
# Files Changed:
#   src/feature.js | 45 +++++++++++++++++++++++++
#   tests/feature.test.js | 23 +++++++++++++
#
# Recovery Options:
# 1. Create branch (safest)
# 2. Reset current branch (restore state)
# 3. Cherry-pick commit
# 4. Show more details
#
# Choice: 2
#
# ⚠ This will reset current branch
# Backup created: backup-main-1729534567
# Type 'RESET' to confirm: RESET
#
# Resetting to abc1234...
# ✓ Recovery complete!
#
# You are now at: Important feature
# Lost commit is recovered!
```

### Example 3: Find and Recover Deleted Branch

```bash
/git:reflog-recover "deleted branch" show

# Searching reflog for: "deleted branch"
#
# Found 2 matches:
# ========================================
#
# HEAD@{15}  def5678  2 days ago
#   Branch: delete branch feature-x
#   Last commit on feature-x: "Add feature X"
#
# HEAD@{145}  abc1234  2 months ago
#   Branch: delete branch old-experiment
#   Last commit: "Experimental changes"
#
# Recover which entry? (1-2, or 'all')
# User: 1
#
# Recovering branch: feature-x
# Last commit: def5678 "Add feature X"
#
# New branch name? (default: feature-x)
# User: feature-x-recovered
#
# Creating branch...
# ✓ Created branch: feature-x-recovered at def5678
#
# To use recovered branch:
#   git checkout feature-x-recovered
#
# Switch now? (y/n)
# User: y
#
# ✓ Switched to branch 'feature-x-recovered'
# Your deleted branch is recovered!
```

### Example 4: Undo Bad Rebase

```bash
# Situation: Rebase went wrong, conflicts everywhere
# Want to undo entire rebase

/git:reflog-recover rebase

# Searching for: rebase
#
# Found rebase operations:
# ========================================
#
# HEAD@{0}  abc9999  rebase (finish): refs/heads/feature
#   (5 minutes ago) ← Bad rebase!
#
# HEAD@{1}  def8888  rebase (continue): Add feature Y
#   (7 minutes ago)
#
# HEAD@{2}  ghi7777  rebase (start): checkout main
#   (10 minutes ago)
#
# HEAD@{3}  jkl6666  commit: Add feature Y
#   (15 minutes ago) ← Before rebase started
#
# Recover to before rebase? (entry 3)
# User: y
#
# This will restore branch to: jkl6666
# Before rebase started
#
# Recovery method:
# 1. Reset branch (undo rebase)
# 2. Create new branch (keep both)
#
# Choice: 1
#
# Creating backup: backup-feature-1729534567
# Resetting to jkl6666...
# ✓ Rebase undone!
#
# You are back to state before rebase
# Original commits preserved
```

### Example 5: Find Lost Work by Keyword

```bash
/git:reflog-recover "authentication" show

# Searching for: "authentication"
#
# Found 8 entries with "authentication":
# ========================================
#
# HEAD@{3}  abc1234  3 hours ago
#   commit: Add user authentication
#
# HEAD@{12}  def5678  1 day ago
#   commit: Fix authentication bug
#
# HEAD@{25}  ghi9012  3 days ago
#   commit: Update authentication flow
#
# HEAD@{45}  jkl3456  1 week ago
#   commit: Implement OAuth authentication
#
# ...
#
# Show details for which entry? (number or 'all')
# User: 3
#
# Commit: ghi9012
# ========================================
# Message: Update authentication flow
# Author: Jane Smith
# Date: 2025-10-18 10:15:00
#
# Changes:
#   src/auth/flow.js | 67 ++++++++++++++++++++++++++++++++
#   src/auth/middleware.js | 34 +++++++++++++---
#
# [Shows full diff]
#
# Actions:
# [b] Create branch from this commit
# [c] Cherry-pick to current branch
# [p] Export as patch
# [q] Back to list
```

### Example 6: Recover Amended Commit

```bash
# Situation: Amended commit but want original version

/git:reflog-recover "amend"

# Searching for: amend
#
# Found amendments:
# ========================================
#
# HEAD@{0}  abc9999  commit (amend): Fix typo in docs
#   (2 minutes ago) ← New version
#
# HEAD@{1}  abc1234  commit: Fix typo in docs
#   (5 minutes ago) ← Original version before amend
#
# Compare versions? (y/n)
# User: y
#
# Differences between versions:
# ========================================
# Original (abc1234):
#   Fixed typo in README
#   [Shows original diff]
#
# Amended (abc9999):
#   Fixed typo in README and CONTRIBUTING
#   [Shows amended diff]
#
# Recover original version?
# 1. Create branch with original
# 2. Reset to original (lose amendment)
# 3. Keep amended version
#
# Choice: 1
#
# Branch name: pre-amend-version
# ✓ Created branch with original version
```

## Advanced Usage

### Find Dangling Commits

```bash
# Find commits not in any branch (beyond reflog)
git fsck --lost-found

# Shows unreachable commits
# More aggressive than reflog
# Can find very old lost commits
```

### Export Reflog

```bash
# Save reflog to file
git reflog show > reflog-backup-$(date +%Y%m%d).txt

# Useful before dangerous operations
# Can review later if needed
```

### Reflog for Specific Branch

```bash
# View reflog for specific branch
git reflog show feature-branch

# See all changes to that branch
# Not just HEAD movements
```

### Reflog with Dates

```bash
# Show reflog with exact dates
git reflog show --date=iso

# Or relative dates
git reflog show --date=relative

# Find what happened at specific time
git reflog show HEAD@{2025-10-21.14:30:00}
```

### Expire Reflog Manually

```bash
# Expire reflog entries older than X
git reflog expire --expire=30.days --all

# Aggressive cleanup
git reflog expire --expire=now --all
git gc --prune=now

# Only do if sure!
```

## Tips for Using Reflog

1. **Act quickly:**
   - Reflog expires after ~90 days
   - Recover as soon as you notice mistake
   - Don't wait

2. **Check reflog before dangerous operations:**
   - Before reset --hard
   - Before rebase
   - Before force-push
   - Know you can undo

3. **Search effectively:**
   - Use keywords from commit messages
   - Search by branch names
   - Look for operation types (reset, rebase)

4. **Create branches, don't reset:**
   - Safest recovery method
   - Can review before deciding
   - Preserves current state

5. **Regular reflog backups:**
   - Export reflog periodically
   - Especially before risky operations
   - Extra safety net

6. **Understand reflog vs garbage collection:**
   - Reflog keeps references
   - Prevents garbage collection
   - After expiry, commits can be GC'd

## Related Commands

- `/git:branch-cleanup` - Clean up recovered branches
- `/git:cherry-pick-helper` - Apply recovered commits
- `/git:bisect` - Find bugs in recovered history
- `/git:worktree` - Test recovered commits safely

---
name: git:stash-manager
description: Advanced stash management including list, save, apply, pop, and organize stashes with detailed context.
---

# Git Stash Manager - Advanced Stash Operations

Advanced stash management including list, save, apply, pop, and organize stashes with detailed context.

## Command

`/git:stash-manager <action> [stash-ref-or-message]`

## Arguments

- `$1`: action - `list|save|apply|pop|show|drop|clear|branch` (required)
- `$2`: stash-ref or message - Depends on action (stash@{n} for apply/pop/show/drop, message for save)

## Description

Git stash allows you to save uncommitted changes temporarily and restore them later. This is useful when you need to switch contexts, pull updates, or try experimental changes without committing. The stash manager provides an organized way to manage multiple stashes with better visibility and control.

## Use Cases

- Switch branches without committing work-in-progress
- Pull latest changes with uncommitted local changes
- Try experimental changes with easy rollback
- Temporarily remove changes to test something
- Save different variations of work
- Transfer changes between branches
- Context switching during interruptions

## Workflow

### Listing Stashes

1. **Display all stashes:**
   ```bash
   git stash list
   ```

2. **Enhanced listing with details:**
   - Show stash index and message
   - Show branch where stash was created
   - Show date/time of stash creation
   - Show which files are affected
   - Show summary of changes (additions/deletions)
   - Highlight recent stashes (< 24 hours)

3. **For each stash show:**
   ```
   stash@{0}: On feature-auth: WIP authentication module
     Branch: feature-auth
     Created: 2 hours ago (2025-10-21 14:30:15)
     Files: 3 modified, 1 added
       M  src/auth.js (+45, -12)
       M  src/session.js (+23, -5)
       A  src/token.js (+67)
     Size: ~135 lines changed
   ```

4. **Interactive options:**
   - Show diff for specific stash
   - Apply or pop stash
   - Delete stash
   - Create branch from stash
   - Export stash as patch file

### Saving Stashes

5. **Gather stash options:**
   - Ask for descriptive message (required)
   - Ask if including untracked files (`-u`)
   - Ask if including ignored files (`-a`, all)
   - Ask if keeping staged changes (`--keep-index`)
   - Ask if including path-specific changes

6. **Create stash with options:**

   Basic stash:
   ```bash
   git stash push -m "message"
   ```

   With untracked files:
   ```bash
   git stash push -u -m "message"
   ```

   Keep staged changes:
   ```bash
   git stash push --keep-index -m "message"
   ```

   Specific paths only:
   ```bash
   git stash push -m "message" -- path/to/file path/to/dir
   ```

7. **Confirm stash created:**
   - Show stash reference (stash@{0})
   - Show what was stashed
   - Show current status
   - Offer to show stash diff

### Applying Stashes

8. **Select stash to apply:**
   - If no stash-ref provided, show list
   - Ask user to select by number or reference
   - Show stash details before applying
   - Warn if stash is from different branch

9. **Pre-apply checks:**
   - Check for uncommitted changes (warn about merge)
   - Check for conflicts with stash
   - Dry-run to predict conflicts
   - Show which files will be modified

10. **Apply stash:**
    ```bash
    git stash apply stash@{n}
    ```

    Or with index restoration:
    ```bash
    git stash apply --index stash@{n}
    ```

11. **Handle conflicts:**
    - If conflicts occur, show conflicted files
    - Guide through resolution
    - Offer to abort (stash remains in list)
    - After resolution, stash remains in list

12. **Confirm application:**
    - Show what was applied
    - Note that stash still exists (use pop to remove)
    - Show current status

### Popping Stashes

13. **Pop vs Apply:**
    - Explain difference: pop removes stash after applying
    - Confirm user wants to remove stash
    - Recommend apply if unsure

14. **Pop stash:**
    ```bash
    git stash pop stash@{n}
    ```

15. **On success:**
    - Stash is removed from list
    - Changes applied to working directory
    - Show updated status

16. **On conflict:**
    - Changes partially applied
    - Stash is NOT removed
    - Must resolve conflicts manually
    - Can abort with `git reset --hard`

### Showing Stash Details

17. **Display stash content:**
    ```bash
    git stash show -p stash@{n}
    ```

18. **Show comprehensive details:**
    - Commit information
    - Full diff of changes
    - Summary statistics
    - List of affected files
    - Branch context

19. **Interactive options:**
    - View file-by-file
    - Show only specific files
    - Compare with current working directory
    - Apply/pop after viewing

### Dropping Stashes

20. **Confirm deletion:**
    - Show stash details before dropping
    - Warn that drop is permanent
    - Require explicit confirmation
    - Offer to save as patch file first

21. **Drop stash:**
    ```bash
    git stash drop stash@{n}
    ```

22. **Recovery note:**
    - Explain dropped stashes can be recovered (briefly)
    - Mention reflog recovery within ~90 days
    - Show recover command hint

### Clearing All Stashes

23. **Warning prompt:**
    - Show count of stashes to be deleted
    - List all stashes briefly
    - Warn this is permanent
    - Require typing "yes" to confirm

24. **Clear all stashes:**
    ```bash
    git stash clear
    ```

25. **Confirmation:**
    - Confirm all stashes cleared
    - Note that recovery may be possible via reflog
    - Show clean stash list

### Creating Branch from Stash

26. **Create branch with stash:**
    - Useful when stash has conflicts with current branch
    - Ask for new branch name
    - Create branch and apply stash

27. **Execute:**
    ```bash
    git stash branch <branch-name> stash@{n}
    ```

28. **Result:**
    - New branch created from commit where stash was created
    - Stash applied to new branch
    - Stash removed from list
    - Switched to new branch

## Safety Checks

### Before Saving Stash

- **Nothing to stash:**
  ```bash
  if [ -z "$(git status --porcelain)" ]; then
    echo "Error: No changes to stash"
    echo "Working directory is clean"
    exit 1
  fi
  ```

- **Descriptive message required:**
  ```bash
  if [ -z "$message" ] || [ "$message" = "WIP" ]; then
    echo "Please provide a descriptive stash message"
    echo "Bad: 'WIP', 'temp', 'stuff'"
    echo "Good: 'WIP: authentication refactor', 'Debug logging for issue #123'"
    # Ask for better message
  fi
  ```

- **Untracked files warning:**
  ```bash
  untracked_count=$(git ls-files --others --exclude-standard | wc -l)
  if [ $untracked_count -gt 0 ]; then
    echo "Warning: $untracked_count untracked file(s) detected"
    echo "Include untracked files in stash? (y/n)"
    echo "Use -u flag to include them"
  fi
  ```

### Before Applying/Popping

- **Uncommitted changes warning:**
  ```bash
  if [ -n "$(git status --porcelain)" ]; then
    echo "Warning: You have uncommitted changes"
    echo "Applying stash may cause conflicts"
    echo ""
    git status --short
    echo ""
    echo "Options:"
    echo "  1. Continue anyway (may conflict)"
    echo "  2. Commit current changes first"
    echo "  3. Stash current changes first (nested stash)"
    echo "  4. Cancel"
  fi
  ```

- **Stash reference validation:**
  ```bash
  if ! git rev-parse --verify "$stash_ref" >/dev/null 2>&1; then
    echo "Error: Invalid stash reference: $stash_ref"
    echo ""
    echo "Available stashes:"
    git stash list
    echo ""
    echo "Use: stash@{0}, stash@{1}, etc."
    exit 1
  fi
  ```

- **Branch mismatch warning:**
  ```bash
  stash_branch=$(git stash list | grep "$stash_ref" | sed 's/.*On \([^:]*\):.*/\1/')
  current_branch=$(git branch --show-current)

  if [ "$stash_branch" != "$current_branch" ]; then
    echo "Notice: Stash created on different branch"
    echo "  Stash from: $stash_branch"
    echo "  Current: $current_branch"
    echo ""
    echo "This may cause conflicts. Continue? (y/n)"
  fi
  ```

- **Conflict prediction:**
  ```bash
  # Dry-run to check for conflicts
  if ! git apply --check $(git stash show -p $stash_ref) 2>/dev/null; then
    echo "Warning: This stash may have conflicts"
    echo "Files that may conflict:"
    # Show potentially conflicting files
    echo ""
    echo "Continue? (y/n)"
  fi
  ```

### Before Dropping/Clearing

- **Confirmation required:**
  ```bash
  echo "About to drop stash: $stash_ref"
  git stash show --stat $stash_ref
  echo ""
  echo "This cannot be undone easily!"
  echo "Type 'yes' to confirm: "
  read confirmation

  if [ "$confirmation" != "yes" ]; then
    echo "Drop cancelled"
    exit 0
  fi
  ```

- **Offer patch export:**
  ```bash
  echo "Save this stash as a patch file first? (y/n)"
  read save_patch

  if [ "$save_patch" = "y" ]; then
    patch_file="stash-$(date +%s).patch"
    git stash show -p $stash_ref > "$patch_file"
    echo "Saved to: $patch_file"
  fi
  ```

### After Operations

- **Verify application:**
  ```bash
  echo "Stash applied. Verifying..."
  echo ""
  echo "Changed files:"
  git status --short
  echo ""
  echo "Run tests to verify everything works:"
  echo "  npm test"
  echo "  pytest"
  echo "  cargo test"
  ```

## Error Handling

### No Stashes Exist

```bash
if [ -z "$(git stash list)" ]; then
  echo "No stashes found"
  echo ""
  echo "Create a stash with:"
  echo "  /git:stash-manager save 'description'"
  echo ""
  echo "Or directly:"
  echo "  git stash push -m 'description'"
  exit 1
fi
```

### Apply/Pop Conflicts

```bash
# When git stash apply/pop fails with conflicts
if [ $? -ne 0 ]; then
  echo "Conflict occurred while applying stash!"
  echo ""
  echo "Conflicted files:"
  git diff --name-only --diff-filter=U
  echo ""
  echo "Options:"
  echo "  1. Resolve conflicts manually:"
  echo "     - Edit conflicted files"
  echo "     - git add <file> (after resolving)"
  echo "  2. Abort changes:"
  echo "     git reset --hard HEAD"
  echo "  3. Try applying to different branch:"
  echo "     /git:stash-manager branch new-branch-name"
  echo ""
  echo "Note: For pop, stash was NOT removed due to conflict"
  exit 1
fi
```

### Invalid Stash Reference

```bash
if ! git stash list | grep -q "^$stash_ref:"; then
  echo "Error: Stash not found: $stash_ref"
  echo ""
  echo "Available stashes:"
  git stash list | nl -v 0
  echo ""
  echo "Note: stash@{0} is most recent"
  exit 1
fi
```

### Stash Apply to Dirty Directory

```bash
if [ -n "$(git status --porcelain)" ]; then
  echo "Warning: Working directory has uncommitted changes"
  echo ""
  git status --short
  echo ""
  echo "Applying stash on top of these changes may cause issues"
  echo ""
  echo "Recommended: "
  echo "  1. Commit current changes, or"
  echo "  2. Stash current changes first (nested stash), or"
  echo "  3. Use a worktree: /git:worktree"
  echo ""
  echo "Force apply anyway? (y/n)"
  read force
  [ "$force" != "y" ] && exit 0
fi
```

## Examples

### Example 1: Save Stash with Description

```bash
/git:stash-manager save "WIP: implementing OAuth authentication"

# Include untracked files? (y/n)
# User: y
#
# Keep staged changes in working directory? (y/n)
# User: n
#
# Saved working directory and index state:
#   stash@{0}: On feature-auth: WIP: implementing OAuth authentication
#
# Stashed:
#   3 modified files
#   2 new files (untracked)
#   Total: ~127 lines changed
#
# Working directory is now clean
```

### Example 2: List Stashes with Details

```bash
/git:stash-manager list

# ========================================
# Git Stashes (3)
# ========================================
#
# stash@{0}: On feature-auth: WIP: implementing OAuth authentication
#   Branch: feature-auth
#   Created: 2 hours ago (2025-10-21 14:30:15)
#   Files: 3 modified, 2 added
#     M  src/auth/oauth.js (+45, -12)
#     M  src/auth/session.js (+23, -5)
#     A  src/auth/tokens.js (+67)
#     A  tests/auth/oauth.test.js (+89)
#
# stash@{1}: On main: Fix styling issues on mobile
#   Branch: main
#   Created: 1 day ago (2025-10-20 09:15:42)
#   Files: 5 modified
#     M  src/styles/mobile.css (+34, -18)
#     M  src/components/Header.js (+12, -8)
#     ...
#
# stash@{2}: On feature-ui: Experimental layout changes
#   Branch: feature-ui
#   Created: 3 days ago (2025-10-18 16:45:00)
#   Files: 8 modified, 1 deleted
#     ...
#
# Actions: [s]how, [a]pply, [p]op, [d]rop, [q]uit
```

### Example 3: Apply Stash with Conflicts

```bash
/git:stash-manager apply stash@{0}

# Applying stash@{0}...
#   On feature-auth: WIP: implementing OAuth authentication
#
# Warning: You are on a different branch
#   Stash from: feature-auth
#   Current: main
#
# This may cause conflicts. Continue? (y/n)
# User: y
#
# Applying...
# Conflict in src/auth/oauth.js
# Conflict in src/auth/session.js
#
# Conflicted files:
#   src/auth/oauth.js
#   src/auth/session.js
#
# Please resolve conflicts:
#   1. Edit files to resolve <<<< ==== >>>> markers
#   2. Test your changes
#   3. Stage resolved files: git add <file>
#
# Or abort:
#   git reset --hard HEAD
#
# Note: Stash still exists (not removed)
```

### Example 4: Pop Most Recent Stash

```bash
/git:stash-manager pop

# Most recent stash:
#   stash@{0}: On feature-auth: WIP: implementing OAuth authentication
#   3 files modified, 2 files added
#
# Apply and remove this stash? (y/n)
# User: y
#
# Applying stash@{0}...
# Success!
#
# Changed files:
#   M  src/auth/oauth.js
#   M  src/auth/session.js
#   M  src/auth/tokens.js
#   A  tests/auth/oauth.test.js
#   A  tests/auth/tokens.test.js
#
# Stash removed from list
# Current status: 5 files modified
```

### Example 5: Show Stash Details

```bash
/git:stash-manager show stash@{1}

# ========================================
# Stash: stash@{1}
# ========================================
# Message: Fix styling issues on mobile
# Branch: main
# Created: 1 day ago (2025-10-20 09:15:42)
# Author: John Doe <john@example.com>
#
# Files Changed (5):
# ========================================
# src/styles/mobile.css | 52 ++++++++++++++++++++++-----------
# src/components/Header.js | 20 ++++++------
# src/components/Nav.js | 15 ++++++---
# src/components/Footer.js | 8 ++---
# src/index.css | 3 +-
#
# Diff:
# ========================================
# [Shows full diff output...]
#
# Actions:
#   [a] Apply this stash
#   [p] Pop this stash
#   [d] Drop this stash
#   [b] Create branch from stash
#   [q] Back to list
```

### Example 6: Drop Specific Stash

```bash
/git:stash-manager drop stash@{2}

# About to drop:
#   stash@{2}: On feature-ui: Experimental layout changes
#   Created: 3 days ago
#   8 files modified, 1 file deleted
#
# This cannot be easily undone!
#
# Save as patch file first? (y/n)
# User: y
#
# Saved to: stash-1729534567.patch
#
# Type 'yes' to confirm deletion:
# User: yes
#
# Dropped stash@{2}
# Recovery may be possible via reflog:
#   git fsck --unreachable | grep commit
```

### Example 7: Clear All Stashes

```bash
/git:stash-manager clear

# WARNING: About to delete ALL stashes!
#
# Current stashes (3):
#   stash@{0}: WIP: implementing OAuth authentication
#   stash@{1}: Fix styling issues on mobile
#   stash@{2}: Experimental layout changes
#
# This action is PERMANENT!
#
# Type 'DELETE ALL' to confirm:
# User: DELETE ALL
#
# Cleared all stashes
# Stash list is now empty
#
# Note: Recovery may be possible within 90 days via reflog
```

### Example 8: Create Branch from Stash

```bash
/git:stash-manager branch experimental-auth stash@{0}

# Creating branch from stash...
#   Branch: experimental-auth
#   Based on commit where stash was created
#   Stash: stash@{0}: WIP: implementing OAuth authentication
#
# Created branch 'experimental-auth'
# Switched to branch 'experimental-auth'
# Applied stash changes
# Dropped stash@{0}
#
# Your changes are now on branch: experimental-auth
# Status: 5 files modified
```

## Advanced Usage

### Partial Stash (Specific Files)

```bash
# Stash only specific files
/git:stash-manager save "WIP: auth module only"

# Which files to stash?
# User: src/auth/*.js tests/auth/*.js

# Command:
git stash push -m "WIP: auth module only" -- src/auth/*.js tests/auth/*.js
```

### Interactive Stash

```bash
# Stash with interactive staging
git stash push -p -m "Selected changes only"

# Prompts for each hunk: stage this hunk? y/n
```

### Stash to Patch File

```bash
# Export stash as patch
git stash show -p stash@{0} > my-changes.patch

# Later, apply patch
git apply my-changes.patch

# Or:
patch -p1 < my-changes.patch
```

### View Stash as Commit

```bash
# Each stash is actually a commit
git show stash@{0}

# View stash log
git log --oneline --graph stash@{0}

# Stash has 3 parents:
# 1. HEAD when stash was created
# 2. Index state
# 3. Untracked files (if -u used)
```

## Tips for Effective Stash Usage

1. **Descriptive messages:**
   - Bad: "WIP", "temp", "stuff"
   - Good: "WIP: OAuth integration", "Debug: issue #123", "Experiment: new layout"
   - Include ticket numbers, feature names, or context

2. **Keep stashes short-lived:**
   - Don't use stash as long-term storage
   - Apply or pop within a day or two
   - For longer storage, commit to a branch

3. **One stash at a time (usually):**
   - Multiple stashes get confusing
   - Apply/pop before creating new ones
   - Use worktrees for parallel work instead

4. **Include untracked files:**
   - Use `-u` flag when saving
   - Prevents forgetting about new files
   - Makes stash more complete

5. **Branch strategy:**
   - If stash has conflicts, create branch
   - Better than fighting conflicts
   - Can merge branch later

## Related Commands

- `/git:worktree` - Better than stash for parallel work
- `/git:branch-cleanup` - Clean up branches created from stashes
- `/git:cherry-pick-helper` - Apply specific commits instead of stash
- `/git:reflog-recover` - Recover dropped stashes

---
name: git:worktree
description: Manage multiple working trees for parallel development, testing, and code review without branch switching overhead.
---

# Git Worktree - Multiple Working Trees Management

Manage multiple working trees for parallel development, testing, and code review without branch switching overhead.

## Command

`/git:worktree <action> [path] [branch-name]`

## Arguments

- `$1`: action - `add|list|remove|prune|lock|unlock` (required)
- `$2`: path - Directory path for the worktree (required for add/remove)
- `$3`: branch-name - Branch to checkout in worktree (optional for add)

## Description

Git worktrees allow you to have multiple working directories from the same repository, each with different branches checked out. This eliminates the need to stash changes, switch branches, and potentially deal with conflicts when you need to work on multiple features simultaneously or review code while keeping your current work intact.

## Use Cases

- Work on multiple features simultaneously
- Review pull requests without interrupting current work
- Run tests on one branch while developing on another
- Compare code between branches side-by-side
- Keep a clean build directory separate from development
- Emergency hotfixes without stashing current work

## Workflow

### Adding a New Worktree

1. **Validate input:**
   - Check path doesn't already exist
   - Check path is not inside current repository
   - Validate branch name if provided
   - Check for branch conflicts

2. **Gather information:**
   - Ask for target path (relative or absolute)
   - Ask for branch name (or generate from feature name)
   - Ask if creating new branch or checking out existing
   - Optionally ask for starting point (commit/branch to base on)

3. **Create worktree:**

   For new branch:
   ```bash
   git worktree add -b <new-branch> <path> <starting-point>
   ```

   For existing branch:
   ```bash
   git worktree add <path> <existing-branch>
   ```

   Create worktree and checkout:
   ```bash
   git worktree add <path>
   # Creates new branch from HEAD
   ```

4. **Post-creation:**
   - Confirm worktree created successfully
   - Display worktree information
   - Show path, branch, and commit
   - Offer to change directory to new worktree
   - Suggest next steps (cd command, IDE instructions)

### Listing Worktrees

5. **Display all worktrees:**
   - Show main working tree
   - Show all linked worktrees
   - For each worktree show:
     - Path (absolute)
     - Branch name
     - Commit hash and message
     - Status (clean/modified/locked)
     - Whether it's the current worktree

6. **Enhanced listing:**
   ```bash
   git worktree list --porcelain
   ```

   Parse and display:
   - Which worktree is current (*)
   - Uncommitted changes indicator
   - Days since last commit
   - Locked status with reason

7. **Interactive options:**
   - Offer to show details for specific worktree
   - Option to remove stale worktrees
   - Option to navigate to worktree
   - Show disk usage per worktree

### Removing a Worktree

8. **Pre-removal checks:**
   - Verify worktree exists
   - Check if it's the current worktree (can't remove)
   - Check for uncommitted changes
   - Check for unpushed commits
   - Warn about any issues

9. **Confirm removal:**
   - Show worktree details
   - Show what will be lost
   - Ask for explicit confirmation
   - Option to force remove if locked

10. **Remove worktree:**
    ```bash
    git worktree remove <path>
    ```

    Or force removal:
    ```bash
    git worktree remove --force <path>
    ```

11. **Post-removal:**
    - Confirm removal successful
    - Note that branch still exists (unless deleted)
    - Offer to delete branch if fully merged
    - Show updated worktree list

### Pruning Stale Worktrees

12. **Find stale entries:**
    - Worktree directories that no longer exist
    - Locked worktrees that can be cleaned
    - Administrative data that can be pruned

13. **Show what will be pruned:**
    ```bash
    git worktree prune --dry-run
    ```

14. **Prune stale entries:**
    ```bash
    git worktree prune
    ```

15. **Confirm results:**
    - Show what was pruned
    - Display updated worktree list

### Lock/Unlock Worktrees

16. **Lock worktree:**
    - Prevent accidental removal
    - Useful for worktrees on removable media
    - Add reason for lock
    ```bash
    git worktree lock --reason "Testing environment" <path>
    ```

17. **Unlock worktree:**
    ```bash
    git worktree unlock <path>
    ```

## Safety Checks

### Before Adding

- **Path validation:**
  ```bash
  # Check path doesn't exist
  if [ -e "$path" ]; then
    echo "Error: Path already exists: $path"
    echo "Choose a different path or remove existing directory"
    exit 1
  fi

  # Check path is not inside repository
  if [[ "$path" == "$(git rev-parse --show-toplevel)"* ]]; then
    echo "Warning: Creating worktree inside repository"
    echo "This is unusual. Continue? (y/n)"
    # Wait for confirmation
  fi
  ```

- **Branch validation:**
  ```bash
  # Check if branch exists
  if git show-ref --verify --quiet refs/heads/$branch; then
    # Branch exists
    # Check if already checked out in another worktree
    if git worktree list | grep -q "$branch"; then
      echo "Error: Branch '$branch' is already checked out in another worktree"
      echo "A branch can only be checked out in one worktree at a time"
      exit 1
    fi
  fi
  ```

- **Disk space check:**
  ```bash
  # Check available disk space
  available=$(df "$target_dir" | awk 'NR==2 {print $4}')
  repo_size=$(du -s "$(git rev-parse --show-toplevel)" | awk '{print $1}')

  if [ $available -lt $repo_size ]; then
    echo "Warning: Low disk space"
    echo "Available: ${available}K"
    echo "Repository size: ${repo_size}K"
    echo "Continue? (y/n)"
  fi
  ```

### Before Removing

- **Uncommitted changes check:**
  ```bash
  cd "$worktree_path"
  if [ -n "$(git status --porcelain)" ]; then
    echo "Warning: Worktree has uncommitted changes:"
    git status --short
    echo ""
    echo "Options:"
    echo "  1. Cancel removal"
    echo "  2. Force remove (lose changes)"
    echo "  3. Show me the changes first"
    # Wait for user choice
  fi
  ```

- **Unpushed commits check:**
  ```bash
  unpushed=$(git log --oneline @{u}.. 2>/dev/null | wc -l)
  if [ $unpushed -gt 0 ]; then
    echo "Warning: Worktree has $unpushed unpushed commit(s):"
    git log --oneline @{u}..
    echo ""
    echo "These commits will NOT be lost (branch still exists)"
    echo "But you may want to push them first."
    echo "Continue with removal? (y/n)"
  fi
  ```

- **Current worktree check:**
  ```bash
  current_worktree=$(git worktree list --porcelain | grep "$(pwd)" | head -1)
  if [ -n "$current_worktree" ]; then
    echo "Error: Cannot remove current worktree"
    echo "Please cd to a different directory first"
    exit 1
  fi
  ```

- **Locked worktree check:**
  ```bash
  if git worktree list --porcelain | grep -A5 "worktree $path" | grep -q "locked"; then
    reason=$(git worktree list --porcelain | grep -A5 "worktree $path" | grep "locked" | cut -d' ' -f2-)
    echo "Warning: Worktree is locked"
    echo "Reason: $reason"
    echo ""
    echo "Options:"
    echo "  1. Cancel removal"
    echo "  2. Unlock and remove"
    echo "  3. Force remove (keep lock reason for reference)"
  fi
  ```

### During Prune

- **Dry-run first:**
  ```bash
  echo "Finding stale worktrees..."
  git worktree prune --dry-run --verbose
  echo ""
  echo "Proceed with pruning? (y/n)"
  ```

## Error Handling

### Path Already Exists

```bash
if [ -e "$path" ]; then
  echo "Error: Path already exists: $path"

  # Check if it's an old worktree directory
  if [ -f "$path/.git" ]; then
    content=$(cat "$path/.git")
    if [[ $content == gitdir:* ]]; then
      echo "This appears to be an orphaned worktree directory"
      echo "Options:"
      echo "  1. Remove directory and create new worktree"
      echo "  2. Try to repair worktree link"
      echo "  3. Choose different path"
    fi
  fi
  exit 1
fi
```

### Branch Already Checked Out

```bash
if git worktree list | grep -q " \[$branch\]"; then
  existing_path=$(git worktree list | grep " \[$branch\]" | awk '{print $1}')
  echo "Error: Branch '$branch' is already checked out"
  echo "Location: $existing_path"
  echo ""
  echo "A branch can only be checked out in one worktree at a time."
  echo "Options:"
  echo "  1. Use a different branch name"
  echo "  2. Remove the existing worktree first"
  echo "  3. Navigate to existing worktree: cd $existing_path"
  exit 1
fi
```

### Worktree Not Found

```bash
if ! git worktree list | grep -q "$path"; then
  echo "Error: No worktree found at: $path"
  echo ""
  echo "Available worktrees:"
  git worktree list
  echo ""
  echo "Note: Path must match exactly as shown above"
  exit 1
fi
```

### Cannot Remove Main Worktree

```bash
main_worktree=$(git worktree list | head -1 | awk '{print $1}')
if [ "$path" = "$main_worktree" ]; then
  echo "Error: Cannot remove main worktree"
  echo "The main worktree is the original repository directory"
  echo "You can only remove linked worktrees created with 'git worktree add'"
  exit 1
fi
```

## Examples

### Example 1: Add Worktree for Feature Development

```bash
# Interactive mode
/git:worktree add

# Claude prompts:
# "Where should the new worktree be created?"
# User: "../feature-auth"
#
# "What branch should be checked out?"
# User: "feature/oauth-integration"
#
# "This branch doesn't exist. Create new branch? (y/n)"
# User: "y"
#
# "What should the new branch be based on? (default: HEAD)"
# User: "main"

# Result:
# Created worktree at: /Users/geoff/Projects/feature-auth
# Branch: feature/oauth-integration (new)
# Based on: main
#
# To start working:
#   cd ../feature-auth
```

### Example 2: Direct Add Command

```bash
# Add worktree with new branch
/git:worktree add ../feature-x feature/new-feature

# Add worktree for existing branch
/git:worktree add ../bugfix bugfix/issue-123

# Add worktree with detached HEAD at specific commit
/git:worktree add ../review abc1234
```

### Example 3: List All Worktrees

```bash
/git:worktree list

# Output:
# ========================================
# Git Worktrees
# ========================================
#
# * /Users/geoff/Projects/my-repo (main) [current]
#   └─ Clean • Last commit: 2 hours ago
#
#   /Users/geoff/Projects/feature-auth (feature/oauth-integration)
#   └─ Modified (3 files) • Last commit: 5 minutes ago
#
#   /Users/geoff/Projects/hotfix (hotfix/security-patch)
#   └─ Clean • Last commit: 2 days ago • LOCKED
#
#   /Users/geoff/Projects/review (abc1234) [detached]
#   └─ Clean • Last commit: 1 week ago
#
# Total: 4 worktrees
```

### Example 4: Remove Worktree

```bash
/git:worktree remove ../feature-x

# Claude checks and prompts:
# "Worktree at ../feature-x has uncommitted changes:"
#   M  src/auth.js
#   A  src/session.js
#
# "What would you like to do?"
#   1. Cancel removal
#   2. Show me the changes
#   3. Force remove (changes will be lost)
#
# User choice: 2
#
# [Shows git diff output]
#
# "Still want to remove? (y/n)"
# User: "n"
#
# "Removal cancelled. You might want to:"
#   - cd ../feature-x
#   - Commit your changes
#   - Or: git stash in that worktree
```

### Example 5: Prune Stale Worktrees

```bash
/git:worktree prune

# Output:
# Finding stale worktrees...
#
# Would prune:
#   - /Users/geoff/Projects/old-feature (directory removed)
#   - /Volumes/USB/temp-worktree (volume unmounted)
#
# Proceed with pruning? (y/n)
# User: y
#
# Pruned 2 stale worktree entries
#
# Updated worktree list:
# [shows current worktrees]
```

## Advanced Usage

### Worktree for PR Review

```bash
# Fetch PR branch
git fetch origin pull/123/head:pr-123

# Create worktree for review
/git:worktree add ../pr-review pr-123

# Review in separate directory
cd ../pr-review
# Run tests, review code, test changes
```

### Worktree for Release Builds

```bash
# Create locked worktree for clean builds
/git:worktree add ../build-release release-v1.0
cd ../build-release

# Lock it to prevent accidental removal
git worktree lock --reason "Production build environment"

# Build
npm run build:production
```

### Worktree for Bisect

```bash
# Create worktree for git bisect without affecting main work
/git:worktree add ../bisect-search main
cd ../bisect-search
git bisect start HEAD v1.0.0
# Run bisect without interrupting main development
```

### Multiple Feature Worktrees

```bash
# Main repo: ongoing development
cd /Users/geoff/Projects/my-repo

# Feature 1: new auth system
/git:worktree add ../auth-feature feature/oauth

# Feature 2: UI redesign
/git:worktree add ../ui-feature feature/new-ui

# Hotfix: security patch
/git:worktree add ../hotfix hotfix/cve-2025-1234

# PR review
/git:worktree add ../pr-456 pr-456

# Now work on any without switching branches in main repo
```

## Tips for Effective Worktree Usage

1. **Organize worktree locations:**
   - Keep worktrees in a dedicated parent directory
   - Use descriptive directory names
   - Example structure:
     ```
     ~/Projects/
       my-repo/           # Main worktree
       my-repo-features/  # Feature worktrees
         auth/
         ui-redesign/
         api-v2/
     ```

2. **Naming conventions:**
   - Use branch names as directory names for clarity
   - Prefix with purpose: `review-`, `feature-`, `hotfix-`
   - Keep names short but descriptive

3. **Clean up regularly:**
   - Remove worktrees when done with feature
   - Run prune periodically
   - Don't let worktrees accumulate

4. **IDE considerations:**
   - Open each worktree as separate project/window
   - Be aware of shared config (.git directory)
   - Watch for file watchers across worktrees

5. **Branch management:**
   - Remember: one branch per worktree
   - Can't checkout same branch in multiple worktrees
   - Delete branches after removing worktrees (if merged)

## Related Commands

- `/git:branch-cleanup` - Clean up branches from removed worktrees
- `/git:stash-manager` - Not needed with worktrees (no branch switching)
- `/git:bisect` - Use worktrees to bisect without interrupting work
- `/git:cherry-pick-helper` - Cherry-pick between worktrees

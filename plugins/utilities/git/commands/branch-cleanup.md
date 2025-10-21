---
name: git:branch-cleanup
description: Clean up merged and stale branches locally and remotely with comprehensive safety checks
---

# Git Branch Cleanup - Merged and Stale Branch Management

Clean up merged and stale branches locally and remotely with comprehensive safety checks.

## Command

`/git:branch-cleanup [scope] [base-branch]`

## Arguments

- `$1`: scope - `local|remote|both` (default: `local`)
- `$2`: base-branch - Branch to check merges against (default: `main` or `master`)

## Description

Over time, repositories accumulate branches from completed features, merged pull requests, and abandoned work. Branch cleanup helps maintain repository hygiene by identifying and safely removing branches that are no longer needed, while protecting active and important branches.

## Use Cases

- Clean up after merged pull requests
- Remove abandoned feature branches
- Prepare repository for new work
- Reduce clutter in branch listings
- Find stale branches that need attention
- Audit branch activity across team
- Free up branch names for reuse

## Branch Categories

Branches are classified into categories:

1. **Fully Merged** - Safe to delete
   - All commits are in base branch
   - Feature complete and merged
   - No unique changes

2. **Partially Merged** - Review before delete
   - Some commits merged
   - May have additional work
   - Requires investigation

3. **Stale** - No activity for long period
   - No commits in 90+ days
   - May be abandoned
   - Should be reviewed before delete

4. **Active** - Recent activity
   - Commits within last 30 days
   - Likely still in use
   - Should not be deleted

5. **Protected** - Never delete
   - main, master, develop
   - production, staging
   - release branches
   - Explicitly configured protected branches

## Workflow

### Initial Analysis

1. **Identify base branch:**
   - Check for main or master
   - Use user-specified branch if provided
   - Validate base branch exists

2. **Gather branch information:**
   ```bash
   # List all branches
   git branch -a

   # For each branch, get:
   # - Last commit date
   # - Last author
   # - Commit count ahead/behind
   # - Merge status
   ```

3. **Categorize branches:**
   - Sort into categories (merged, stale, active, protected)
   - Calculate statistics for each category
   - Prepare summary report

4. **Show summary:**
   ```
   Branch Cleanup Analysis
   ==================================================
   Base branch: main
   Scope: local branches

   Categories:
     Fully merged:     12 branches
     Stale (90+ days): 5 branches
     Active (<30 days): 8 branches
     Protected:        3 branches (will not delete)

   Total branches: 28
   Safe to delete: 12 branches
   ```

### Local Branch Cleanup

5. **List fully merged branches:**
   ```bash
   git branch --merged <base-branch>
   ```

6. **For each merged branch show:**
   - Branch name
   - Last commit date
   - Last author
   - Commit message
   - Days since last commit

7. **Exclude protected branches:**
   - main, master
   - develop, development
   - staging, production
   - release/*, hotfix/*
   - Current branch

8. **Show deletion plan:**
   ```
   Fully Merged Branches (12):
   ==================================================
   1. feature/user-auth
      Last: 2025-09-15 (36 days ago)
      By: John Doe
      "Add JWT authentication"

   2. bugfix/login-error
      Last: 2025-08-30 (52 days ago)
      By: Jane Smith
      "Fix login redirect issue"

   ...
   ```

9. **Ask for confirmation:**
   - Show dry-run option
   - Allow individual selection
   - Allow batch selection
   - Offer to skip

10. **Delete local branches:**
    ```bash
    git branch -d <branch-name>
    ```

    Or force delete if needed:
    ```bash
    git branch -D <branch-name>
    ```

### Stale Branch Handling

11. **Identify stale branches:**
    ```bash
    # Branches with no commits in 90+ days
    git for-each-ref --sort=-committerdate refs/heads/
    ```

12. **Show stale branches:**
    - Branch name
    - Last commit date (days ago)
    - Last author
    - Merged status
    - Commit count unique to branch

13. **For each stale branch:**
    - Show details
    - Check if merged (even if old)
    - Check for unique commits
    - Ask user for action:
      - Delete (if safe)
      - Keep (still needed)
      - Review (show more details)

### Remote Branch Cleanup

14. **Analyze remote branches:**
    ```bash
    git branch -r --merged <base-branch>
    ```

15. **Cross-reference with local:**
    - Remote branches without local counterpart
    - Remote branches that are merged
    - Remote branches that are stale

16. **Show remote deletion plan:**
    - More cautious than local
    - Double-check merge status
    - Verify no open pull requests
    - Confirm team coordination

17. **Delete remote branches:**
    ```bash
    git push origin --delete <branch-name>
    ```

18. **Prune remote tracking branches:**
    ```bash
    git fetch --prune
    git remote prune origin
    ```

### Post-Cleanup

19. **Show cleanup summary:**
    - Branches deleted (count and names)
    - Branches skipped
    - Branches protected
    - Space saved (if measurable)

20. **Verify repository state:**
    - Show remaining branches
    - Verify no unintended deletions
    - Check current branch still exists

21. **Offer additional actions:**
    - Push cleanup to remote
    - Archive deleted branches (tags)
    - Export branch list before deletion
    - Clean up remote tracking branches

## Safety Checks

### Before Any Deletion

- **Protected branches list:**
  ```bash
  PROTECTED_BRANCHES=(
    "main"
    "master"
    "develop"
    "development"
    "staging"
    "production"
    "release"
  )

  for protected in "${PROTECTED_BRANCHES[@]}"; do
    if [[ "$branch" == "$protected" ]] || [[ "$branch" == "$protected"/* ]]; then
      echo "Skipping protected branch: $branch"
      continue
    fi
  done
  ```

- **Current branch check:**
  ```bash
  current_branch=$(git branch --show-current)
  if [ "$branch" = "$current_branch" ]; then
    echo "Error: Cannot delete current branch: $branch"
    echo "Switch to a different branch first"
    exit 1
  fi
  ```

- **Base branch check:**
  ```bash
  if [ "$branch" = "$base_branch" ]; then
    echo "Error: Cannot delete base branch: $base_branch"
    echo "This is the branch we're comparing against!"
    exit 1
  fi
  ```

### Local Branch Deletion

- **Merged status verification:**
  ```bash
  if git branch --merged $base_branch | grep -q "^[* ] $branch$"; then
    echo "✓ Branch is fully merged into $base_branch"
    merge_status="safe"
  else
    echo "⚠ Branch is NOT fully merged"
    unmerged_commits=$(git log $base_branch..$branch --oneline | wc -l)
    echo "  $unmerged_commits unique commit(s) will be lost"
    echo ""
    echo "Show commits? (y/n)"
    # If yes: git log $base_branch..$branch
    merge_status="unsafe"
  fi
  ```

- **Force delete confirmation:**
  ```bash
  if [ "$merge_status" = "unsafe" ]; then
    echo "Branch '$branch' has unmerged commits!"
    echo "Force delete will PERMANENTLY lose these commits"
    echo ""
    git log --oneline $base_branch..$branch
    echo ""
    echo "Type 'DELETE' to force delete: "
    read confirmation
    [ "$confirmation" != "DELETE" ] && continue

    # Use -D instead of -d
    git branch -D $branch
  fi
  ```

### Remote Branch Deletion

- **Remote reference check:**
  ```bash
  if ! git ls-remote --heads origin $branch | grep -q $branch; then
    echo "Branch '$branch' does not exist on remote"
    continue
  fi
  ```

- **Pull request check:**
  ```bash
  # If GitHub CLI available
  if command -v gh &> /dev/null; then
    pr_count=$(gh pr list --head $branch --json number --jq 'length')
    if [ $pr_count -gt 0 ]; then
      echo "Warning: Branch '$branch' has open pull request(s)"
      echo "View: gh pr view --web"
      echo ""
      echo "Delete anyway? (y/n)"
      read confirm
      [ "$confirm" != "y" ] && continue
    fi
  fi
  ```

- **Team coordination warning:**
  ```bash
  echo "⚠ REMOTE DELETION WARNING"
  echo "You are about to delete remote branch: origin/$branch"
  echo ""
  echo "This affects other developers if they:"
  echo "  - Have this branch checked out"
  echo "  - Have based work on this branch"
  echo "  - Have unpushed commits on this branch"
  echo ""
  echo "Have you coordinated with your team? (y/n)"
  read coordinated
  [ "$coordinated" != "y" ] && continue
  ```

### Batch Deletion Safety

- **Dry-run mode:**
  ```bash
  echo "DRY-RUN MODE"
  echo "Would delete these branches:"
  for branch in "${branches_to_delete[@]}"; do
    echo "  - $branch"
  done
  echo ""
  echo "Proceed with actual deletion? (y/n)"
  ```

- **Confirmation for bulk delete:**
  ```bash
  if [ ${#branches_to_delete[@]} -gt 5 ]; then
    echo "About to delete ${#branches_to_delete[@]} branches"
    echo "This is a bulk operation!"
    echo ""
    echo "Type 'CONFIRM BULK DELETE' to proceed: "
    read confirmation
    [ "$confirmation" != "CONFIRM BULK DELETE" ] && exit 0
  fi
  ```

## Error Handling

### Branch Not Fully Merged

```bash
if ! git branch -d $branch 2>&1; then
  error=$(git branch -d $branch 2>&1)
  if echo "$error" | grep -q "not fully merged"; then
    echo "Error: Branch '$branch' is not fully merged"
    echo ""
    echo "Options:"
    echo "  1. Skip this branch"
    echo "  2. Force delete (lose commits): git branch -D $branch"
    echo "  3. Show unmerged commits: git log $base_branch..$branch"
    echo "  4. Merge branch first: git merge $branch"
    echo ""
    echo "What would you like to do? (1-4)"
  fi
fi
```

### Remote Deletion Failure

```bash
if ! git push origin --delete $branch 2>&1; then
  error=$(git push origin --delete $branch 2>&1)

  if echo "$error" | grep -q "remote ref does not exist"; then
    echo "Branch '$branch' does not exist on remote"
    echo "Might already be deleted"
  elif echo "$error" | grep -q "protected"; then
    echo "Branch '$branch' is protected on remote"
    echo "Cannot delete via git push"
    echo "Delete via GitHub/GitLab UI if needed"
  elif echo "$error" | grep -q "permission denied"; then
    echo "Permission denied: cannot delete remote branch"
    echo "You may not have push access"
  else
    echo "Unknown error deleting remote branch:"
    echo "$error"
  fi
fi
```

### No Branches to Delete

```bash
if [ ${#branches_to_delete[@]} -eq 0 ]; then
  echo "No branches to delete!"
  echo ""
  echo "All branches are either:"
  echo "  - Protected branches"
  echo "  - Not fully merged"
  echo "  - Recently active"
  echo "  - Current branch"
  echo ""
  echo "Repository is clean!"
  exit 0
fi
```

### Base Branch Not Found

```bash
if ! git rev-parse --verify $base_branch >/dev/null 2>&1; then
  echo "Error: Base branch '$base_branch' not found"
  echo ""
  echo "Available branches:"
  git branch -a | grep -E "(main|master|develop)" | sed 's/^[* ] //'
  echo ""
  echo "Specify base branch as second argument:"
  echo "  /git:branch-cleanup local main"
  exit 1
fi
```

## Examples

### Example 1: Interactive Local Cleanup

```bash
/git:branch-cleanup local

# Analyzing branches...
# Base branch: main
#
# ========================================
# Branch Cleanup Analysis
# ========================================
#
# Fully Merged (8 branches):
# ------------------------------------------
# 1. feature/user-auth
#    Last: 36 days ago by John Doe
#    "Add JWT authentication"
#
# 2. bugfix/login-error
#    Last: 52 days ago by Jane Smith
#    "Fix login redirect issue"
#
# ... (6 more)
#
# Stale Branches (3 branches):
# ------------------------------------------
# 1. feature/old-idea
#    Last: 127 days ago by Bob Johnson
#    NOT merged - 15 unique commits
#
# ... (2 more)
#
# Protected (3 branches):
# ------------------------------------------
# - main (current)
# - develop
# - staging
#
# ========================================
# Actions:
# ========================================
# [1] Delete all fully merged branches
# [2] Review and delete individually
# [3] Handle stale branches
# [4] Show more details
# [5] Cancel
#
# Choice: 2
#
# Delete 'feature/user-auth'? (y/n/details)
# User: y
# ✓ Deleted feature/user-auth
#
# Delete 'bugfix/login-error'? (y/n/details)
# User: y
# ✓ Deleted bugfix/login-error
#
# ...
#
# Summary:
# ✓ Deleted 6 branches
# ✗ Skipped 2 branches
# ⚠ 3 stale branches need review
```

### Example 2: Batch Delete Merged Branches

```bash
/git:branch-cleanup local main

# Found 12 fully merged branches
# Show list? (y/n)
# User: y
#
# [Shows list of 12 branches...]
#
# Delete all? (y/n/select)
# User: y
#
# DRY-RUN: Would delete:
#   feature/user-auth
#   feature/api-v2
#   bugfix/login-error
#   ... (9 more)
#
# Proceed? (y/n)
# User: y
#
# Deleting branches...
# ✓ feature/user-auth
# ✓ feature/api-v2
# ✓ bugfix/login-error
# ...
#
# Deleted 12 branches successfully
```

### Example 3: Remote Branch Cleanup

```bash
/git:branch-cleanup remote origin/main

# ⚠ REMOTE CLEANUP WARNING
# This will delete branches from origin
# Other developers may be affected
#
# Have you coordinated with your team? (y/n)
# User: y
#
# Analyzing remote branches...
#
# Merged remote branches (15):
# ------------------------------------------
# origin/feature/completed-feature-1
# origin/feature/completed-feature-2
# origin/bugfix/old-fix
# ... (12 more)
#
# Checking for open pull requests...
# ✓ No open PRs found for these branches
#
# Delete remote branches? (y/n)
# User: y
#
# Deleting remote branches...
# ✓ Deleted origin/feature/completed-feature-1
# ✓ Deleted origin/feature/completed-feature-2
# ...
#
# Pruning remote tracking branches...
# ✓ Pruned 15 remote tracking branches
#
# Summary:
# Deleted 15 remote branches
# Your local branches were not affected
```

### Example 4: Handle Stale Branches

```bash
/git:branch-cleanup local

# ...
# Stale Branches (4 branches):
# ------------------------------------------
#
# 1. feature/experimental-ui
#    Last: 145 days ago by Alice Cooper
#    NOT merged - 23 unique commits
#    Show details? (y/n/delete/keep)
#    User: y
#
#    Branch details:
#    Created: 2025-06-01
#    Last commit: 2025-06-28
#    Commits ahead: 23
#    Commits behind: 127
#
#    Recent commits:
#      abc1234 - Experiment with new layout
#      def5678 - Add animation effects
#      ... (21 more)
#
#    Action for this branch?
#      [d] Delete (lose 23 commits)
#      [k] Keep (skip)
#      [t] Tag and delete (archive)
#      [b] Create backup branch
#    User: t
#
#    Creating archive tag: archive/experimental-ui
#    ✓ Tag created
#    ✓ Branch deleted
#
#    To restore: git checkout -b feature/experimental-ui archive/experimental-ui
```

### Example 5: Cleanup Both Local and Remote

```bash
/git:branch-cleanup both

# This will clean up both local and remote branches
# Base branch: main
#
# Phase 1: Local Analysis
# ========================================
# Fully merged: 8 branches
# Stale: 3 branches
#
# Phase 2: Remote Analysis
# ========================================
# Fully merged: 12 branches
# Stale: 5 branches
#
# Total branches to clean: 20
#
# Proceed with cleanup? (y/n/review)
# User: review
#
# [Shows detailed lists...]
#
# Start cleanup? (y/n)
# User: y
#
# Cleaning local branches...
# ✓ Deleted 8 local branches
#
# Cleaning remote branches...
# ⚠ This affects other developers!
# Continue? (y/n)
# User: y
#
# ✓ Deleted 12 remote branches
# ✓ Pruned remote tracking branches
#
# Total Summary:
# ✓ 8 local branches deleted
# ✓ 12 remote branches deleted
# ⚠ 8 stale branches need review
```

## Advanced Usage

### Archive Branches Before Deletion

```bash
# Create tags for branches before deleting
for branch in "${branches_to_delete[@]}"; do
  git tag "archive/$branch" "$branch"
  git branch -d "$branch"
done

# Push archive tags
git push origin --tags

# Later restore:
git checkout -b restored-branch archive/branch-name
```

### Export Branch List

```bash
# Save branch list before cleanup
git for-each-ref --format='%(refname:short) %(committerdate:iso8601) %(authorname)' refs/heads/ > branches-$(date +%Y%m%d).txt
```

### Filter by Author

```bash
# Find all branches by specific author
git for-each-ref --format='%(refname:short) %(authorname)' refs/heads/ | grep "John Doe"

# Delete branches by author
/git:branch-cleanup local --author="John Doe"
```

### Custom Stale Period

```bash
# Consider branches stale after 60 days instead of 90
/git:branch-cleanup local --stale-days=60
```

### Batch Operations with jq

```bash
# Get merged branches as JSON
git branch --merged main --format='%(refname:short)' | jq -R -s -c 'split("\n")[:-1]'

# Programmatic deletion
git branch --merged main --format='%(refname:short)' | grep -v "^main$" | xargs -n 1 git branch -d
```

## Tips for Maintaining Clean Branches

1. **Regular cleanup schedule:**
   - Weekly: Review active branches
   - Monthly: Clean up merged branches
   - Quarterly: Review stale branches
   - Set calendar reminders

2. **Branch naming conventions:**
   - Use prefixes: feature/, bugfix/, hotfix/
   - Include ticket numbers: feature/JIRA-123-description
   - Makes it easier to identify purpose

3. **Delete after merge:**
   - Delete branches immediately after PR merge
   - GitHub/GitLab can auto-delete
   - Don't let branches accumulate

4. **Protected branch policies:**
   - Configure protected branches in repo settings
   - Prevent accidental deletion
   - Require PR reviews

5. **Team communication:**
   - Announce before remote cleanup
   - Check with team before deleting shared branches
   - Use Slack/Teams to coordinate

6. **Branch limits:**
   - Keep total branches under 50
   - If more, time for cleanup
   - Too many branches = confusion

## Related Commands

- `/git:worktree` - Use worktrees instead of branches for parallel work
- `/git:cherry-pick-helper` - Cherry-pick commits before deleting branch
- `/git:reflog-recover` - Recover accidentally deleted branches
- `/git:rebase-interactive` - Clean up commits before merging

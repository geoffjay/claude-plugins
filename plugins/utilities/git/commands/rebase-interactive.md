---
name: git:rebase-interactive
description: Interactive rebase helper with guided workflows for squashing, reordering, editing, and splitting commits
---

# Git Interactive Rebase - Guided Commit History Editing

Interactive rebase helper with guided workflows for squashing, reordering, editing, and splitting commits.

## Command

`/git:rebase-interactive [base-ref] [operation]`

## Arguments

- `$1`: base-ref - Starting point for rebase (default: `origin/main` or `origin/master`)
- `$2`: operation - `squash|reorder|edit|split|drop` (optional, interactive if not provided)

## Description

Interactive rebase allows you to rewrite commit history by squashing commits together, reordering them, editing messages, splitting commits, or dropping unwanted commits. This is essential for maintaining a clean, logical commit history before merging to main branches.

## When to Use Interactive Rebase

- Clean up work-in-progress commits before creating PR
- Combine related commits into logical units
- Fix commit messages with typos or unclear descriptions
- Reorder commits to tell a better story
- Split large commits into smaller, focused ones
- Remove debug commits or experimental changes
- Prepare commits for code review

## When NOT to Use Interactive Rebase

- On commits already pushed to shared/public branches
- On merge commits (complex and dangerous)
- On commits other developers have based work on
- If you're unsure about what you're doing (use branches instead)

## Workflow

### Pre-rebase Checks

1. **Safety validation:**
   - Check for uncommitted changes
   - Verify not on main/master/protected branch
   - Check if commits are already pushed
   - Warn about force-push requirements
   - Confirm user understands rebase implications

2. **Gather information:**
   - Determine base commit (where to rebase from)
   - Show commits that will be rebased
   - Calculate number of commits
   - Display commit graph for context

3. **Show commits to be rebased:**
   ```bash
   git log --oneline --graph --decorate <base-ref>..HEAD
   ```

   Display each commit:
   - Commit hash (short)
   - Commit message
   - Author and date
   - Files changed count

### Interactive Mode Selection

4. **Ask user what they want to do:**
   - Squash commits (combine multiple commits)
   - Reorder commits (change commit order)
   - Edit commits (change messages or content)
   - Split commits (break one commit into multiple)
   - Drop commits (remove commits entirely)
   - Custom (use full rebase TODO editor)

### Squash Operation

5. **For squashing commits:**
   - Show all commits that will be rebased
   - Number them for easy reference
   - Ask which commits to squash together
   - Ask for groups: "Commits 2,3,4 into 1" or "Last 3 commits"
   - Confirm the squash plan

6. **Create rebase TODO list:**
   ```
   pick abc1234 First commit (keep this)
   squash def5678 Second commit (squash into above)
   squash ghi9012 Third commit (squash into above)
   pick jkl3456 Fourth commit (keep separate)
   ```

7. **Edit combined commit message:**
   - Show all commit messages being combined
   - Ask user to write new combined message
   - Provide template with all original messages
   - Suggest following conventional commits format

8. **Execute rebase:**
   ```bash
   git rebase -i <base-ref>
   ```

9. **Handle result:**
   - If successful: show new commit history
   - If conflicts: guide through resolution
   - Verify result matches intention

### Reorder Operation

10. **For reordering commits:**
    - Show commits with numbers
    - Current order: 1, 2, 3, 4, 5
    - Ask for new order: "3, 1, 2, 4, 5" or "Move commit 3 before 1"
    - Validate new order (all commits present, no duplicates)
    - Show before/after preview

11. **Create rebase TODO list:**
    ```
    pick ghi9012 Third commit (moved to first)
    pick abc1234 First commit (now second)
    pick def5678 Second commit (now third)
    pick jkl3456 Fourth commit (unchanged)
    ```

12. **Execute and verify:**
    - Run rebase with new order
    - Check for conflicts (reordering can cause conflicts)
    - Show resulting commit graph
    - Verify logical order

### Edit Operation

13. **For editing commits:**
    - Ask which commits to edit:
      - Message only
      - Content (files)
      - Both
    - Mark commits with 'edit' or 'reword'
    - Explain what will happen

14. **Create rebase TODO list:**
    ```
    pick abc1234 First commit
    reword def5678 Second commit (will edit message)
    edit ghi9012 Third commit (will edit content)
    pick jkl3456 Fourth commit
    ```

15. **Execute rebase:**
    - For 'reword': git opens editor for message
    - For 'edit': rebase pauses at commit
    - Show current state and next steps
    - Guide through making changes

16. **At each 'edit' stop:**
    - Show current commit
    - Options:
      - Amend commit: `git commit --amend`
      - Add more changes: stage files and amend
      - Continue: `git rebase --continue`
      - Abort: `git rebase --abort`

### Split Operation

17. **For splitting commits:**
    - Ask which commit to split
    - Mark commit with 'edit'
    - Explain split workflow

18. **At edit stop:**
    ```bash
    # Reset to parent commit (keep changes unstaged)
    git reset HEAD^

    # Now stage and commit in smaller chunks
    git add -p  # Interactively stage hunks
    git commit -m "First part"

    git add ...
    git commit -m "Second part"

    # Continue rebase
    git rebase --continue
    ```

19. **Guide through split:**
    - Show all changed files
    - Help user decide how to split
    - Suggest logical groupings
    - Create each new commit
    - Verify all changes included

### Drop Operation

20. **For dropping commits:**
    - Ask which commits to drop
    - Show what will be removed
    - Warn if commits introduce features used later
    - Confirm deletion

21. **Create rebase TODO list:**
    ```
    pick abc1234 First commit
    drop def5678 Second commit (will be removed)
    pick ghi9012 Third commit
    ```

22. **Execute and verify:**
    - Run rebase
    - Check for conflicts (dropped changes might be referenced)
    - Verify feature still works without dropped commits

### Conflict Resolution

23. **If conflicts occur:**
    - Pause rebase
    - Show conflicting files
    - Explain current state:
      - Which commit being applied
      - Why conflict occurred
      - What needs resolution

24. **Guide through resolution:**
    ```bash
    # Show conflicts
    git status

    # For each file
    git diff <file>

    # Options:
    # 1. Manually edit files to resolve
    # 2. Use mergetool: git mergetool
    # 3. Accept theirs: git checkout --theirs <file>
    # 4. Accept ours: git checkout --ours <file>
    # 5. Skip commit: git rebase --skip
    # 6. Abort rebase: git rebase --abort
    ```

25. **After resolving:**
    ```bash
    git add <resolved-files>
    git rebase --continue
    ```

26. **Continue until complete:**
    - May have multiple conflicts
    - Guide through each one
    - Show progress: "Resolving 2 of 5 commits"

### Post-rebase Verification

27. **Verify rebase success:**
    - Show new commit history
    - Compare before/after
    - Check that all intended changes present
    - Verify tests still pass

28. **Force push considerations:**
    - Explain why force-push needed
    - Check if commits were pushed before
    - Show safe force-push command:
      ```bash
      git push --force-with-lease
      ```
    - Warn about team coordination

## Safety Checks

### Before Rebase

- **Uncommitted changes:**
  ```bash
  if [ -n "$(git status --porcelain)" ]; then
    echo "Error: You have uncommitted changes"
    echo "Please commit or stash them first:"
    git status --short
    exit 1
  fi
  ```

- **Protected branch:**
  ```bash
  current_branch=$(git branch --show-current)
  if [[ "$current_branch" =~ ^(main|master|develop|production|staging)$ ]]; then
    echo "Error: You are on protected branch: $current_branch"
    echo "Interactive rebase is dangerous on shared branches"
    echo "Create a feature branch instead:"
    echo "  git checkout -b fix/rebase-changes"
    exit 1
  fi
  ```

- **Already pushed:**
  ```bash
  # Check if commits are pushed
  if git log --oneline @{u}.. | grep -q .; then
    echo "Warning: Some commits are not pushed yet (safe to rebase)"
  else
    echo "Warning: All commits are already pushed to remote"
    echo ""
    echo "Rebasing will require force-push: git push --force-with-lease"
    echo "This can affect other developers who have pulled your branch"
    echo ""
    echo "Continue with rebase? (y/n)"
    # Wait for confirmation
  fi
  ```

- **Merge commits:**
  ```bash
  merge_commits=$(git log --oneline --merges <base-ref>..HEAD | wc -l)
  if [ $merge_commits -gt 0 ]; then
    echo "Warning: This range contains $merge_commits merge commit(s)"
    echo "Rebasing merge commits is complex and may lose merge resolution"
    echo ""
    git log --oneline --merges <base-ref>..HEAD
    echo ""
    echo "Consider these alternatives:"
    echo "  1. Rebase only non-merge commits"
    echo "  2. Use git filter-branch instead"
    echo "  3. Manually rewrite history"
    echo ""
    echo "Continue anyway? (y/n)"
  fi
  ```

### During Rebase

- **Conflict help:**
  ```bash
  if [ -f ".git/rebase-merge/git-rebase-todo" ]; then
    echo "Rebase in progress. Current state:"
    echo ""

    # Show progress
    done_count=$(grep -c "^$" .git/rebase-merge/done 2>/dev/null || echo 0)
    total_count=$(wc -l < .git/rebase-merge/git-rebase-todo)
    echo "Progress: $done_count / $total_count commits"

    # Show conflicts
    if git status | grep -q "Unmerged paths"; then
      echo ""
      echo "Conflicted files:"
      git diff --name-only --diff-filter=U
      echo ""
      echo "Resolve conflicts then:"
      echo "  git add <file>..."
      echo "  git rebase --continue"
      echo ""
      echo "Or abort:"
      echo "  git rebase --abort"
    fi
  fi
  ```

- **Backup before proceeding:**
  ```bash
  # Create backup branch before risky operations
  backup_branch="backup-$(git branch --show-current)-$(date +%s)"
  git branch "$backup_branch"
  echo "Created backup branch: $backup_branch"
  echo "If something goes wrong: git reset --hard $backup_branch"
  ```

### After Rebase

- **Verify integrity:**
  ```bash
  # Check that no commits were lost
  echo "Verifying rebase result..."

  # Compare file tree
  git diff <original-head> HEAD

  if [ -z "$(git diff <original-head> HEAD)" ]; then
    echo "✓ Working tree identical (good)"
  else
    echo "⚠ Working tree differs:"
    echo "This is expected if you edited commit content"
    echo "Review changes:"
    git diff --stat <original-head> HEAD
  fi

  # Run tests
  echo ""
  echo "Consider running tests to verify nothing broke:"
  echo "  npm test"
  echo "  pytest"
  echo "  cargo test"
  ```

- **Force-push guidance:**
  ```bash
  echo ""
  echo "To update remote branch:"
  echo "  git push --force-with-lease"
  echo ""
  echo "⚠ Only force-push if:"
  echo "  - You are the only one working on this branch"
  echo "  - Or: You've coordinated with team members"
  echo "  - Or: This is a personal feature branch"
  echo ""
  echo "Never force-push to: main, master, develop"
  ```

## Error Handling

### Invalid Base Reference

```bash
if ! git rev-parse --verify "$base_ref" >/dev/null 2>&1; then
  echo "Error: Invalid base reference: $base_ref"
  echo ""
  echo "Valid references:"
  echo "  - Branch: main, develop, origin/main"
  echo "  - Commit: abc1234, HEAD~5"
  echo "  - Tag: v1.0.0"
  echo ""
  echo "To see available branches:"
  echo "  git branch -a"
  exit 1
fi
```

### No Commits to Rebase

```bash
commit_count=$(git log --oneline $base_ref..HEAD | wc -l)
if [ $commit_count -eq 0 ]; then
  echo "Error: No commits to rebase"
  echo "Base: $base_ref"
  echo "HEAD: $(git rev-parse HEAD)"
  echo ""
  echo "Your current branch is even with $base_ref"
  echo "Make some commits first, or choose a different base"
  exit 1
fi
```

### Rebase Already in Progress

```bash
if [ -d ".git/rebase-merge" ] || [ -d ".git/rebase-apply" ]; then
  echo "Error: Rebase already in progress"
  echo ""
  echo "Options:"
  echo "  1. Continue rebase: git rebase --continue"
  echo "  2. Skip current commit: git rebase --skip"
  echo "  3. Abort rebase: git rebase --abort"
  echo ""
  echo "Current status:"
  git status
  exit 1
fi
```

### Rebase Failed

```bash
# If git rebase command fails
if [ $? -ne 0 ]; then
  echo "Rebase failed!"
  echo ""

  # Check for conflicts
  if git status | grep -q "Unmerged paths"; then
    echo "You have conflicts to resolve:"
    git diff --name-only --diff-filter=U
    echo ""
    echo "Next steps:"
    echo "  1. Resolve conflicts in each file"
    echo "  2. Stage resolved files: git add <file>"
    echo "  3. Continue: git rebase --continue"
    echo ""
    echo "Or abort and try different approach:"
    echo "  git rebase --abort"
  else
    echo "Unknown error occurred"
    echo "Check: git status"
    echo ""
    echo "To abort and restore original state:"
    echo "  git rebase --abort"
  fi
  exit 1
fi
```

## Examples

### Example 1: Squash Last 3 Commits

```bash
/git:rebase-interactive HEAD~3 squash

# Claude shows:
# Commits to rebase:
#   1. abc1234 - Fix typo in README
#   2. def5678 - Add missing semicolon
#   3. ghi9012 - Update documentation
#
# Squash commits 1, 2, and 3 into one? (y/n)
# User: y
#
# Enter commit message for combined commit:
# User: "Improve documentation and fix typos"
#
# Rebasing...
# Success! New commit history:
#   abc9999 - Improve documentation and fix typos
```

### Example 2: Reorder Commits

```bash
/git:rebase-interactive origin/main reorder

# Current commit order:
#   1. abc1234 - Add tests
#   2. def5678 - Implement feature
#   3. ghi9012 - Update dependencies
#   4. jkl3456 - Fix bug in feature
#
# Enter new order (e.g., "2,4,1,3"):
# User: 3,2,4,1
#
# New order will be:
#   1. ghi9012 - Update dependencies
#   2. def5678 - Implement feature
#   3. jkl3456 - Fix bug in feature
#   4. abc1234 - Add tests
#
# This tells a better story: deps first, then feature, fix, then tests
# Continue? (y/n)
# User: y
#
# Rebasing... Success!
```

### Example 3: Edit Commit Message

```bash
/git:rebase-interactive HEAD~5 edit

# Which commits to edit?
#   1. abc1234 - Fix stuff (message unclear)
#   2. def5678 - Add feature X
#   3. ghi9012 - Update readme
#   4. jkl3456 - wip (message unclear)
#   5. mno7890 - Refactor auth
#
# Enter commit numbers to edit: 1,4
#
# Rebasing to commit 1: abc1234
# Current message: "Fix stuff"
# Enter new message:
# User: "Fix authentication token validation bug"
#
# Rebasing to commit 4: jkl3456
# Current message: "wip"
# Enter new message:
# User: "Add user session timeout handling"
#
# Rebase complete! Updated 2 commit messages.
```

### Example 4: Split Commit

```bash
/git:rebase-interactive HEAD~3 split

# Which commit to split?
#   1. abc1234 - Add feature X and Y and fix bug Z
#   2. def5678 - Update tests
#   3. ghi9012 - Update docs
#
# User: 1
#
# Stopping at commit abc1234...
# This commit changed:
#   src/featureX.js (45 additions)
#   src/featureY.js (67 additions)
#   src/bugfix.js (12 additions)
#
# Reset commit, keeping changes:
# Run: git reset HEAD^
#
# Now stage and commit in smaller pieces:
#   git add src/featureX.js
#   git commit -m "Add feature X"
#
#   git add src/featureY.js
#   git commit -m "Add feature Y"
#
#   git add src/bugfix.js
#   git commit -m "Fix bug Z"
#
# Then continue:
#   git rebase --continue
```

### Example 5: Interactive Full Control

```bash
/git:rebase-interactive origin/main

# 15 commits to rebase from origin/main
# What do you want to do?
#   1. Squash commits
#   2. Reorder commits
#   3. Edit commit messages
#   4. Split commits
#   5. Drop commits
#   6. Custom (use full TODO editor)
#
# User: 6
#
# Opening rebase TODO editor...
# Edit instructions as needed:
#
# pick abc1234 First commit
# squash def5678 Second commit (squash into first)
# reword ghi9012 Third commit (edit message)
# edit jkl3456 Fourth commit (edit content)
# drop mno7890 Fifth commit (remove)
# pick pqr3456 Sixth commit
#
# Save and close to start rebase
```

## Advanced Usage

### Autosquash Workflow

```bash
# Make fixup commits during development
git commit --fixup=abc1234

# Later, autosquash all fixup commits
git rebase -i --autosquash origin/main

# Fixup commits automatically squashed into target commits
```

### Exec Commands

```bash
# Run command after each commit during rebase
git rebase -i --exec "npm test" origin/main

# Rebase will pause if any test fails
# Useful for ensuring each commit builds/passes tests
```

### Preserve Merges (Careful!)

```bash
# Preserve merge commits (advanced)
git rebase -i --rebase-merges origin/main

# Only use if you understand implications
# Usually better to avoid rebasing merges
```

## Tips for Clean Commit History

1. **Logical commits:**
   - One feature/fix per commit
   - Atomic: each commit should build and pass tests
   - Related changes together

2. **Good commit messages:**
   - Clear, descriptive summary line
   - Body explains WHY, not what
   - Reference issue numbers
   - Follow conventional commits format

3. **Before creating PR:**
   - Squash WIP commits
   - Reorder for logical flow
   - Fix commit messages
   - Each commit tells part of the story

4. **Rebase strategies:**
   - Rebase early and often on feature branches
   - Keep commits organized from the start
   - Use fixup commits during development
   - Final cleanup before PR

5. **Team coordination:**
   - Don't rebase shared branches
   - Communicate before force-pushing
   - Use --force-with-lease, never --force
   - Consider rebasing only your commits

## Related Commands

- `/git:fixup` - Create fixup commits for autosquash
- `/git:branch-cleanup` - Clean up after rebasing
- `/git:cherry-pick-helper` - Alternative to rebase for specific commits
- `/git:reflog-recover` - Recover from rebase mistakes

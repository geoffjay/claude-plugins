---
name: git:bisect
description: Interactive git bisect workflow to find commits that introduced bugs using binary search
---

# Git Bisect - Binary Search for Bug-Introducing Commits

Interactive git bisect workflow to find commits that introduced bugs using binary search.

## Command

`/git:bisect [mode] [commit-ref]`

## Arguments

- `$1`: mode - `start|good|bad|skip|reset` (optional, interactive if not provided)
- `$2`: commit-ref (optional, depends on mode)

## Description

Git bisect uses binary search to efficiently find the commit that introduced a bug. Instead of checking every commit, it splits the commit range in half repeatedly, asking you to test each midpoint. This can find a bug in log(n) checks instead of n checks.

## Workflow

### Starting a Bisect Session

1. **Pre-flight checks:**
   - Check if bisect is already in progress: `git bisect log`
   - Check for uncommitted changes: `git status --porcelain`
   - If changes exist, warn user and suggest stashing

2. **Gather information:**
   - Ask for the "good" commit (where bug didn't exist)
     - Default: last tag or commit from 1 week ago
     - User can specify: commit hash, tag, branch name
   - Ask for the "bad" commit (where bug exists)
     - Default: HEAD (current commit)
     - User can specify: commit hash, tag, branch name
   - Calculate and show number of commits between good and bad
   - Estimate number of steps needed: ~log2(n)

3. **Start bisect:**
   ```bash
   git bisect start
   git bisect bad [bad-commit]
   git bisect good [good-commit]
   ```

4. **Show first commit to test:**
   - Display commit hash, date, author, message
   - Show which files changed: `git show --stat <commit>`
   - Provide clear instructions on what to test

### During Bisect Session

5. **Test current commit:**
   - Ask user to test whether the bug exists
   - Provide clear instructions:
     - "Run your tests"
     - "Manually test the feature"
     - "Check the logs"
   - Wait for user feedback

6. **Mark commit based on test result:**
   - If bug exists: `git bisect bad`
   - If bug doesn't exist: `git bisect good`
   - If commit is untestable (won't build, etc): `git bisect skip`
   - Option to abort: `git bisect reset`

7. **Show progress:**
   - Display remaining commits to test
   - Show estimated steps left
   - Display bisect log: `git bisect log`

8. **Repeat steps 5-7** until the first bad commit is found

### Completion

9. **When bug commit identified:**
   - Display full commit details:
     ```bash
     git show <commit-hash>
     ```
   - Show commit message, author, date
   - Show full diff
   - Highlight which files were changed

10. **Offer actions:**
    - Create a branch from this commit for investigation
    - Create a branch from parent commit for fix
    - Copy commit hash to clipboard
    - View commit in GitHub/GitLab (if remote exists)
    - Reset bisect and return to original HEAD

11. **Reset bisect:**
    ```bash
    git bisect reset
    ```
    - Return to original branch/commit
    - Confirm user is back to starting state

### Abort/Reset Anytime

At any point during the bisect, user can:
- Type 'abort' to run `git bisect reset`
- Type 'skip' to skip current commit
- Type 'log' to see bisect progress
- Type 'visualize' to see bisect state graphically

## Safety Checks

### Before Starting

- **Uncommitted changes:**
  ```bash
  if [ -n "$(git status --porcelain)" ]; then
    echo "Warning: You have uncommitted changes."
    echo "Options:"
    echo "  1. Stash changes: git stash save 'Pre-bisect stash'"
    echo "  2. Commit changes"
    echo "  3. Discard changes (dangerous)"
    echo "  4. Cancel bisect"
    # Wait for user choice
  fi
  ```

- **Already in bisect:**
  ```bash
  if [ -f .git/BISECT_LOG ]; then
    echo "Bisect already in progress!"
    echo "Options:"
    echo "  1. Continue current bisect"
    echo "  2. Reset and start new bisect"
    echo "  3. Cancel"
    # Wait for user choice
  fi
  ```

- **Detached HEAD warning:**
  - Explain that bisect will put repo in detached HEAD state
  - Assure user that `git bisect reset` will return to original state

### During Bisect

- **Clear instructions at each step:**
  - Show current commit details
  - Explain what user needs to test
  - Show available commands (good/bad/skip/reset)
  - Display progress and remaining steps

- **Skip commit handling:**
  - Explain when to skip (build failures, unrelated changes)
  - Warn that excessive skipping reduces effectiveness
  - Show how many commits have been skipped

### After Bisect

- **Confirmation before reset:**
  - Ask if user wants to save any notes
  - Offer to create branch at bug commit
  - Confirm reset operation

- **Verify return state:**
  - Check user is back on original branch
  - Verify working directory is clean
  - Confirm bisect refs are removed

## Error Handling

### Invalid Commit References

```bash
if ! git rev-parse --verify "$commit_ref" >/dev/null 2>&1; then
  echo "Error: '$commit_ref' is not a valid commit reference"
  echo "Valid formats:"
  echo "  - Commit hash: abc1234 or abc1234567890abcdef"
  echo "  - Branch name: main, feature-branch"
  echo "  - Tag: v1.0.0"
  echo "  - Relative: HEAD~5, HEAD^^^"
  exit 1
fi
```

### Good Commit is Newer Than Bad Commit

```bash
if [ $(git rev-list --count $good_commit..$bad_commit) -eq 0 ]; then
  echo "Error: Good commit ($good_commit) is not an ancestor of bad commit ($bad_commit)"
  echo "Make sure:"
  echo "  - Good commit is older (bug didn't exist yet)"
  echo "  - Bad commit is newer (bug exists)"
  echo "  - Both commits are on the same branch history"
  exit 1
fi
```

### Build Failures

```bash
# When user reports commit won't build
echo "This commit won't build/test. Options:"
echo "  1. Skip this commit: git bisect skip"
echo "  2. Skip a range: git bisect skip v1.0..v1.5"
echo "  3. Reset and try different good/bad commits"
# Wait for user choice
```

### Conflicts or Issues

```bash
# If checkout fails during bisect
if [ $? -ne 0 ]; then
  echo "Error: Could not checkout commit"
  echo "This might indicate:"
  echo "  - Local modifications conflict with commit"
  echo "  - Repository corruption"
  echo "Run 'git bisect reset' to abort and investigate"
  exit 1
fi
```

## Examples

### Example 1: Basic Interactive Bisect

```bash
# Start interactive bisect
/git:bisect

# Claude will prompt:
# "When did you last see the code working correctly?"
# User: "On the v1.2.0 tag"
#
# "When did you first notice the bug?"
# User: "In the current commit (HEAD)"
#
# Starting bisect with 47 commits between v1.2.0 and HEAD
# This will take approximately 6 steps
#
# Now at: commit abc1234
# Author: John Doe
# Date: 2025-10-15
# Message: Refactor authentication module
#
# Files changed:
#   src/auth.js | 45 +++++++++++++++++++++
#   tests/auth.test.js | 23 +++++++++++
#
# Please test if the bug exists in this commit.
# Reply with: good, bad, skip, or abort
```

### Example 2: Direct Mode Commands

```bash
# Start bisect directly
/git:bisect start

# Mark HEAD as bad
/git:bisect bad

# Mark a specific commit as good
/git:bisect good v1.2.0

# Skip untestable commit
/git:bisect skip

# View bisect log
git bisect log

# Reset and return to original state
/git:bisect reset
```

### Example 3: Automated Testing

```bash
# For repositories with automated tests
/git:bisect

# At each commit, run:
npm test  # or: pytest, cargo test, go test, etc.

# If tests pass:
/git:bisect good

# If tests fail:
/git:bisect bad

# Continue until bug commit found
```

### Example 4: Binary Search Range

```bash
# Search within specific range
/git:bisect start HEAD v1.0.0

# Or use commit hashes
/git:bisect start abc1234 def5678

# Or use date-based references
/git:bisect start HEAD HEAD@{2.weeks.ago}
```

## Advanced Usage

### Bisect with Script

For fully automated bisecting when you have a test that can determine good/bad:

```bash
# Create a test script that exits 0 for good, 1 for bad
cat > test-bug.sh << 'EOF'
#!/bin/bash
npm test -- --testNamePattern="specific bug test"
EOF
chmod +x test-bug.sh

# Run bisect with script
git bisect start HEAD v1.0.0
git bisect run ./test-bug.sh
```

### Visualize Bisect State

```bash
# Text-based visualization
git bisect visualize --oneline

# Or with gitk (if available)
git bisect visualize
```

### Skip a Range of Commits

```bash
# If you know commits in a range are all untestable
git bisect skip v1.1.0..v1.2.0
```

### Bisect Log Analysis

```bash
# View complete bisect log
git bisect log

# Replay bisect from log
git bisect replay path/to/bisect-log.txt
```

## Tips for Effective Bisecting

1. **Choose good starting points:**
   - Good commit: Use a tagged release where you know code worked
   - Bad commit: Use the commit where you first noticed the bug
   - Wider range = more accurate, but more steps

2. **Have a clear test:**
   - Know exactly what behavior indicates the bug
   - Have a reproducible test case
   - Ideally have an automated test

3. **Handle build failures:**
   - Skip commits that won't build
   - If too many skip, widen the initial range

4. **Track progress:**
   - Note down commit hashes you've tested
   - Keep test results consistent
   - Don't change test criteria mid-bisect

5. **When bug commit found:**
   - Verify it's truly the first bad commit
   - Check if bug is in the commit itself or its merge
   - Look at what changed in that commit

## Output Format

During bisect, Claude will display structured output:

```
========================================
Git Bisect Status
========================================
Range: v1.2.0 (good) → HEAD (bad)
Total commits: 47
Estimated steps: 6 remaining

Current Commit:
----------------------------------------
Hash: abc1234567890abcdef
Author: Jane Smith <jane@example.com>
Date: Mon Oct 16 14:32:10 2025 -0700
Message: Update user authentication flow

Files Changed (5):
  src/auth/login.js       | 34 +++++++++++++++---
  src/auth/session.js     | 12 +++++--
  tests/auth/login.test.js| 45 ++++++++++++++++++++++++
  ...

========================================
Action Required:
----------------------------------------
1. Test if bug exists in this commit
2. Reply with result:
   - 'good' - bug does NOT exist
   - 'bad'  - bug DOES exist
   - 'skip' - cannot test this commit
   - 'abort' - stop bisect

What's your result?
```

## Related Commands

- `/git:reflog-recover` - Recover from bisect mistakes
- `/git:cherry-pick-helper` - Cherry-pick the bug fix
- `/git:worktree` - Test multiple commits simultaneously
- `/git:branch-cleanup` - Clean up bisect test branches

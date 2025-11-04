---
name: tokio-review
description: Review Tokio code for async anti-patterns, performance issues, and best practices
---

# Tokio Review Command

This command performs comprehensive code review of Tokio-based applications, identifying async/await anti-patterns, performance issues, blocking operations, and suggesting improvements.

## Arguments

- `$1` - File path or directory to review (optional, defaults to current directory)

## Usage

```
/rust-tokio-expert:tokio-review
/rust-tokio-expert:tokio-review src/handlers/
/rust-tokio-expert:tokio-review src/main.rs
```

## Workflow

1. **Analyze Target**
   - If no argument provided, scan current directory for Rust files
   - If directory provided, scan all `.rs` files recursively
   - If file provided, review that specific file

2. **Read Relevant Files**
   - Use Glob tool to find Rust source files
   - Read all identified files using Read tool
   - Prioritize files in: src/main.rs, src/lib.rs, src/**/*.rs

3. **Invoke Agent**
   - Use Task tool with `subagent_type="rust-tokio-expert:tokio-performance"`
   - Provide all source code context to the agent
   - Request comprehensive analysis

4. **Review Checklist**

   The agent should analyze for:

   ### Async/Await Anti-Patterns

   - [ ] **Blocking Operations in Async Context**
     - Detect `std::thread::sleep` instead of `tokio::time::sleep`
     - Identify blocking I/O operations
     - Find CPU-intensive operations not wrapped in `spawn_blocking`

   - [ ] **Holding Locks Across Await Points**
     - Detect `std::sync::Mutex` or `tokio::sync::Mutex` held across `.await`
     - Suggest lock scope reduction
     - Recommend alternatives like channels

   - [ ] **Unnecessary Cloning**
     - Identify expensive clones in async contexts
     - Suggest `Arc` for shared data
     - Recommend reference passing where possible

   - [ ] **Futures Not Being Awaited**
     - Find async functions called without `.await`
     - Detect unused futures
     - Identify missing error handling

   ### Performance Issues

   - [ ] **Excessive Task Spawning**
     - Detect unbounded task creation in loops
     - Suggest `buffer_unordered` or bounded concurrency
     - Recommend semaphore-based limiting

   - [ ] **Large Future Sizes**
     - Identify large types stored in future state
     - Suggest boxing large data
     - Recommend heap allocation for big arrays

   - [ ] **Inefficient Channel Usage**
     - Detect unbounded channels
     - Identify inappropriate channel types
     - Suggest buffer size optimization

   - [ ] **Memory Allocation in Hot Paths**
     - Find repeated allocations in loops
     - Suggest buffer reuse
     - Recommend object pooling

   ### Concurrency Issues

   - [ ] **Potential Deadlocks**
     - Detect complex lock ordering
     - Identify circular dependencies
     - Suggest lock-free alternatives

   - [ ] **Missing Timeout Handling**
     - Find network operations without timeouts
     - Suggest `tokio::time::timeout` usage
     - Recommend timeout configuration

   - [ ] **Improper Shutdown Handling**
     - Check for graceful shutdown implementation
     - Verify cleanup in Drop implementations
     - Ensure resource release

   ### Error Handling

   - [ ] **Error Propagation**
     - Verify proper error context
     - Check error type appropriateness
     - Suggest improvements for error handling

   - [ ] **Panic in Async Context**
     - Detect unwrap/expect in async code
     - Suggest proper error handling
     - Recommend Result usage

   ### Channel Patterns

   - [ ] **Channel Selection**
     - Verify appropriate channel type (mpsc, oneshot, broadcast, watch)
     - Check buffer sizes
     - Suggest alternatives if needed

   - [ ] **Select! Usage**
     - Review select! macro usage
     - Check for biased selection when needed
     - Verify all branches handle errors

   ### Runtime Configuration

   - [ ] **Runtime Setup**
     - Check worker thread configuration
     - Verify blocking thread pool size
     - Suggest optimizations based on workload

5. **Generate Report**

   Create a structured review report with:

   ### Critical Issues (Must Fix)
   - Blocking operations in async context
   - Potential deadlocks
   - Memory safety issues
   - Resource leaks

   ### High Priority (Should Fix)
   - Performance bottlenecks
   - Inefficient patterns
   - Missing error handling
   - Improper shutdown handling

   ### Medium Priority (Consider Fixing)
   - Suboptimal channel usage
   - Missing timeouts
   - Code organization
   - Documentation gaps

   ### Low Priority (Nice to Have)
   - Style improvements
   - Additional tracing
   - Better variable names

   For each issue, provide:
   - **Location**: File, line number, function
   - **Issue**: Clear description of the problem
   - **Impact**: Why it matters (performance, correctness, maintainability)
   - **Suggestion**: Specific fix with code example
   - **Priority**: Critical, High, Medium, Low

6. **Code Examples**

   For each suggestion, provide:
   - Current problematic code
   - Suggested improved code
   - Explanation of the improvement

7. **Summary Statistics**

   Provide overview:
   - Total files reviewed
   - Total issues found (by priority)
   - Estimated effort to fix
   - Overall code health score (if applicable)

## Example Report Format

```markdown
# Tokio Code Review Report

## Summary
- Files reviewed: 15
- Critical issues: 2
- High priority: 5
- Medium priority: 8
- Low priority: 3

## Critical Issues

### 1. Blocking Operation in Async Context
**Location**: `src/handlers/user.rs:45`
**Function**: `process_user`

**Issue**:
Using `std::thread::sleep` in async function blocks the runtime thread.

**Current Code**:
\`\`\`rust
async fn process_user(id: u64) {
    std::thread::sleep(Duration::from_secs(1)); // Blocks thread!
    // ...
}
\`\`\`

**Suggested Fix**:
\`\`\`rust
async fn process_user(id: u64) {
    tokio::time::sleep(Duration::from_secs(1)).await; // Yields control
    // ...
}
\`\`\`

**Impact**: This blocks an entire runtime worker thread, preventing other tasks from making progress. Can cause significant performance degradation under load.

## High Priority Issues

### 1. Lock Held Across Await Point
**Location**: `src/state.rs:78`
...
```

## Best Practices Validation

The review should also verify:

1. **Tracing**: Proper use of `#[instrument]` and structured logging
2. **Error Types**: Appropriate error types with context
3. **Testing**: Async tests with `#[tokio::test]`
4. **Documentation**: Doc comments on public async functions
5. **Metrics**: Performance-critical paths instrumented
6. **Configuration**: Runtime properly configured
7. **Dependencies**: Using appropriate crate versions

## Notes

- Focus on actionable feedback with concrete examples
- Prioritize issues that impact correctness over style
- Provide educational explanations for async concepts
- Suggest resources for learning more about identified issues
- Be constructive and supportive in feedback tone

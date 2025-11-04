---
name: cli-review
description: Review Rust CLI applications for UX, error handling, testing, and cross-platform compatibility
---

# CLI Review Command

Comprehensively review a Rust CLI application for code quality, user experience, error handling, testing coverage, and cross-platform compatibility.

## Arguments

- `$1` - Path to project directory (optional, defaults to current directory)
- `--focus` - Specific area to focus on: "ux", "errors", "tests", "config", "perf", or "all" (optional, default: "all")

## Usage

```bash
# Review current directory
/cli-review

# Review specific project
/cli-review /path/to/my-cli

# Focus on specific area
/cli-review --focus ux
/cli-review --focus errors
/cli-review --focus tests
```

## Review Areas

### 1. Argument Design & CLI Interface

**Checks:**
- [ ] Argument naming follows conventions (kebab-case)
- [ ] Short and long forms provided where appropriate
- [ ] Help text is clear and descriptive
- [ ] Defaults are sensible and documented
- [ ] Mutually exclusive args use proper groups
- [ ] Required args are clearly marked
- [ ] Value names are descriptive (FILE, PORT, URL)
- [ ] Global options work with all subcommands
- [ ] Version information is present

**Example Issues:**

```
❌ Issue: Unclear argument name
   File: src/cli.rs:15
   Found: #[arg(short, long)]
          pub x: String,

   Recommendation: Use descriptive names
   #[arg(short, long, value_name = "FILE")]
   pub input_file: PathBuf,
```

### 2. Help Text Quality

**Checks:**
- [ ] Command-level help is present
- [ ] All arguments have descriptions
- [ ] Long help provides examples
- [ ] Help text uses active voice
- [ ] Complex options have detailed explanations
- [ ] Examples section shows common usage
- [ ] After-help provides additional resources

**Example Issues:**

```
❌ Issue: Missing help text
   File: src/cli.rs:23
   Found: #[arg(short, long)]
          pub verbose: bool,

   Recommendation: Add descriptive help
   /// Enable verbose output with detailed logging
   #[arg(short, long)]
   pub verbose: bool,
```

### 3. Error Messages

**Checks:**
- [ ] Errors explain what went wrong
- [ ] Errors suggest how to fix the problem
- [ ] File paths are displayed in error messages
- [ ] Using miette or similar for rich diagnostics
- [ ] Error types are well-structured (thiserror)
- [ ] Context is added at each error level
- [ ] Exit codes are meaningful and documented
- [ ] Errors go to stderr, not stdout

**Example Issues:**

```
❌ Issue: Unhelpful error message
   File: src/commands/build.rs:42
   Found: bail!("Build failed");

   Recommendation: Provide context and solutions
   bail!(
       "Build failed: {}\n\n\
        Possible causes:\n\
        - Missing dependencies\n\
        - Invalid configuration\n\
        Try: cargo check",
       source
   );
```

### 4. User Experience

**Checks:**
- [ ] Progress indicators for long operations
- [ ] Colors used semantically (red=error, green=success)
- [ ] NO_COLOR environment variable respected
- [ ] Interactive prompts have --yes flag alternative
- [ ] Destructive operations require confirmation
- [ ] Output is well-formatted (tables, lists)
- [ ] Supports both human and machine-readable output
- [ ] Verbosity levels work correctly (-v, -vv, -vvv)

**Example Issues:**

```
⚠ Warning: Missing progress indicator
   File: src/commands/download.rs:30
   Found: Long-running download operation without feedback

   Recommendation: Add progress bar
   use indicatif::{ProgressBar, ProgressStyle};

   let pb = ProgressBar::new(total_size);
   pb.set_style(ProgressStyle::default_bar()...);
```

### 5. Configuration Management

**Checks:**
- [ ] Config file support implemented
- [ ] Environment variables supported
- [ ] Precedence is correct (defaults < file < env < CLI)
- [ ] Config file locations follow XDG spec
- [ ] Command to generate default config
- [ ] Config validation on load
- [ ] Sensitive data from env vars only
- [ ] Config errors are helpful

**Example Issues:**

```
❌ Issue: No environment variable support
   File: src/config.rs:15
   Found: Config only loaded from file

   Recommendation: Support env vars
   #[arg(long, env = "MYAPP_DATABASE_URL")]
   pub database_url: String,
```

### 6. Cross-Platform Compatibility

**Checks:**
- [ ] Path handling uses std::path, not string concat
- [ ] File permissions checked before use
- [ ] Line endings handled correctly (CRLF vs LF)
- [ ] Platform-specific code properly cfg-gated
- [ ] Terminal width detection
- [ ] Color support detection
- [ ] Signal handling (Ctrl+C)
- [ ] Tests run on all platforms in CI

**Example Issues:**

```
❌ Issue: Hardcoded path separator
   File: src/utils.rs:10
   Found: let path = format!("{}/{}", dir, file);

   Recommendation: Use Path::join
   let path = Path::new(dir).join(file);
```

### 7. Testing Coverage

**Checks:**
- [ ] Integration tests present (assert_cmd)
- [ ] Help output tested
- [ ] Error cases tested
- [ ] Exit codes verified
- [ ] Config loading tested
- [ ] Environment variable handling tested
- [ ] Snapshot tests for output (insta)
- [ ] Cross-platform tests in CI

**Example Issues:**

```
⚠ Warning: No integration tests found
   Expected: tests/integration.rs or tests/cli_tests.rs

   Recommendation: Add integration tests
   See: https://rust-cli.github.io/book/tutorial/testing.html
```

### 8. Performance

**Checks:**
- [ ] Startup time is reasonable (< 100ms for --help)
- [ ] Binary size is optimized
- [ ] Lazy loading for heavy dependencies
- [ ] Streaming for large files
- [ ] Async runtime only when needed
- [ ] Proper buffering for I/O

## Review Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLI Review Report: my-cli
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall Rating: B+ (Good)

Summary:
✓ 23 checks passed
⚠ 5 warnings
❌ 3 issues found

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Issues Found
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ CRITICAL: Missing error context
   File: src/commands/build.rs:42
   Line: return Err(e.into());

   Problem: Errors are not wrapped with context
   Impact: Users won't understand what failed

   Recommendation:
   return Err(e)
       .context("Failed to build project")
       .context("Check build configuration");

   Priority: High
   Effort: Low

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠ WARNING: No progress indicator
   File: src/commands/download.rs:55

   Problem: Long operation without user feedback
   Impact: Poor user experience, appears frozen

   Recommendation:
   Add indicatif progress bar for downloads

   Priority: Medium
   Effort: Low

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Strengths
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Well-structured CLI with clear subcommands
✓ Good use of Clap derive API
✓ Proper error types with thiserror
✓ Configuration management implemented
✓ Cross-platform path handling

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Recommendations
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Priority: HIGH
1. Add error context to all error paths
2. Implement integration tests
3. Add --help examples section

Priority: MEDIUM
4. Add progress indicators for long operations
5. Implement shell completion generation
6. Add NO_COLOR support

Priority: LOW
7. Optimize binary size with strip = true
8. Add benchmarks for performance testing

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Detailed Metrics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Code Quality:         ████████░░ 80%
Error Handling:       ██████░░░░ 60%
User Experience:      ███████░░░ 70%
Testing:              ████░░░░░░ 40%
Documentation:        ████████░░ 80%
Cross-Platform:       █████████░ 90%

Binary Size:          2.1 MB (Good)
Startup Time:         45ms (Excellent)
Test Coverage:        45% (Needs Improvement)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next Steps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Address critical issues (3 found)
2. Review and fix warnings (5 found)
3. Improve test coverage to >70%
4. Add missing documentation

Run with specific focus:
  /cli-review --focus errors
  /cli-review --focus ux
  /cli-review --focus tests

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Workflow

When you invoke this command:

1. **Analyze Project Structure**
   - Identify CLI framework (Clap, structopt, etc.)
   - Locate main entry point and command definitions
   - Map out module structure

2. **Review CLI Interface**
   - Parse CLI definitions
   - Check argument naming and documentation
   - Verify help text quality
   - Test help output

3. **Analyze Error Handling**
   - Review error types
   - Check error message quality
   - Verify proper context addition
   - Test error scenarios

4. **Check User Experience**
   - Look for progress indicators
   - Review color usage
   - Check interactive prompts
   - Verify output formatting

5. **Examine Configuration**
   - Review config loading
   - Check precedence implementation
   - Verify env var support
   - Test config validation

6. **Test Cross-Platform Support**
   - Review path handling
   - Check platform-specific code
   - Verify CI configuration
   - Test on different platforms

7. **Assess Testing**
   - Count integration tests
   - Check test coverage
   - Review test quality
   - Identify missing tests

8. **Generate Report**
   - Compile findings
   - Prioritize issues
   - Provide recommendations
   - Calculate metrics

## Implementation

Use the **rust-cli-developer** agents to perform the review:

```
Use Task tool with subagent_type="rust-cli-developer:cli-ux-specialist"
for UX and error message review

Use Task tool with subagent_type="rust-cli-developer:cli-testing-expert"
for test coverage analysis

Use Task tool with subagent_type="rust-cli-developer:cli-architect"
for architecture and cross-platform review

Use Task tool with subagent_type="rust-cli-developer:clap-expert"
for CLI interface review
```

## Focus Options

### UX Focus

Reviews only user experience aspects:
- Color usage
- Progress indicators
- Interactive prompts
- Output formatting
- Error messages

### Errors Focus

Reviews only error handling:
- Error types
- Error messages
- Context addition
- Exit codes
- Recovery strategies

### Tests Focus

Reviews only testing:
- Integration tests
- Test coverage
- Test quality
- Missing test scenarios
- CI configuration

### Config Focus

Reviews only configuration:
- Config loading
- Precedence
- Environment variables
- Validation
- Documentation

### Performance Focus

Reviews only performance:
- Startup time
- Binary size
- Memory usage
- I/O efficiency
- Async usage

## Notes

- Review is non-destructive (read-only analysis)
- Generates actionable recommendations
- Prioritizes issues by impact and effort
- Provides code examples for fixes
- Can be run in CI for automated checks

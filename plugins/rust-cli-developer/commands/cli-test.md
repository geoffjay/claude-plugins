---
name: cli-test
description: Generate comprehensive tests for Rust CLI applications including integration, snapshot, and property-based tests
---

# CLI Test Command

Generate comprehensive test suites for Rust CLI applications, including integration tests, snapshot tests for output, and property-based tests for input validation.

## Arguments

- `$1` - Test type: "integration", "snapshot", "property", or "all" (required)
- `$2` - Path to project directory (optional, defaults to current directory)
- `--command <name>` - Specific command to test (optional)

## Usage

```bash
# Generate all test types
/cli-test all

# Generate integration tests only
/cli-test integration

# Generate snapshot tests for specific command
/cli-test snapshot --command build

# Generate property-based tests
/cli-test property

# Test specific project
/cli-test all /path/to/my-cli
```

## Test Types

### 1. Integration Tests

Tests that run the actual CLI binary with different arguments and verify output, exit codes, and side effects.

**Generated Tests:**

```rust
// tests/integration_tests.rs
use assert_cmd::Command;
use assert_fs::prelude::*;
use predicates::prelude::*;

fn cmd() -> Command {
    Command::cargo_bin(env!("CARGO_PKG_NAME")).unwrap()
}

#[test]
fn test_help_flag() {
    cmd().arg("--help")
        .assert()
        .success()
        .stdout(predicate::str::contains("Usage:"));
}

#[test]
fn test_version_flag() {
    cmd().arg("--version")
        .assert()
        .success()
        .stdout(predicate::str::contains(env!("CARGO_PKG_VERSION")));
}

#[test]
fn test_invalid_argument() {
    cmd().arg("--invalid")
        .assert()
        .failure()
        .stderr(predicate::str::contains("unexpected argument"));
}

#[test]
fn test_missing_required_arg() {
    cmd().arg("build")
        .assert()
        .failure()
        .stderr(predicate::str::contains("required arguments"));
}

#[test]
fn test_command_with_file_io() -> Result<(), Box<dyn std::error::Error>> {
    let temp = assert_fs::TempDir::new()?;
    let input = temp.child("input.txt");
    input.write_str("test content")?;

    let output = temp.child("output.txt");

    cmd()
        .arg("process")
        .arg(input.path())
        .arg("--output")
        .arg(output.path())
        .assert()
        .success();

    output.assert(predicate::path::exists());
    output.assert(predicate::str::contains("TEST CONTENT"));

    temp.close()?;
    Ok(())
}

#[test]
fn test_exit_code_config_error() {
    cmd()
        .arg("--config")
        .arg("/nonexistent/config.toml")
        .assert()
        .code(2)
        .failure();
}

#[test]
fn test_env_var_override() -> Result<(), Box<dyn std::error::Error>> {
    cmd()
        .env("MYAPP_PORT", "9000")
        .arg("config")
        .arg("show")
        .assert()
        .success()
        .stdout(predicate::str::contains("9000"));

    Ok(())
}
```

### 2. Snapshot Tests

Tests that capture and compare command output to saved snapshots, useful for help text, formatted output, and error messages.

**Generated Tests:**

```rust
// tests/snapshots.rs
use assert_cmd::Command;
use insta::{assert_snapshot, with_settings};

fn cmd() -> Command {
    Command::cargo_bin(env!("CARGO_PKG_NAME")).unwrap()
}

#[test]
fn test_help_output() {
    let output = cmd()
        .arg("--help")
        .output()
        .unwrap();

    assert_snapshot!(String::from_utf8_lossy(&output.stdout));
}

#[test]
fn test_command_help() {
    let output = cmd()
        .arg("build")
        .arg("--help")
        .output()
        .unwrap();

    assert_snapshot!("build_help", String::from_utf8_lossy(&output.stdout));
}

#[test]
fn test_version_output() {
    let output = cmd()
        .arg("--version")
        .output()
        .unwrap();

    assert_snapshot!(String::from_utf8_lossy(&output.stdout));
}

#[test]
fn test_error_message_format() {
    let output = cmd()
        .arg("build")
        .arg("--invalid-option")
        .output()
        .unwrap();

    assert_snapshot!(String::from_utf8_lossy(&output.stderr));
}

#[test]
fn test_formatted_output_with_filters() {
    let output = cmd()
        .arg("status")
        .output()
        .unwrap();

    let stdout = String::from_utf8_lossy(&output.stdout);

    // Filter out timestamps and dynamic data
    with_settings!({
        filters => vec![
            (r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", "[TIMESTAMP]"),
            (r"Duration: \d+ms", "Duration: [TIME]"),
            (r"/[^\s]+/([^/\s]+)", "/path/to/$1"),
        ]
    }, {
        assert_snapshot!(stdout);
    });
}

#[test]
fn test_table_output() -> Result<(), Box<dyn std::error::Error>> {
    let output = cmd()
        .arg("list")
        .output()?;

    with_settings!({
        filters => vec![
            (r"\d{4}-\d{2}-\d{2}", "[DATE]"),
        ]
    }, {
        assert_snapshot!(String::from_utf8_lossy(&output.stdout));
    });

    Ok(())
}
```

### 3. Property-Based Tests

Tests that verify CLI behavior across a wide range of inputs using property-based testing.

**Generated Tests:**

```rust
// tests/property_tests.rs
use assert_cmd::Command;
use proptest::prelude::*;

fn cmd() -> Command {
    Command::cargo_bin(env!("CARGO_PKG_NAME")).unwrap()
}

proptest! {
    #[test]
    fn test_port_validation(port in 0u16..=65535) {
        let result = cmd()
            .arg("--port")
            .arg(port.to_string())
            .arg("validate")
            .output()
            .unwrap();

        if (1024..=65535).contains(&port) {
            assert!(result.status.success(),
                "Port {} should be valid", port);
        } else {
            assert!(!result.status.success(),
                "Port {} should be invalid", port);
        }
    }

    #[test]
    fn test_string_input_handling(s in "\\PC{0,100}") {
        // CLI should handle any valid Unicode string without panicking
        let result = cmd()
            .arg("--name")
            .arg(&s)
            .arg("test")
            .output();

        // Should not panic, even if it returns an error
        assert!(result.is_ok());
    }

    #[test]
    fn test_file_path_handling(
        parts in prop::collection::vec("[a-zA-Z0-9_-]{1,10}", 1..5)
    ) {
        let path = parts.join("/");

        let _result = cmd()
            .arg("--path")
            .arg(&path)
            .output()
            .unwrap();

        // Should handle various path structures without panicking
    }

    #[test]
    fn test_numeric_range_validation(n in -1000i32..1000i32) {
        let result = cmd()
            .arg("--count")
            .arg(n.to_string())
            .output()
            .unwrap();

        if n >= 0 {
            assert!(result.status.success() ||
                String::from_utf8_lossy(&result.stderr).contains("out of range"),
                "Non-negative number should be handled");
        } else {
            assert!(!result.status.success(),
                "Negative number should be rejected");
        }
    }

    #[test]
    fn test_list_argument(items in prop::collection::vec("[a-z]{3,8}", 0..10)) {
        let result = cmd()
            .arg("process")
            .args(&items)
            .output()
            .unwrap();

        // Should handle 0 to many items
        assert!(result.status.success() || result.status.code() == Some(3));
    }
}
```

### 4. Interactive Prompt Tests

Tests for interactive CLI features.

**Generated Tests:**

```rust
// tests/interactive_tests.rs
use assert_cmd::Command;

#[test]
fn test_confirmation_prompt_yes() -> Result<(), Box<dyn std::error::Error>> {
    cmd()
        .arg("delete")
        .arg("resource")
        .write_stdin("yes\n")
        .assert()
        .success()
        .stdout(predicate::str::contains("Deleted"));

    Ok(())
}

#[test]
fn test_confirmation_prompt_no() -> Result<(), Box<dyn std::error::Error>> {
    cmd()
        .arg("delete")
        .arg("resource")
        .write_stdin("no\n")
        .assert()
        .success()
        .stdout(predicate::str::contains("Cancelled"));

    Ok(())
}

#[test]
fn test_yes_flag_skips_prompt() -> Result<(), Box<dyn std::error::Error>> {
    cmd()
        .arg("delete")
        .arg("resource")
        .arg("--yes")
        .assert()
        .success()
        .stdout(predicate::str::contains("Deleted"));

    Ok(())
}

#[test]
fn test_non_interactive_mode() -> Result<(), Box<dyn std::error::Error>> {
    cmd()
        .arg("delete")
        .env("CI", "true")
        .assert()
        .failure()
        .stderr(predicate::str::contains("non-interactive"));

    Ok(())
}
```

### 5. Cross-Platform Tests

Platform-specific tests for compatibility.

**Generated Tests:**

```rust
// tests/cross_platform_tests.rs
use assert_cmd::Command;

#[test]
#[cfg(target_os = "windows")]
fn test_windows_paths() -> Result<(), Box<dyn std::error::Error>> {
    cmd()
        .arg("--path")
        .arg(r"C:\Users\test\file.txt")
        .assert()
        .success();

    Ok(())
}

#[test]
#[cfg(not(target_os = "windows"))]
fn test_unix_paths() -> Result<(), Box<dyn std::error::Error>> {
    cmd()
        .arg("--path")
        .arg("/home/test/file.txt")
        .assert()
        .success();

    Ok(())
}

#[test]
fn test_cross_platform_path_handling() -> Result<(), Box<dyn std::error::Error>> {
    let temp = assert_fs::TempDir::new()?;
    let file = temp.child("test.txt");
    file.write_str("content")?;

    cmd()
        .arg("process")
        .arg(file.path())
        .assert()
        .success();

    temp.close()?;
    Ok(())
}

#[test]
#[cfg(target_os = "windows")]
fn test_windows_line_endings() -> Result<(), Box<dyn std::error::Error>> {
    let temp = assert_fs::TempDir::new()?;
    let input = temp.child("input.txt");
    input.write_str("line1\r\nline2\r\nline3")?;

    cmd()
        .arg("process")
        .arg(input.path())
        .assert()
        .success();

    temp.close()?;
    Ok(())
}
```

## Test Organization

Generated tests are organized into separate files:

```
tests/
├── integration_tests.rs    # Basic integration tests
├── snapshots.rs            # Snapshot tests
├── property_tests.rs       # Property-based tests
├── interactive_tests.rs    # Interactive prompt tests
├── cross_platform_tests.rs # Platform-specific tests
└── snapshots/              # Saved snapshots (insta)
    ├── snapshots__help_output.snap
    ├── snapshots__build_help.snap
    └── ...
```

## Dependencies Added

```toml
[dev-dependencies]
assert_cmd = "2"
assert_fs = "1"
predicates = "3"
insta = "1"
proptest = "1"
```

## Workflow

When you invoke this command:

1. **Analyze CLI Structure**
   - Parse CLI definitions (Clap structure)
   - Identify commands and subcommands
   - Extract argument definitions
   - Find file I/O operations

2. **Generate Test Structure**
   - Create test directory if needed
   - Set up test modules
   - Add necessary dependencies

3. **Generate Tests Based on Type**
   - **Integration**: Tests for each command, success/failure paths
   - **Snapshot**: Capture help text, error messages, formatted output
   - **Property**: Input validation, edge cases
   - **Interactive**: Prompt handling, --yes flag
   - **Cross-platform**: Path handling, line endings

4. **Create Test Fixtures**
   - Sample input files
   - Config files for testing
   - Expected output files

5. **Generate Helper Functions**
   - Command builder helper
   - Common assertions
   - Fixture setup/teardown

6. **Verify Tests**
   - Run generated tests
   - Ensure they pass
   - Report any issues

7. **Generate Documentation**
   - Add comments explaining tests
   - Document test organization
   - Provide examples of adding more tests

## Example Output

```
✓ Analyzed CLI structure
✓ Found 3 commands: init, build, test
✓ Generated integration tests (12 tests)
✓ Generated snapshot tests (8 tests)
✓ Generated property-based tests (5 tests)
✓ Generated interactive tests (4 tests)
✓ Generated cross-platform tests (6 tests)
✓ Added test dependencies to Cargo.toml
✓ Created test fixtures

Test Suite Generated Successfully!

Files created:
  tests/integration_tests.rs    (12 tests)
  tests/snapshots.rs             (8 tests)
  tests/property_tests.rs        (5 tests)
  tests/interactive_tests.rs     (4 tests)
  tests/cross_platform_tests.rs  (6 tests)

Total: 35 tests

Run tests:
  cargo test

Run specific test file:
  cargo test --test integration_tests

Update snapshots (if needed):
  cargo insta review

Coverage:
  • All CLI commands tested
  • Success and failure paths covered
  • Help text snapshots captured
  • Input validation tested
  • Cross-platform compatibility verified

Next steps:
  1. Review generated tests
  2. Run: cargo test
  3. Add custom test cases as needed
  4. Update snapshots: cargo insta review
```

## Implementation

Use the **rust-cli-developer:cli-testing-expert** agent to:

1. Analyze the CLI structure
2. Generate appropriate tests
3. Set up test infrastructure
4. Create fixtures and helpers
5. Verify tests run correctly

Invoke with:

```
Use Task tool with subagent_type="rust-cli-developer:cli-testing-expert"
```

## Notes

- Generated tests are starting points; customize as needed
- Snapshot tests require manual review on first run
- Property tests may need adjustment for specific domains
- Interactive tests require stdin support
- Cross-platform tests should run in CI on multiple platforms
- Tests are non-destructive and use temporary directories

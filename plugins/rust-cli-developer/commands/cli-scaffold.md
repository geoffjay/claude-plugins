---
name: cli-scaffold
description: Scaffold new Rust CLI projects with Clap, error handling, logging, and testing setup
---

# CLI Scaffold Command

Scaffold a new Rust CLI application with best practices, proper structure, and all necessary dependencies configured.

## Arguments

- `$1` - Project name (required)
- `$2` - Project type: "simple", "subcommands", or "plugin" (optional, default: "simple")

## Usage

```bash
# Create a simple single-command CLI
/cli-scaffold my-cli simple

# Create a CLI with subcommands
/cli-scaffold my-cli subcommands

# Create a CLI with plugin architecture
/cli-scaffold my-cli plugin
```

## What Gets Created

The scaffold creates a complete Rust CLI project with:

### Dependencies

- **clap** (v4+) with derive feature for argument parsing
- **anyhow** for error handling in application code
- **thiserror** for library error types
- **miette** for beautiful error messages with diagnostics
- **tracing** + **tracing-subscriber** for structured logging
- **config** for configuration management
- **directories** for XDG directory support
- **serde** for configuration serialization

### Project Structure

```
my-cli/
├── Cargo.toml
├── src/
│   ├── main.rs          # Entry point
│   ├── lib.rs           # Library interface
│   ├── cli.rs           # CLI definitions
│   ├── commands/        # Command implementations
│   │   └── mod.rs
│   ├── config.rs        # Configuration management
│   ├── error.rs         # Error types
│   └── logging.rs       # Logging setup
├── tests/
│   └── integration.rs   # Integration tests
├── config/
│   └── default.toml     # Default configuration
└── README.md
```

### Features

1. **Clean architecture** - Library-first design, thin CLI wrapper
2. **Error handling** - miette for beautiful diagnostics, structured errors
3. **Logging** - Tracing with verbosity levels (-v, -vv, -vvv)
4. **Configuration** - TOML config with precedence (defaults < file < env < CLI)
5. **Testing** - Integration tests with assert_cmd pre-configured
6. **Shell completions** - Built-in completion generation
7. **Cross-platform** - Works on Windows, macOS, Linux

## Workflow

When you invoke this command:

1. **Gather Information**
   - Confirm project name
   - Select project type if not provided
   - Ask about optional features (async support, additional crates)

2. **Create Project Structure**
   - Run `cargo init` to create base project
   - Set up directory structure (src/, tests/, config/)
   - Create all necessary source files

3. **Configure Dependencies**
   - Add all required dependencies to Cargo.toml
   - Configure features appropriately
   - Set up dev-dependencies for testing

4. **Generate Source Files**
   - Create main.rs with proper error handling
   - Set up lib.rs with module exports
   - Create cli.rs with Clap definitions
   - Generate command modules based on project type
   - Set up error types with miette
   - Configure logging with tracing
   - Create configuration management code

5. **Add Testing Infrastructure**
   - Create integration test file
   - Add example tests for CLI commands
   - Configure assert_cmd and assert_fs

6. **Documentation**
   - Generate README.md with usage examples
   - Add inline documentation to code
   - Include configuration examples

7. **Finalize**
   - Run `cargo check` to verify setup
   - Run `cargo test` to ensure tests pass
   - Display next steps to user

## Project Type Details

### Simple CLI

Single command application with arguments and flags.

**Example:**

```rust
// src/cli.rs
use clap::Parser;

#[derive(Parser)]
#[command(name = "my-cli")]
#[command(version, about, long_about = None)]
pub struct Cli {
    /// Input file
    #[arg(short, long)]
    pub input: PathBuf,

    /// Verbosity level
    #[arg(short, long, action = clap::ArgAction::Count)]
    pub verbose: u8,
}
```

### Subcommands CLI

Application with multiple subcommands (like git, cargo).

**Example:**

```rust
// src/cli.rs
use clap::{Parser, Subcommand};

#[derive(Parser)]
pub struct Cli {
    #[arg(short, long, global = true, action = clap::ArgAction::Count)]
    pub verbose: u8,

    #[command(subcommand)]
    pub command: Command,
}

#[derive(Subcommand)]
pub enum Command {
    Init { name: String },
    Build { release: bool },
    Test { filter: Option<String> },
}
```

### Plugin-based CLI

Extensible architecture with plugin system.

**Features:**
- Plugin trait definition
- Plugin registry
- Dynamic plugin loading
- Plugin command routing

## Example Output

After running `/cli-scaffold my-cli subcommands`, you'll see:

```
✓ Created project structure
✓ Configured dependencies
✓ Generated source files
✓ Set up testing infrastructure
✓ Created documentation

Successfully scaffolded 'my-cli'!

Project structure:
  my-cli/
  ├── Cargo.toml
  ├── src/
  │   ├── main.rs
  │   ├── lib.rs
  │   ├── cli.rs
  │   ├── commands/
  │   │   ├── mod.rs
  │   │   ├── init.rs
  │   │   ├── build.rs
  │   │   └── test.rs
  │   ├── config.rs
  │   ├── error.rs
  │   └── logging.rs
  ├── tests/
  │   └── integration.rs
  └── README.md

Next steps:
  cd my-cli
  cargo build
  cargo test
  cargo run -- --help

Features included:
  • Clap v4+ for argument parsing
  • miette for beautiful error messages
  • tracing for structured logging
  • Configuration management (TOML)
  • Integration tests with assert_cmd
  • Shell completion generation

To add your logic:
  1. Edit src/commands/*.rs to implement commands
  2. Add tests in tests/integration.rs
  3. Update config/default.toml if needed

Documentation:
  • See README.md for usage examples
  • Run with --help to see all options
  • Use RUST_LOG=debug for detailed logs
```

## Additional Options

You can customize the scaffold with these options:

- `--async` - Add tokio runtime for async operations
- `--database` - Add sqlx for database support
- `--http` - Add reqwest for HTTP client functionality
- `--template <name>` - Use a custom template

## Implementation

Use the **rust-cli-developer** agent (any of the specialized agents as needed) to:

1. Validate inputs and gather requirements
2. Generate the complete project structure
3. Create all source files with proper implementations
4. Set up testing and documentation
5. Verify the project builds and tests pass

Invoke the agent with:

```
Use Task tool with subagent_type="rust-cli-developer:cli-architect"
```

The agent will handle all the implementation details and ensure the scaffolded project follows best practices for Rust CLI applications.

## Notes

- Projects are created in the current directory
- Will fail if directory already exists (safety check)
- Generated code includes inline documentation
- All dependencies use latest stable versions
- Cross-platform compatibility is ensured
- Follows Rust API guidelines

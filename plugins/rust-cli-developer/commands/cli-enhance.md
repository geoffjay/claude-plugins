---
name: cli-enhance
description: Add features to existing CLI applications like colors, progress bars, shell completions, and better error messages
---

# CLI Enhance Command

Add modern CLI features to an existing Rust CLI application, including colors, progress bars, interactive prompts, shell completions, and beautiful error messages.

## Arguments

- `$1` - Feature to add: "colors", "progress", "prompts", "completions", "errors", "config", "logging", or "all" (required)
- `$2` - Path to project directory (optional, defaults to current directory)

## Usage

```bash
# Add all enhancements
/cli-enhance all

# Add specific feature
/cli-enhance colors
/cli-enhance progress
/cli-enhance completions

# Enhance specific project
/cli-enhance colors /path/to/my-cli
```

## Available Enhancements

### 1. Colors and Styling

Add semantic colors to CLI output using owo-colors.

**What Gets Added:**

- Dependency: `owo-colors`
- Dependency: `supports-color` (for detection)
- Color module with semantic helpers
- NO_COLOR environment variable support
- Terminal capability detection

**Example Implementation:**

```rust
// src/colors.rs
use owo_colors::{OwoColorize, Stream};

pub fn success(message: &str) {
    println!(
        "{} {}",
        "✓".if_supports_color(Stream::Stdout, |text| text.green().bold()),
        message
    );
}

pub fn error(message: &str) {
    eprintln!(
        "{} {}",
        "✗".if_supports_color(Stream::Stderr, |text| text.red().bold()),
        message
    );
}

pub fn warning(message: &str) {
    println!(
        "{} {}",
        "⚠".if_supports_color(Stream::Stdout, |text| text.yellow().bold()),
        message
    );
}

pub fn info(message: &str) {
    println!(
        "{} {}",
        "ℹ".if_supports_color(Stream::Stdout, |text| text.blue().bold()),
        message
    );
}

pub fn supports_color() -> bool {
    use supports_color::Stream as ColorStream;
    supports_color::on(ColorStream::Stdout).is_some()
}
```

**Usage in Code:**

```rust
use crate::colors;

colors::success("Build completed!");
colors::error("Failed to read file");
colors::warning("Configuration incomplete");
colors::info("Processing 10 files");
```

### 2. Progress Bars and Spinners

Add visual feedback for long-running operations using indicatif.

**What Gets Added:**

- Dependency: `indicatif`
- Progress module with common patterns
- Spinner for indeterminate operations
- Progress bars with custom styling
- Multi-progress for parallel tasks

**Example Implementation:**

```rust
// src/progress.rs
use indicatif::{ProgressBar, ProgressStyle, MultiProgress, HumanDuration};
use std::time::Duration;

pub fn create_progress_bar(total: u64) -> ProgressBar {
    let pb = ProgressBar::new(total);
    pb.set_style(
        ProgressStyle::default_bar()
            .template("{spinner:.green} [{elapsed_precise}] [{bar:40.cyan/blue}] {pos}/{len} ({eta})")
            .unwrap()
            .progress_chars("#>-")
    );
    pb
}

pub fn create_spinner(message: &str) -> ProgressBar {
    let spinner = ProgressBar::new_spinner();
    spinner.set_style(
        ProgressStyle::default_spinner()
            .template("{spinner:.green} {msg}")
            .unwrap()
            .tick_strings(&["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
    );
    spinner.set_message(message.to_string());
    spinner
}

pub fn create_multi_progress() -> MultiProgress {
    MultiProgress::new()
}
```

**Usage in Code:**

```rust
use crate::progress;

// Progress bar for known total
let pb = progress::create_progress_bar(100);
for i in 0..100 {
    // Do work
    pb.inc(1);
}
pb.finish_with_message("Complete!");

// Spinner for unknown duration
let spinner = progress::create_spinner("Processing...");
// Do work
spinner.finish_with_message("Done!");
```

### 3. Interactive Prompts

Add user-friendly interactive prompts using dialoguer.

**What Gets Added:**

- Dependency: `dialoguer`
- Prompts module with common patterns
- Confirmation prompts
- Text input with validation
- Selection menus
- Multi-select options

**Example Implementation:**

```rust
// src/prompts.rs
use dialoguer::{
    Confirm, Input, Select, MultiSelect, Password,
    theme::ColorfulTheme
};
use anyhow::Result;

pub fn confirm(prompt: &str, default: bool) -> Result<bool> {
    Ok(Confirm::with_theme(&ColorfulTheme::default())
        .with_prompt(prompt)
        .default(default)
        .interact()?)
}

pub fn input(prompt: &str, default: Option<String>) -> Result<String> {
    let mut input = Input::with_theme(&ColorfulTheme::default())
        .with_prompt(prompt);

    if let Some(d) = default {
        input = input.default(d);
    }

    Ok(input.interact_text()?)
}

pub fn select<T: ToString>(prompt: &str, items: &[T]) -> Result<usize> {
    Ok(Select::with_theme(&ColorfulTheme::default())
        .with_prompt(prompt)
        .items(items)
        .interact()?)
}

pub fn multi_select<T: ToString>(prompt: &str, items: &[T]) -> Result<Vec<usize>> {
    Ok(MultiSelect::with_theme(&ColorfulTheme::default())
        .with_prompt(prompt)
        .items(items)
        .interact()?)
}

pub fn password(prompt: &str, confirm: bool) -> Result<String> {
    if confirm {
        Ok(Password::with_theme(&ColorfulTheme::default())
            .with_prompt(prompt)
            .with_confirmation("Confirm password", "Passwords don't match")
            .interact()?)
    } else {
        Ok(Password::with_theme(&ColorfulTheme::default())
            .with_prompt(prompt)
            .interact()?)
    }
}
```

**Usage in Code:**

```rust
use crate::prompts;

// Confirmation
if prompts::confirm("Continue with deployment?", false)? {
    deploy()?;
}

// Text input
let name = prompts::input("Project name", Some("my-project".to_string()))?;

// Selection
let envs = vec!["dev", "staging", "production"];
let idx = prompts::select("Select environment", &envs)?;
```

### 4. Shell Completions

Add shell completion generation support.

**What Gets Added:**

- Dependency: `clap_complete`
- Completion generation command
- Support for bash, zsh, fish, powershell
- Installation instructions

**Example Implementation:**

```rust
// src/completions.rs
use clap::CommandFactory;
use clap_complete::{generate, Generator, Shell};
use std::io;

pub fn generate_completions<G: Generator>(gen: G) {
    let mut cmd = crate::cli::Cli::command();
    generate(gen, &mut cmd, cmd.get_name().to_string(), &mut io::stdout());
}

pub fn print_install_instructions(shell: Shell) {
    match shell {
        Shell::Bash => {
            eprintln!("To install completions, add to ~/.bashrc:");
            eprintln!("  eval \"$(myapp --generate bash)\"");
        }
        Shell::Zsh => {
            eprintln!("To install completions, add to ~/.zshrc:");
            eprintln!("  eval \"$(myapp --generate zsh)\"");
        }
        Shell::Fish => {
            eprintln!("To install completions:");
            eprintln!("  myapp --generate fish | source");
            eprintln!("  Or save to: ~/.config/fish/completions/myapp.fish");
        }
        Shell::PowerShell => {
            eprintln!("To install completions, add to $PROFILE:");
            eprintln!("  Invoke-Expression (& myapp --generate powershell)");
        }
        _ => {}
    }
}
```

**Add to CLI:**

```rust
// src/cli.rs
use clap::{Parser, ValueEnum};

#[derive(Parser)]
pub struct Cli {
    /// Generate shell completions
    #[arg(long = "generate", value_enum)]
    pub generate: Option<Shell>,

    // ... other fields
}

#[derive(ValueEnum, Clone)]
pub enum Shell {
    Bash,
    Zsh,
    Fish,
    PowerShell,
}
```

### 5. Beautiful Error Messages

Upgrade error handling with miette for rich diagnostics.

**What Gets Added:**

- Dependency: `miette` with `fancy` feature
- Structured error types
- Source code snippets in errors
- Help text and suggestions
- Error URLs

**Example Implementation:**

```rust
// src/error.rs
use miette::{Diagnostic, SourceSpan};
use thiserror::Error;

#[derive(Error, Debug, Diagnostic)]
#[error("Configuration error")]
#[diagnostic(
    code(config::invalid),
    url("https://example.com/docs/config"),
    help("Check your configuration file syntax")
)]
pub struct ConfigError {
    #[source_code]
    pub src: String,

    #[label("this field is invalid")]
    pub span: SourceSpan,

    #[help]
    pub advice: Option<String>,
}

#[derive(Error, Debug, Diagnostic)]
pub enum AppError {
    #[error("File not found: {path}")]
    #[diagnostic(
        code(app::file_not_found),
        help("Check that the file exists and you have permission to read it")
    )]
    FileNotFound {
        path: String,
    },

    #[error("Build failed")]
    #[diagnostic(
        code(app::build_failed),
        help("Run with -vv for detailed logs")
    )]
    BuildFailed {
        #[source]
        source: anyhow::Error,
    },
}
```

**Update main.rs:**

```rust
fn main() -> miette::Result<()> {
    miette::set_panic_hook();

    // Rest of application
}
```

### 6. Configuration Management

Add comprehensive configuration system.

**What Gets Added:**

- Dependency: `config`
- Dependency: `serde`
- Dependency: `toml`
- Dependency: `directories`
- Config module with precedence handling
- XDG directory support
- Environment variable support

**Example Implementation:**

```rust
// src/config.rs
use config::{Config as ConfigBuilder, Environment, File};
use directories::ProjectDirs;
use serde::{Deserialize, Serialize};
use std::path::PathBuf;
use anyhow::Result;

#[derive(Debug, Deserialize, Serialize)]
pub struct Config {
    pub general: General,
    pub features: Features,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct General {
    pub log_level: String,
    pub timeout: u64,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct Features {
    pub colors: bool,
    pub progress: bool,
}

impl Config {
    pub fn load(cli_config: Option<PathBuf>) -> Result<Self> {
        let mut builder = ConfigBuilder::builder()
            .set_default("general.log_level", "info")?
            .set_default("general.timeout", 30)?
            .set_default("features.colors", true)?
            .set_default("features.progress", true)?;

        // Load from standard locations
        if let Some(proj_dirs) = ProjectDirs::from("com", "example", "myapp") {
            let config_dir = proj_dirs.config_dir();
            builder = builder
                .add_source(File::from(config_dir.join("config.toml")).required(false));
        }

        // Override with CLI-specified config
        if let Some(path) = cli_config {
            builder = builder.add_source(File::from(path));
        }

        // Environment variables override everything
        builder = builder.add_source(
            Environment::with_prefix("MYAPP")
                .separator("_")
                .try_parsing(true)
        );

        Ok(builder.build()?.try_deserialize()?)
    }

    pub fn write_default(path: &PathBuf) -> Result<()> {
        let default = Config {
            general: General {
                log_level: "info".to_string(),
                timeout: 30,
            },
            features: Features {
                colors: true,
                progress: true,
            },
        };

        let toml = toml::to_string_pretty(&default)?;
        std::fs::write(path, toml)?;
        Ok(())
    }
}
```

### 7. Structured Logging

Add tracing-based structured logging.

**What Gets Added:**

- Dependency: `tracing`
- Dependency: `tracing-subscriber`
- Logging module with verbosity support
- Structured logging macros

**Example Implementation:**

```rust
// src/logging.rs
use tracing_subscriber::{fmt, prelude::*, EnvFilter};
use anyhow::Result;

pub fn setup(verbosity: u8) -> Result<()> {
    let level = match verbosity {
        0 => "error",
        1 => "warn",
        2 => "info",
        3 => "debug",
        _ => "trace",
    };

    let env_filter = EnvFilter::try_from_default_env()
        .or_else(|_| EnvFilter::try_new(level))?;

    tracing_subscriber::registry()
        .with(fmt::layer().with_target(false).with_level(true))
        .with(env_filter)
        .init();

    Ok(())
}
```

**Usage:**

```rust
use tracing::{info, warn, error, debug};

info!("Starting build process");
debug!("Configuration: {:?}", config);
warn!("Using default value for missing field");
error!("Build failed: {}", error);
```

## Workflow

When you invoke this command:

1. **Analyze Current Project**
   - Detect existing dependencies
   - Identify CLI framework (Clap version)
   - Check for existing features
   - Find integration points

2. **Add Dependencies**
   - Update Cargo.toml with new dependencies
   - Add appropriate feature flags
   - Ensure version compatibility

3. **Generate Code**
   - Create new modules for features
   - Add helper functions and patterns
   - Integrate with existing code

4. **Update Existing Code**
   - Replace println! with colored output
   - Add progress bars to long operations
   - Upgrade error types
   - Add completion generation to CLI

5. **Add Documentation**
   - Document new features in README
   - Add inline code documentation
   - Provide usage examples

6. **Verify Integration**
   - Run cargo check
   - Run tests
   - Test new features

7. **Generate Report**
   - List added features
   - Show usage examples
   - Provide next steps

## Example Output

```
✓ Analyzed project structure
✓ Added dependencies to Cargo.toml
✓ Created colors module (src/colors.rs)
✓ Created progress module (src/progress.rs)
✓ Created prompts module (src/prompts.rs)
✓ Updated CLI for completions
✓ Upgraded error types with miette
✓ Updated 15 call sites with new features
✓ Added documentation

Enhancements Applied Successfully!

Added Features:
  • Colors and styling (owo-colors)
  • Progress bars and spinners (indicatif)
  • Interactive prompts (dialoguer)
  • Shell completions (bash, zsh, fish, powershell)
  • Beautiful error messages (miette)

New Dependencies:
  owo-colors = "4"
  indicatif = "0.17"
  dialoguer = "0.11"
  clap_complete = "4"
  miette = { version = "7", features = ["fancy"] }

Files Modified:
  • Cargo.toml (dependencies added)
  • src/lib.rs (modules exported)
  • src/cli.rs (completion flag added)
  • src/main.rs (error handler updated)

Files Created:
  • src/colors.rs
  • src/progress.rs
  • src/prompts.rs
  • src/completions.rs

Updated Code Locations:
  • src/commands/build.rs (added progress bar)
  • src/commands/init.rs (added prompts)
  • src/error.rs (upgraded to miette)

Usage Examples:

Colors:
  use crate::colors;
  colors::success("Build completed!");
  colors::error("Failed to read file");

Progress:
  use crate::progress;
  let pb = progress::create_progress_bar(100);
  pb.inc(1);
  pb.finish_with_message("Done!");

Prompts:
  use crate::prompts;
  if prompts::confirm("Continue?", true)? {
      // do something
  }

Completions:
  myapp --generate bash > /etc/bash_completion.d/myapp
  myapp --generate zsh > ~/.zfunc/_myapp

Next Steps:
  1. Review generated code
  2. Test new features: cargo run
  3. Update documentation if needed
  4. Commit changes: git add . && git commit
```

## Implementation

Use the appropriate **rust-cli-developer** agents:

```
Use Task tool with subagent_type="rust-cli-developer:cli-ux-specialist"
for colors, progress, and prompts

Use Task tool with subagent_type="rust-cli-developer:cli-architect"
for configuration and logging

Use Task tool with subagent_type="rust-cli-developer:clap-expert"
for shell completions integration
```

## Notes

- Enhancements are additive and non-destructive
- Existing code is updated carefully to maintain functionality
- Dependencies are added with compatible versions
- All changes are tested before completion
- Documentation is updated to reflect new features
- Backward compatibility is maintained where possible

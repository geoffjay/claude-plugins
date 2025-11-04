---
name: tokio-scaffold
description: Scaffold new Tokio projects with proper structure and best practices
---

# Tokio Scaffold Command

This command scaffolds new Tokio-based Rust projects with modern structure, proper dependencies, error handling patterns, tracing infrastructure, and testing setup.

## Arguments

- `$1` - Project name (required)
- `$2` - Project type: `http-server`, `grpc-server`, `tcp-server`, `cli`, or `library` (optional, defaults to `library`)

## Usage

```
/rust-tokio-expert:tokio-scaffold my-service http-server
/rust-tokio-expert:tokio-scaffold my-cli cli
/rust-tokio-expert:tokio-scaffold my-lib library
```

## Workflow

1. **Validate Arguments**
   - Check that project name is provided
   - Validate project type if provided
   - Ensure target directory doesn't already exist

2. **Invoke Agent**
   - Use Task tool with `subagent_type="rust-tokio-expert:tokio-pro"`
   - Pass project name and type to the agent

3. **Agent Instructions**

   The agent should create a complete project structure based on the type:

   ### For HTTP Server Projects

   Create:
   - `Cargo.toml` with dependencies:
     - tokio with full features
     - axum for HTTP framework
     - tower and tower-http for middleware
     - serde and serde_json for serialization
     - tracing and tracing-subscriber for logging
     - anyhow and thiserror for error handling
     - sqlx (optional) for database
     - config for configuration management

   - `src/main.rs` with:
     - Runtime setup with tracing
     - Router configuration
     - Graceful shutdown handling
     - Health check endpoints

   - `src/handlers/mod.rs` with example HTTP handlers
   - `src/error.rs` with custom error types
   - `src/config.rs` with configuration loading
   - `src/telemetry.rs` with tracing setup

   - `tests/integration_test.rs` with API integration tests
   - `.env.example` with configuration template
   - `README.md` with usage instructions

   ### For gRPC Server Projects

   Create:
   - `Cargo.toml` with:
     - tokio with full features
     - tonic and tonic-build
     - prost for protobuf
     - tower for middleware
     - tracing infrastructure
     - error handling crates

   - `proto/service.proto` with example service definition
   - `build.rs` for proto compilation
   - `src/main.rs` with gRPC server setup
   - `src/service.rs` with service implementation
   - `src/error.rs` with error types
   - `tests/integration_test.rs`

   ### For TCP Server Projects

   Create:
   - `Cargo.toml` with:
     - tokio with io-util, net features
     - tokio-util with codec
     - bytes for buffer management
     - tracing infrastructure

   - `src/main.rs` with TCP server setup
   - `src/protocol.rs` with protocol definition
   - `src/handler.rs` with connection handler
   - `tests/integration_test.rs`

   ### For CLI Projects

   Create:
   - `Cargo.toml` with:
     - tokio with full features
     - clap for argument parsing
     - anyhow for error handling
     - tracing-subscriber for logging

   - `src/main.rs` with CLI setup
   - `src/commands/mod.rs` with command structure
   - `src/config.rs` with configuration
   - `tests/cli_test.rs`

   ### For Library Projects

   Create:
   - `Cargo.toml` with:
     - tokio as optional dependency
     - async-trait
     - thiserror for errors

   - `src/lib.rs` with library structure
   - `tests/lib_test.rs` with comprehensive tests
   - `examples/basic.rs` with usage example
   - `README.md` with API documentation

4. **Common Files for All Types**

   - `.gitignore` with Rust-specific ignores
   - `Cargo.toml` with proper metadata
   - `rustfmt.toml` with formatting rules
   - `clippy.toml` with linting configuration (if needed)

5. **Initialize Testing**

   For all project types:
   - Add `#[tokio::test]` examples
   - Include timeout tests
   - Add mock/test utilities
   - Set up test helpers

6. **Documentation**

   Generate `README.md` with:
   - Project description
   - Requirements
   - Installation instructions
   - Usage examples
   - Development setup
   - Testing instructions
   - Contributing guidelines

7. **Verification**

   After scaffolding:
   - Run `cargo check` to verify compilation
   - Run `cargo test` to verify tests
   - Report any issues found

## Example Cargo.toml Template (HTTP Server)

```toml
[package]
name = "{{project_name}}"
version = "0.1.0"
edition = "2021"

[dependencies]
tokio = { version = "1", features = ["full"] }
axum = "0.7"
tower = "0.4"
tower-http = { version = "0.5", features = ["trace", "compression-gzip"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }
anyhow = "1"
thiserror = "1"
config = "0.14"

[dev-dependencies]
tokio-test = "0.4"
```

## Example Main Template (HTTP Server)

```rust
use axum::{Router, routing::get};
use std::net::SocketAddr;
use tower_http::trace::TraceLayer;

mod handlers;
mod error;
mod config;
mod telemetry;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Initialize telemetry
    telemetry::init()?;

    // Load configuration
    let config = config::load()?;

    // Create router
    let app = Router::new()
        .route("/health", get(handlers::health_check))
        .route("/api/v1/users", get(handlers::list_users))
        .layer(TraceLayer::new_for_http());

    // Start server
    let addr = SocketAddr::from(([0, 0, 0, 0], config.port));
    tracing::info!("Starting server on {}", addr);

    let listener = tokio::net::TcpListener::bind(addr).await?;
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await?;

    Ok(())
}

async fn shutdown_signal() {
    tokio::signal::ctrl_c()
        .await
        .expect("failed to install CTRL+C signal handler");
}
```

## Best Practices

The scaffolded project should follow these best practices:

1. **Error Handling**: Use `thiserror` for domain errors, `anyhow` for application errors
2. **Configuration**: Use environment variables with sensible defaults
3. **Logging**: Use `tracing` with structured logging
4. **Testing**: Include both unit and integration tests
5. **Documentation**: Generate comprehensive README with examples
6. **Security**: Include basic security headers and validation
7. **Performance**: Configure runtime appropriately for workload type
8. **Observability**: Include metrics and health check endpoints

## Notes

- Always use the latest stable versions of dependencies
- Include comments explaining key architectural decisions
- Provide both simple and advanced usage examples
- Generate projects that compile and pass tests out of the box
- Follow Rust API guidelines and naming conventions

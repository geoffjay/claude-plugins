---
name: tokio-migrate
description: Migrate synchronous code to async Tokio or upgrade between Tokio versions
---

# Tokio Migrate Command

This command assists with migrating synchronous code to async Tokio, upgrading between Tokio versions, or converting from other async runtimes.

## Arguments

- `$1` - Migration type: `sync-to-async`, `tokio-upgrade`, `runtime-switch` (required)
- `$2` - Target file or directory (optional, defaults to current directory)
- `$3` - Additional context: Tokio version for upgrades, or source runtime for switches (optional)

## Usage

```
/rust-tokio-expert:tokio-migrate sync-to-async src/handlers/
/rust-tokio-expert:tokio-migrate tokio-upgrade src/ 1.0
/rust-tokio-expert:tokio-migrate runtime-switch src/ async-std
```

## Workflow

### 1. Sync to Async Migration

When migrating synchronous code to async Tokio:

#### Analysis Phase

1. **Scan Target Files**
   - Use Glob to find all Rust files in target
   - Read files and identify synchronous operations
   - Detect blocking I/O operations
   - Find CPU-intensive operations
   - Identify thread spawning

2. **Identify Conversion Candidates**
   - Functions with I/O operations (network, file, database)
   - Functions that spawn threads
   - Functions with sleep/delays
   - Functions with synchronous HTTP clients
   - Functions with blocking mutex operations

3. **Analyze Dependencies**
   - Check `Cargo.toml` for sync crates
   - Identify replacements (e.g., `reqwest` blocking → async)
   - Find database drivers needing async versions

#### Migration Phase

4. **Invoke Agent**
   - Use Task tool with `subagent_type="rust-tokio-expert:tokio-pro"`
   - Provide code context and migration plan

5. **Convert Functions to Async**

   The agent should transform:

   **Synchronous Function:**
   ```rust
   use std::fs::File;
   use std::io::Read;

   fn read_config(path: &str) -> Result<String, Error> {
       let mut file = File::open(path)?;
       let mut contents = String::new();
       file.read_to_string(&mut contents)?;
       Ok(contents)
   }
   ```

   **To Async:**
   ```rust
   use tokio::fs::File;
   use tokio::io::AsyncReadExt;

   async fn read_config(path: &str) -> Result<String, Error> {
       let mut file = File::open(path).await?;
       let mut contents = String::new();
       file.read_to_string(&mut contents).await?;
       Ok(contents)
   }
   ```

6. **Replace Blocking Operations**

   Convert common patterns:

   **Thread Sleep → Async Sleep:**
   ```rust
   // Before
   use std::thread;
   use std::time::Duration;

   fn wait() {
       thread::sleep(Duration::from_secs(1));
   }

   // After
   use tokio::time::{sleep, Duration};

   async fn wait() {
       sleep(Duration::from_secs(1)).await;
   }
   ```

   **Std Mutex → Tokio Mutex:**
   ```rust
   // Before
   use std::sync::Mutex;

   fn update_state(mutex: &Mutex<State>) {
       let mut state = mutex.lock().unwrap();
       state.update();
   }

   // After
   use tokio::sync::Mutex;

   async fn update_state(mutex: &Mutex<State>) {
       let mut state = mutex.lock().await;
       state.update();
   }
   ```

   **Thread Spawning → Task Spawning:**
   ```rust
   // Before
   use std::thread;

   fn spawn_worker() {
       thread::spawn(|| {
           do_work();
       });
   }

   // After
   use tokio::task;

   async fn spawn_worker() {
       task::spawn(async {
           do_work().await;
       });
   }
   ```

7. **Update Dependencies in Cargo.toml**

   Replace sync crates:
   ```toml
   # Before
   [dependencies]
   reqwest = { version = "0.11", features = ["blocking"] }

   # After
   [dependencies]
   reqwest = "0.11"
   tokio = { version = "1", features = ["full"] }
   ```

8. **Add Runtime Setup**

   Add to main.rs:
   ```rust
   #[tokio::main]
   async fn main() -> Result<(), Box<dyn std::error::Error>> {
       // Your async code
       Ok(())
   }
   ```

9. **Handle CPU-Intensive Operations**

   Wrap in `spawn_blocking`:
   ```rust
   async fn process_data(data: Vec<u8>) -> Result<Vec<u8>, Error> {
       // CPU-intensive work
       let result = tokio::task::spawn_blocking(move || {
           expensive_computation(data)
       }).await?;

       Ok(result)
   }
   ```

### 2. Tokio Version Upgrade

When upgrading between Tokio versions (e.g., 0.2 → 1.x):

#### Analysis Phase

1. **Detect Current Version**
   - Read `Cargo.toml`
   - Identify current Tokio version
   - Check dependent crates versions

2. **Identify Breaking Changes**
   - Scan for deprecated APIs
   - Find removed features
   - Detect renamed functions

#### Migration Phase

3. **Update Cargo.toml**

   ```toml
   # From Tokio 0.2
   [dependencies]
   tokio = { version = "0.2", features = ["macros", "rt-threaded"] }

   # To Tokio 1.x
   [dependencies]
   tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
   ```

4. **Update Runtime Setup**

   ```rust
   // Tokio 0.2
   #[tokio::main]
   async fn main() {
       // ...
   }

   // Tokio 1.x (same, but verify features)
   #[tokio::main]
   async fn main() {
       // ...
   }
   ```

5. **Fix API Changes**

   Common migrations:

   **Timer API:**
   ```rust
   // Tokio 0.2
   use tokio::time::delay_for;
   delay_for(Duration::from_secs(1)).await;

   // Tokio 1.x
   use tokio::time::sleep;
   sleep(Duration::from_secs(1)).await;
   ```

   **Timeout API:**
   ```rust
   // Tokio 0.2
   use tokio::time::timeout_at;

   // Tokio 1.x
   use tokio::time::timeout;
   ```

   **Signal Handling:**
   ```rust
   // Tokio 0.2
   use tokio::signal::ctrl_c;

   // Tokio 1.x (same, but improved)
   use tokio::signal::ctrl_c;
   ```

6. **Update Feature Flags**

   Map old features to new:
   - `rt-threaded` → `rt-multi-thread`
   - `rt-core` → `rt`
   - `tcp` → `net`
   - `dns` → removed (use async DNS crates)

### 3. Runtime Switch

When switching from other runtimes (async-std, smol) to Tokio:

#### Analysis Phase

1. **Identify Runtime-Specific Code**
   - Find runtime initialization
   - Detect runtime-specific APIs
   - Identify spawning patterns

#### Migration Phase

2. **Replace Runtime Setup**

   **From async-std:**
   ```rust
   // Before
   #[async_std::main]
   async fn main() {
       // ...
   }

   // After
   #[tokio::main]
   async fn main() {
       // ...
   }
   ```

3. **Update Spawning**

   ```rust
   // async-std
   use async_std::task;
   task::spawn(async { /* ... */ });

   // Tokio
   use tokio::task;
   task::spawn(async { /* ... */ });
   ```

4. **Replace I/O Types**

   ```rust
   // async-std
   use async_std::net::TcpListener;

   // Tokio
   use tokio::net::TcpListener;
   ```

5. **Update Dependencies**

   Replace runtime-specific crates:
   ```toml
   # Remove
   async-std = "1"

   # Add
   tokio = { version = "1", features = ["full"] }
   ```

### Common Migration Tasks

For all migration types:

1. **Update Tests**
   ```rust
   // Before
   #[async_std::test]
   async fn test_something() { }

   // After
   #[tokio::test]
   async fn test_something() { }
   ```

2. **Update Error Handling**
   - Ensure error types work with async
   - Add proper error context
   - Use `?` operator appropriately

3. **Add Tracing**
   - Instrument key functions
   - Add structured logging
   - Set up tracing subscriber

4. **Verification**
   - Run `cargo check`
   - Run `cargo test`
   - Run `cargo clippy`
   - Verify no blocking operations remain

## Migration Checklist

- [ ] All I/O operations are async
- [ ] No `std::thread::sleep` usage
- [ ] No `std::sync::Mutex` in async code
- [ ] CPU-intensive work uses `spawn_blocking`
- [ ] Runtime properly configured
- [ ] Tests updated to use `#[tokio::test]`
- [ ] Dependencies updated in Cargo.toml
- [ ] Error handling verified
- [ ] Documentation updated
- [ ] Performance tested

## Incremental Migration Strategy

For large codebases:

1. **Identify Migration Boundaries**
   - Start with leaf functions (no callers)
   - Move up the call graph gradually
   - Create async versions alongside sync

2. **Bridge Sync and Async**
   ```rust
   // Call async from sync
   fn sync_wrapper() -> Result<T, Error> {
       let rt = tokio::runtime::Runtime::new()?;
       rt.block_on(async_function())
   }

   // Call sync from async (CPU-intensive)
   async fn async_wrapper() -> Result<T, Error> {
       tokio::task::spawn_blocking(|| {
           sync_function()
       }).await?
   }
   ```

3. **Migration Order**
   - I/O layer first
   - Business logic second
   - API/handlers last
   - Tests continuously

## Best Practices

1. **Don't Mix Sync and Async I/O**: Choose one model
2. **Use spawn_blocking**: For blocking operations you can't convert
3. **Test Thoroughly**: Async bugs can be subtle
4. **Profile Performance**: Measure before and after
5. **Update Documentation**: Note async requirements
6. **Handle Cancellation**: Implement proper cleanup
7. **Consider Backpressure**: Add flow control

## Notes

- Migration is often incremental - don't try to do everything at once
- Test each migration step thoroughly
- Consider performance implications of async
- Some operations may not benefit from async
- Document breaking changes for API consumers

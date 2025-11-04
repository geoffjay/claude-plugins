---
name: tokio-test
description: Generate comprehensive async tests for Tokio applications
---

# Tokio Test Command

This command generates comprehensive async tests for Tokio applications, including unit tests, integration tests, benchmarks, and property-based tests.

## Arguments

- `$1` - Target to generate tests for: file path, module name, or function name (required)
- `$2` - Test type: `unit`, `integration`, `benchmark`, or `all` (optional, defaults to `unit`)

## Usage

```
/rust-tokio-expert:tokio-test src/handlers/user.rs
/rust-tokio-expert:tokio-test src/service.rs integration
/rust-tokio-expert:tokio-test process_request benchmark
/rust-tokio-expert:tokio-test src/api/ all
```

## Workflow

1. **Parse Arguments**
   - Validate target is provided
   - Determine test type (unit, integration, benchmark, all)
   - Identify target scope (file, module, or function)

2. **Analyze Target Code**
   - Read the target file(s) using Read tool
   - Identify async functions to test
   - Analyze function signatures and dependencies
   - Detect error types and return values

3. **Invoke Agent**
   - Use Task tool with `subagent_type="rust-tokio-expert:tokio-pro"`
   - Provide code context and test requirements
   - Request test generation based on type

4. **Generate Unit Tests**

   For each async function, create tests covering:

   ### Happy Path Tests
   ```rust
   #[tokio::test]
   async fn test_process_user_success() {
       // Arrange
       let user_id = 1;
       let expected_name = "John Doe";

       // Act
       let result = process_user(user_id).await;

       // Assert
       assert!(result.is_ok());
       let user = result.unwrap();
       assert_eq!(user.name, expected_name);
   }
   ```

   ### Error Handling Tests
   ```rust
   #[tokio::test]
   async fn test_process_user_not_found() {
       let result = process_user(999).await;

       assert!(result.is_err());
       assert!(matches!(result.unwrap_err(), Error::NotFound));
   }
   ```

   ### Timeout Tests
   ```rust
   #[tokio::test]
   async fn test_operation_completes_within_timeout() {
       use tokio::time::{timeout, Duration};

       let result = timeout(
           Duration::from_secs(5),
           slow_operation()
       ).await;

       assert!(result.is_ok(), "Operation timed out");
   }
   ```

   ### Concurrent Execution Tests
   ```rust
   #[tokio::test]
   async fn test_concurrent_processing() {
       let handles: Vec<_> = (0..10)
           .map(|i| tokio::spawn(process_item(i)))
           .collect();

       let results: Vec<_> = futures::future::join_all(handles)
           .await
           .into_iter()
           .map(|r| r.unwrap())
           .collect();

       assert_eq!(results.len(), 10);
       assert!(results.iter().all(|r| r.is_ok()));
   }
   ```

   ### Mock Tests
   ```rust
   #[cfg(test)]
   mod tests {
       use super::*;
       use mockall::predicate::*;
       use mockall::mock;

       mock! {
           UserRepository {}

           #[async_trait::async_trait]
           impl UserRepository for UserRepository {
               async fn find_by_id(&self, id: u64) -> Result<User, Error>;
           }
       }

       #[tokio::test]
       async fn test_with_mock_repository() {
           let mut mock_repo = MockUserRepository::new();
           mock_repo
               .expect_find_by_id()
               .with(eq(1))
               .times(1)
               .returning(|_| Ok(User { id: 1, name: "Test".into() }));

           let service = UserService::new(Box::new(mock_repo));
           let user = service.get_user(1).await.unwrap();

           assert_eq!(user.name, "Test");
       }
   }
   ```

5. **Generate Integration Tests**

   Create `tests/integration_test.rs` with:

   ### API Integration Tests
   ```rust
   use tokio::net::TcpListener;

   #[tokio::test]
   async fn test_http_endpoint() {
       // Start test server
       let listener = TcpListener::bind("127.0.0.1:0").await.unwrap();
       let addr = listener.local_addr().unwrap();

       tokio::spawn(async move {
           run_server(listener).await.unwrap();
       });

       // Make request
       let client = reqwest::Client::new();
       let response = client
           .get(format!("http://{}/health", addr))
           .send()
           .await
           .unwrap();

       assert_eq!(response.status(), 200);
   }
   ```

   ### Database Integration Tests
   ```rust
   #[tokio::test]
   async fn test_database_operations() {
       let pool = create_test_pool().await;

       // Insert test data
       let user = User { id: 1, name: "Test".into() };
       save_user(&pool, &user).await.unwrap();

       // Verify
       let fetched = find_user(&pool, 1).await.unwrap();
       assert_eq!(fetched.unwrap().name, "Test");

       // Cleanup
       cleanup_test_data(&pool).await;
   }
   ```

   ### End-to-End Tests
   ```rust
   #[tokio::test]
   async fn test_complete_workflow() {
       // Setup
       let app = create_test_app().await;

       // Create user
       let create_response = app.create_user("John").await.unwrap();
       let user_id = create_response.id;

       // Fetch user
       let user = app.get_user(user_id).await.unwrap();
       assert_eq!(user.name, "John");

       // Update user
       app.update_user(user_id, "Jane").await.unwrap();

       // Verify update
       let updated = app.get_user(user_id).await.unwrap();
       assert_eq!(updated.name, "Jane");

       // Delete user
       app.delete_user(user_id).await.unwrap();

       // Verify deletion
       let deleted = app.get_user(user_id).await;
       assert!(deleted.is_err());
   }
   ```

6. **Generate Benchmarks**

   Create `benches/async_bench.rs` with:

   ```rust
   use criterion::{criterion_group, criterion_main, Criterion, BenchmarkId};
   use tokio::runtime::Runtime;

   fn benchmark_async_operations(c: &mut Criterion) {
       let rt = Runtime::new().unwrap();

       let mut group = c.benchmark_group("async-operations");

       // Throughput benchmark
       for size in [10, 100, 1000].iter() {
           group.throughput(criterion::Throughput::Elements(*size as u64));
           group.bench_with_input(
               BenchmarkId::from_parameter(size),
               size,
               |b, &size| {
                   b.to_async(&rt).iter(|| async move {
                       process_batch(size).await
                   });
               },
           );
       }

       // Latency benchmark
       group.bench_function("single_request", |b| {
           b.to_async(&rt).iter(|| async {
               process_request().await
           });
       });

       // Concurrent operations
       group.bench_function("concurrent_10", |b| {
           b.to_async(&rt).iter(|| async {
               let handles: Vec<_> = (0..10)
                   .map(|_| tokio::spawn(process_request()))
                   .collect();

               for handle in handles {
                   handle.await.unwrap();
               }
           });
       });

       group.finish();
   }

   criterion_group!(benches, benchmark_async_operations);
   criterion_main!(benches);
   ```

7. **Generate Test Utilities**

   Create `tests/common/mod.rs` with helpers:

   ```rust
   use tokio::runtime::Runtime;

   pub fn create_test_runtime() -> Runtime {
       Runtime::new().unwrap()
   }

   pub async fn setup_test_database() -> TestDb {
       // Create test database
       // Run migrations
       // Return handle
   }

   pub async fn cleanup_test_database(db: TestDb) {
       // Drop test database
   }

   pub struct TestApp {
       // Application state for testing
   }

   impl TestApp {
       pub async fn new() -> Self {
           // Initialize test application
       }

       pub async fn cleanup(self) {
           // Cleanup resources
       }
   }
   ```

8. **Add Test Configuration**

   Update `Cargo.toml` with test dependencies:

   ```toml
   [dev-dependencies]
   tokio-test = "0.4"
   mockall = "0.12"
   criterion = { version = "0.5", features = ["async_tokio"] }
   proptest = "1"
   futures = "0.3"
   ```

9. **Generate Property-Based Tests**

   For appropriate functions:

   ```rust
   use proptest::prelude::*;

   proptest! {
       #[test]
       fn test_parse_always_succeeds(input in "\\PC*") {
           let rt = tokio::runtime::Runtime::new().unwrap();
           rt.block_on(async {
               let result = parse_input(&input).await;
               assert!(result.is_ok() || result.is_err());
           });
       }
   }
   ```

10. **Run and Verify Tests**

    After generation:
    - Run `cargo test` to verify tests compile and pass
    - Run `cargo bench` to verify benchmarks work
    - Report coverage gaps if any
    - Suggest additional test cases if needed

## Test Categories

Generate tests for:

1. **Functional Correctness**
   - Happy path scenarios
   - Edge cases
   - Error conditions
   - Boundary values

2. **Concurrency**
   - Race conditions
   - Deadlocks
   - Task spawning
   - Shared state access

3. **Performance**
   - Throughput
   - Latency
   - Resource usage
   - Scalability

4. **Reliability**
   - Error recovery
   - Timeout handling
   - Retry logic
   - Graceful degradation

5. **Integration**
   - API endpoints
   - Database operations
   - External services
   - End-to-end workflows

## Best Practices

Generated tests should:

1. Use descriptive test names that explain what is being tested
2. Follow Arrange-Act-Assert pattern
3. Be independent and idempotent
4. Clean up resources properly
5. Use appropriate timeouts
6. Include helpful assertion messages
7. Mock external dependencies
8. Test both success and failure paths
9. Use `#[tokio::test]` for async tests
10. Configure runtime appropriately for test type

## Example Test Organization

```
tests/
├── common/
│   ├── mod.rs           # Shared test utilities
│   └── fixtures.rs      # Test data fixtures
├── integration_test.rs   # API integration tests
├── database_test.rs      # Database integration tests
└── e2e_test.rs          # End-to-end tests

benches/
├── throughput.rs        # Throughput benchmarks
└── latency.rs           # Latency benchmarks
```

## Notes

- Generate tests that are maintainable and easy to understand
- Include comments explaining complex test scenarios
- Provide setup and teardown helpers
- Use realistic test data
- Consider using test fixtures for consistency
- Document any test-specific configuration needed

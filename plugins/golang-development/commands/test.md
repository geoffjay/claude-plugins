---
name: golang-development:test
description: Generate comprehensive tests including unit tests, table-driven tests, benchmarks, and examples with high coverage
---

# Golang Development Test Command

Generate comprehensive, production-ready tests for Go code including unit tests, table-driven tests, benchmarks, and examples.

## Usage

```bash
/golang-development:test <file-or-function> [test-type] [options]
```

## Arguments

- `$1` - File path or function name to test (required)
- `$2` - Test type: `unit`, `table`, `benchmark`, `integration`, `all` (optional, defaults to `unit`)
- `$3` - Options as JSON (optional)

## Examples

```bash
# Generate unit tests for a file
/golang-development:test internal/service/user.go

# Generate table-driven tests
/golang-development:test internal/service/user.go table

# Generate benchmarks
/golang-development:test internal/service/user.go benchmark

# Generate all test types
/golang-development:test internal/service/user.go all

# Generate tests with options
/golang-development:test internal/service/user.go unit '{"with_mocks": true, "coverage_target": 90}'
```

## Test Types

### 1. Unit Tests

Basic unit tests for individual functions:

```go
// Source: user.go
package service

type User struct {
    ID    string
    Email string
    Age   int
}

func (u *User) IsAdult() bool {
    return u.Age >= 18
}

func ValidateEmail(email string) error {
    if !strings.Contains(email, "@") {
        return errors.New("invalid email format")
    }
    return nil
}

// Generated: user_test.go
package service

import (
    "testing"
)

func TestUser_IsAdult(t *testing.T) {
    t.Run("adult user", func(t *testing.T) {
        user := &User{Age: 25}
        if !user.IsAdult() {
            t.Error("expected user to be adult")
        }
    })

    t.Run("minor user", func(t *testing.T) {
        user := &User{Age: 15}
        if user.IsAdult() {
            t.Error("expected user to be minor")
        }
    })

    t.Run("edge case - exactly 18", func(t *testing.T) {
        user := &User{Age: 18}
        if !user.IsAdult() {
            t.Error("18 year old should be adult")
        }
    })
}

func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name    string
        email   string
        wantErr bool
    }{
        {
            name:    "valid email",
            email:   "user@example.com",
            wantErr: false,
        },
        {
            name:    "invalid email - no @",
            email:   "userexample.com",
            wantErr: true,
        },
        {
            name:    "empty email",
            email:   "",
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := ValidateEmail(tt.email)
            if (err != nil) != tt.wantErr {
                t.Errorf("ValidateEmail() error = %v, wantErr %v", err, tt.wantErr)
            }
        })
    }
}
```

### 2. Table-Driven Tests

Comprehensive table-driven tests:

```go
// Source: calculator.go
package calculator

func Add(a, b int) int {
    return a + b
}

func Divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

// Generated: calculator_test.go
package calculator

import (
    "math"
    "testing"
)

func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a        int
        b        int
        expected int
    }{
        {"positive numbers", 2, 3, 5},
        {"negative numbers", -2, -3, -5},
        {"mixed signs", -2, 3, 1},
        {"zeros", 0, 0, 0},
        {"large numbers", 1000000, 2000000, 3000000},
        {"overflow scenario", math.MaxInt - 1, 1, math.MaxInt},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d",
                    tt.a, tt.b, result, tt.expected)
            }
        })
    }
}

func TestDivide(t *testing.T) {
    tests := []struct {
        name      string
        a         float64
        b         float64
        expected  float64
        expectErr bool
    }{
        {"normal division", 10.0, 2.0, 5.0, false},
        {"division by zero", 10.0, 0.0, 0.0, true},
        {"negative numbers", -10.0, 2.0, -5.0, false},
        {"fractional result", 7.0, 2.0, 3.5, false},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result, err := Divide(tt.a, tt.b)

            if tt.expectErr {
                if err == nil {
                    t.Error("expected error but got none")
                }
                return
            }

            if err != nil {
                t.Errorf("unexpected error: %v", err)
                return
            }

            if math.Abs(result-tt.expected) > 0.0001 {
                t.Errorf("Divide(%f, %f) = %f; want %f",
                    tt.a, tt.b, result, tt.expected)
            }
        })
    }
}
```

### 3. Benchmarks

Performance benchmarks:

```go
// Generated: user_bench_test.go
package service

import (
    "testing"
)

func BenchmarkUser_IsAdult(b *testing.B) {
    user := &User{Age: 25}

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        _ = user.IsAdult()
    }
}

func BenchmarkValidateEmail(b *testing.B) {
    email := "test@example.com"

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        _ = ValidateEmail(email)
    }
}

func BenchmarkValidateEmail_Invalid(b *testing.B) {
    email := "invalid-email"

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        _ = ValidateEmail(email)
    }
}

// Memory allocation benchmarks
func BenchmarkStringConcatenation(b *testing.B) {
    strs := []string{"hello", "world", "foo", "bar"}

    b.Run("operator", func(b *testing.B) {
        b.ReportAllocs()
        for i := 0; i < b.N; i++ {
            result := ""
            for _, s := range strs {
                result += s
            }
            _ = result
        }
    })

    b.Run("strings.Builder", func(b *testing.B) {
        b.ReportAllocs()
        for i := 0; i < b.N; i++ {
            var sb strings.Builder
            for _, s := range strs {
                sb.WriteString(s)
            }
            _ = sb.String()
        }
    })
}
```

### 4. Integration Tests

Integration tests with external dependencies:

```go
// Generated: user_integration_test.go
// +build integration

package service

import (
    "context"
    "database/sql"
    "testing"

    _ "github.com/lib/pq"
)

func setupTestDB(t *testing.T) *sql.DB {
    t.Helper()

    db, err := sql.Open("postgres", "postgres://test:test@localhost/test?sslmode=disable")
    if err != nil {
        t.Fatalf("failed to connect to database: %v", err)
    }

    // Create schema
    _, err = db.Exec(`CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        age INTEGER NOT NULL
    )`)
    if err != nil {
        t.Fatalf("failed to create schema: %v", err)
    }

    t.Cleanup(func() {
        db.Exec("DROP TABLE users")
        db.Close()
    })

    return db
}

func TestUserRepository_Create_Integration(t *testing.T) {
    if testing.Short() {
        t.Skip("skipping integration test in short mode")
    }

    db := setupTestDB(t)
    repo := NewUserRepository(db)

    ctx := context.Background()
    user := &User{
        Email: "test@example.com",
        Age:   25,
    }

    err := repo.Create(ctx, user)
    if err != nil {
        t.Fatalf("failed to create user: %v", err)
    }

    if user.ID == "" {
        t.Error("expected user ID to be set")
    }

    // Verify user was created
    retrieved, err := repo.GetByEmail(ctx, user.Email)
    if err != nil {
        t.Fatalf("failed to retrieve user: %v", err)
    }

    if retrieved.Email != user.Email {
        t.Errorf("email mismatch: got %s, want %s", retrieved.Email, user.Email)
    }
}
```

### 5. Mock Generation

Generate mocks for interfaces:

```go
// Source: repository.go
package service

type UserRepository interface {
    GetByID(ctx context.Context, id string) (*User, error)
    Create(ctx context.Context, user *User) error
    Update(ctx context.Context, user *User) error
    Delete(ctx context.Context, id string) error
}

// Generated: mocks/user_repository_mock.go
package mocks

import (
    "context"
    "sync"

    "yourmodule/service"
)

type MockUserRepository struct {
    mu sync.Mutex

    GetByIDFunc func(ctx context.Context, id string) (*service.User, error)
    GetByIDCalls []GetByIDCall

    CreateFunc func(ctx context.Context, user *service.User) error
    CreateCalls []CreateCall

    UpdateFunc func(ctx context.Context, user *service.User) error
    UpdateCalls []UpdateCall

    DeleteFunc func(ctx context.Context, id string) error
    DeleteCalls []DeleteCall
}

type GetByIDCall struct {
    Ctx context.Context
    ID  string
}

type CreateCall struct {
    Ctx  context.Context
    User *service.User
}

// ... more types ...

func (m *MockUserRepository) GetByID(ctx context.Context, id string) (*service.User, error) {
    m.mu.Lock()
    m.GetByIDCalls = append(m.GetByIDCalls, GetByIDCall{Ctx: ctx, ID: id})
    m.mu.Unlock()

    if m.GetByIDFunc != nil {
        return m.GetByIDFunc(ctx, id)
    }

    return nil, nil
}

// ... more methods ...

// Usage in tests:
func TestUserService_GetUser(t *testing.T) {
    mockRepo := &mocks.MockUserRepository{
        GetByIDFunc: func(ctx context.Context, id string) (*service.User, error) {
            return &service.User{
                ID:    id,
                Email: "test@example.com",
                Age:   25,
            }, nil
        },
    }

    svc := service.NewUserService(mockRepo)
    user, err := svc.GetUser(context.Background(), "123")

    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }

    if user.ID != "123" {
        t.Errorf("expected user ID 123, got %s", user.ID)
    }

    if len(mockRepo.GetByIDCalls) != 1 {
        t.Errorf("expected 1 call to GetByID, got %d", len(mockRepo.GetByIDCalls))
    }
}
```

## Test Helpers

Generate common test helpers:

```go
// Generated: testhelpers/helpers.go
package testhelpers

import (
    "testing"
    "time"
)

// AssertEqual checks if two values are equal
func AssertEqual(t *testing.T, got, want interface{}) {
    t.Helper()
    if got != want {
        t.Errorf("got %v, want %v", got, want)
    }
}

// AssertError checks if an error occurred
func AssertError(t *testing.T, err error, wantErr bool) {
    t.Helper()
    if (err != nil) != wantErr {
        t.Errorf("error = %v, wantErr %v", err, wantErr)
    }
}

// AssertNil checks if value is nil
func AssertNil(t *testing.T, got interface{}) {
    t.Helper()
    if got != nil {
        t.Errorf("expected nil, got %v", got)
    }
}

// AssertNotNil checks if value is not nil
func AssertNotNil(t *testing.T, got interface{}) {
    t.Helper()
    if got == nil {
        t.Error("expected non-nil value")
    }
}

// Eventually retries assertion until timeout
func Eventually(t *testing.T, assertion func() bool, timeout time.Duration) {
    t.Helper()
    deadline := time.Now().Add(timeout)

    for time.Now().Before(deadline) {
        if assertion() {
            return
        }
        time.Sleep(100 * time.Millisecond)
    }

    t.Error("assertion failed within timeout")
}
```

## Configuration Options

```json
{
  "with_mocks": true,
  "with_benchmarks": true,
  "with_examples": true,
  "coverage_target": 80,
  "use_testify": false,
  "parallel_tests": true,
  "generate_helpers": true
}
```

## Coverage Analysis

The command includes coverage analysis:

```bash
# Run tests with coverage
go test -coverprofile=coverage.out ./...

# View coverage report
go tool cover -html=coverage.out

# Check coverage threshold
go test -cover ./... | grep "coverage:"
```

## Best Practices

Generated tests follow:
- Table-driven test patterns
- Subtests for isolation
- Test helpers for DRY code
- Proper cleanup with t.Cleanup()
- Context usage in tests
- Parallel test execution
- Comprehensive edge cases
- Clear test names

## When to Use

Use this command to:
- Generate tests for new code
- Improve test coverage
- Add missing test cases
- Create benchmark tests
- Generate integration tests
- Mock external dependencies
- Follow testing best practices

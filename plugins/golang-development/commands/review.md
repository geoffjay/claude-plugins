---
name: golang-development:review
description: Review Go code for idiomatic patterns, performance issues, security vulnerabilities, and common pitfalls with actionable suggestions
---

# Golang Development Review Command

Comprehensive Go code review focusing on idiomatic patterns, performance, security, and best practices.

## Usage

```bash
/golang-development:review [file-path-or-directory] [focus-area]
```

## Arguments

- `$1` - File path or directory to review (optional, defaults to current directory)
- `$2` - Focus area: `all`, `idioms`, `performance`, `security`, `concurrency`, `errors` (optional, defaults to `all`)

## Examples

```bash
# Review all files in current directory
/golang-development:review

# Review specific file
/golang-development:review internal/service/user.go

# Focus on performance issues
/golang-development:review . performance

# Focus on security
/golang-development:review ./handlers security

# Review concurrency patterns
/golang-development:review . concurrency
```

## Review Categories

### 1. Idiomatic Go (`idioms`)

**Checks:**
- Naming conventions (camelCase, capitalization)
- Error handling patterns
- Interface usage and design
- Struct composition over inheritance
- Receiver naming and types
- Exported vs. unexported identifiers
- Go proverbs adherence

**Example Issues:**
```go
// ❌ BAD: Non-idiomatic error handling
func getUser(id string) (*User, string) {
    if id == "" {
        return nil, "invalid ID"
    }
    // ...
}

// ✅ GOOD: Idiomatic error handling
func GetUser(id string) (*User, error) {
    if id == "" {
        return nil, fmt.Errorf("invalid ID: %s", id)
    }
    // ...
}

// ❌ BAD: Getter naming
func (u *User) GetName() string {
    return u.name
}

// ✅ GOOD: Idiomatic getter
func (u *User) Name() string {
    return u.name
}

// ❌ BAD: Setter without validation
func (u *User) SetAge(age int) {
    u.age = age
}

// ✅ GOOD: Validated setter with error
func (u *User) SetAge(age int) error {
    if age < 0 || age > 150 {
        return fmt.Errorf("invalid age: %d", age)
    }
    u.age = age
    return nil
}
```

### 2. Performance (`performance`)

**Checks:**
- Unnecessary allocations
- String concatenation in loops
- Slice pre-allocation
- Map pre-allocation
- Defer in loops
- Inefficient algorithms
- Memory leaks
- Goroutine leaks

**Example Issues:**
```go
// ❌ BAD: String concatenation in loop
func concat(strs []string) string {
    result := ""
    for _, s := range strs {
        result += s  // Allocates new string each time
    }
    return result
}

// ✅ GOOD: Use strings.Builder
func concat(strs []string) string {
    var sb strings.Builder
    for _, s := range strs {
        sb.WriteString(s)
    }
    return sb.String()
}

// ❌ BAD: Growing slice
func process(n int) []int {
    var result []int
    for i := 0; i < n; i++ {
        result = append(result, i)
    }
    return result
}

// ✅ GOOD: Pre-allocate
func process(n int) []int {
    result := make([]int, 0, n)
    for i := 0; i < n; i++ {
        result = append(result, i)
    }
    return result
}

// ❌ BAD: Defer in tight loop
for i := 0; i < 10000; i++ {
    mu.Lock()
    defer mu.Unlock()  // Defers accumulate
    // ...
}

// ✅ GOOD: Explicit unlock
for i := 0; i < 10000; i++ {
    mu.Lock()
    // ...
    mu.Unlock()
}
```

### 3. Security (`security`)

**Checks:**
- SQL injection vulnerabilities
- Command injection
- Path traversal
- Hardcoded credentials
- Weak cryptography
- Unsafe operations
- Input validation
- XSS vulnerabilities

**Example Issues:**
```go
// ❌ BAD: SQL injection
func getUser(db *sql.DB, username string) (*User, error) {
    query := fmt.Sprintf("SELECT * FROM users WHERE username = '%s'", username)
    return db.Query(query)
}

// ✅ GOOD: Parameterized query
func getUser(db *sql.DB, username string) (*User, error) {
    query := "SELECT * FROM users WHERE username = $1"
    return db.Query(query, username)
}

// ❌ BAD: Hardcoded credentials
const apiKey = "sk_live_1234567890"

// ✅ GOOD: Environment variables
apiKey := os.Getenv("API_KEY")

// ❌ BAD: Weak random
func generateToken() string {
    return fmt.Sprintf("%d", rand.Int())
}

// ✅ GOOD: Cryptographically secure random
func generateToken() (string, error) {
    b := make([]byte, 32)
    if _, err := rand.Read(b); err != nil {
        return "", err
    }
    return base64.URLEncoding.EncodeToString(b), nil
}
```

### 4. Concurrency (`concurrency`)

**Checks:**
- Race conditions
- Deadlock potential
- Missing mutex protection
- Channel misuse
- Context propagation
- Goroutine leaks
- Improper synchronization
- Lock contention

**Example Issues:**
```go
// ❌ BAD: Race condition
type Counter struct {
    count int
}

func (c *Counter) Increment() {
    c.count++  // Not thread-safe
}

// ✅ GOOD: Protected with mutex
type Counter struct {
    mu    sync.Mutex
    count int
}

func (c *Counter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count++
}

// ❌ BAD: Goroutine leak
func fetchData(url string) <-chan Result {
    ch := make(chan Result)
    go func() {
        // If this fails, goroutine leaks
        data := fetch(url)
        ch <- data
    }()
    return ch
}

// ✅ GOOD: Context for cancellation
func fetchData(ctx context.Context, url string) <-chan Result {
    ch := make(chan Result)
    go func() {
        defer close(ch)
        select {
        case <-ctx.Done():
            return
        default:
            data := fetch(url)
            select {
            case ch <- data:
            case <-ctx.Done():
            }
        }
    }()
    return ch
}
```

### 5. Error Handling (`errors`)

**Checks:**
- Ignored errors
- Error wrapping
- Sentinel errors
- Custom error types
- Error messages
- Panic usage
- Recover usage

**Example Issues:**
```go
// ❌ BAD: Ignored error
file, _ := os.Open("file.txt")

// ✅ GOOD: Handle error
file, err := os.Open("file.txt")
if err != nil {
    return fmt.Errorf("open file: %w", err)
}

// ❌ BAD: Lost error context
func process() error {
    if err := doSomething(); err != nil {
        return err
    }
    return nil
}

// ✅ GOOD: Wrapped error
func process() error {
    if err := doSomething(); err != nil {
        return fmt.Errorf("process failed: %w", err)
    }
    return nil
}

// ❌ BAD: Panic for normal errors
func getConfig() *Config {
    cfg, err := loadConfig()
    if err != nil {
        panic(err)  // Don't panic
    }
    return cfg
}

// ✅ GOOD: Return error
func getConfig() (*Config, error) {
    cfg, err := loadConfig()
    if err != nil {
        return nil, fmt.Errorf("load config: %w", err)
    }
    return cfg, nil
}
```

## Review Output Format

```
📝 Code Review Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📂 File: internal/service/user.go

⚠️  HIGH: SQL Injection Vulnerability (line 45)
   ├─ Issue: Unsanitized user input in SQL query
   ├─ Risk: Database compromise
   └─ Fix: Use parameterized queries

💡 MEDIUM: Non-Idiomatic Error Handling (line 67)
   ├─ Issue: Returning string error instead of error type
   ├─ Impact: Type safety, error wrapping
   └─ Suggestion: Return error type

⚡ LOW: Performance - Missing Pre-allocation (line 89)
   ├─ Issue: Slice growing without capacity hint
   ├─ Impact: Multiple allocations
   └─ Optimization: make([]Type, 0, expectedSize)

✅ GOOD: Proper context propagation (line 23)
✅ GOOD: Thread-safe cache implementation (line 112)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary:
  High: 1 | Medium: 1 | Low: 1 | Good: 2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Automated Checks

The review includes automated checks using:
- `go vet` - Official Go static analysis
- `staticcheck` - Advanced static analysis
- `gosec` - Security-focused linter
- `golangci-lint` - Comprehensive linter suite
- Custom pattern matching for Go-specific issues

## Manual Review Areas

For complex code, the command performs manual review of:
- Architecture and design patterns
- API design and interfaces
- Test coverage and quality
- Documentation completeness
- Code complexity and maintainability

## Actionable Suggestions

Each issue includes:
1. **Location**: Exact file and line number
2. **Severity**: HIGH, MEDIUM, LOW
3. **Description**: What the issue is
4. **Impact**: Why it matters
5. **Fix**: How to resolve it
6. **Example**: Code snippet showing the fix

## Integration with Tools

The command can integrate with:
- GitHub PR comments
- GitLab merge request notes
- Bitbucket PR feedback
- Slack notifications
- Email reports

## Configuration

Create `.go-review.yml` in project root:

```yaml
ignore:
  - vendor/
  - mocks/
  - ".*_test.go"

severity:
  min_level: MEDIUM

focus:
  - security
  - performance
  - concurrency

custom_rules:
  - pattern: "fmt.Print"
    message: "Use structured logging"
    severity: LOW
```

## When to Use

Use this command:
- Before creating pull requests
- During code reviews
- After major refactoring
- When onboarding new team members
- As part of CI/CD pipeline
- When learning Go best practices
- Before production deployment

## Best Practices

The review checks compliance with:
- Effective Go guidelines
- Go Code Review Comments
- Go proverbs
- Industry best practices
- Security standards (OWASP)
- Performance optimization patterns

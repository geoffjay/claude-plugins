---
name: go-patterns
description: Modern Go patterns, idioms, and best practices from Go 1.18+. Use when user needs guidance on idiomatic Go code, design patterns, or modern Go features like generics and workspaces.
---

# Go Patterns Skill

This skill provides comprehensive guidance on modern Go patterns, idioms, and best practices, with special focus on features introduced in Go 1.18 and later.

## When to Use

Activate this skill when:
- Writing idiomatic Go code
- Implementing design patterns in Go
- Using modern Go features (generics, fuzzing, workspaces)
- Refactoring code to be more idiomatic
- Teaching Go best practices
- Code review for idiom compliance

## Modern Go Features

### Generics (Go 1.18+)

**Type Parameters:**
```go
// Generic function
func Map[T, U any](slice []T, f func(T) U) []U {
    result := make([]U, len(slice))
    for i, v := range slice {
        result[i] = f(v)
    }
    return result
}

// Usage
numbers := []int{1, 2, 3, 4, 5}
doubled := Map(numbers, func(n int) int { return n * 2 })
```

**Type Constraints:**
```go
// Ordered constraint
type Ordered interface {
    ~int | ~int8 | ~int16 | ~int32 | ~int64 |
    ~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 |
    ~float32 | ~float64 | ~string
}

func Min[T Ordered](a, b T) T {
    if a < b {
        return a
    }
    return b
}

// Custom constraints
type Numeric interface {
    ~int | ~int64 | ~float64
}

func Sum[T Numeric](values []T) T {
    var sum T
    for _, v := range values {
        sum += v
    }
    return sum
}
```

**Generic Data Structures:**
```go
// Generic stack
type Stack[T any] struct {
    items []T
}

func NewStack[T any]() *Stack[T] {
    return &Stack[T]{items: make([]T, 0)}
}

func (s *Stack[T]) Push(item T) {
    s.items = append(s.items, item)
}

func (s *Stack[T]) Pop() (T, bool) {
    if len(s.items) == 0 {
        var zero T
        return zero, false
    }
    item := s.items[len(s.items)-1]
    s.items = s.items[:len(s.items)-1]
    return item, true
}

// Generic map utilities
func Keys[K comparable, V any](m map[K]V) []K {
    keys := make([]K, 0, len(m))
    for k := range m {
        keys = append(keys, k)
    }
    return keys
}

func Values[K comparable, V any](m map[K]V) []V {
    values := make([]V, 0, len(m))
    for _, v := range m {
        values = append(values, v)
    }
    return values
}
```

### Workspaces (Go 1.18+)

**go.work file:**
```
go 1.21

use (
    ./service
    ./shared
    ./tools
)

replace example.com/legacy => ./vendor/legacy
```

**Benefits:**
- Multi-module development
- Local dependency overrides
- Simplified testing across modules
- Better monorepo support

## Essential Go Patterns

### Functional Options Pattern

```go
type Server struct {
    host    string
    port    int
    timeout time.Duration
    logger  *log.Logger
}

type Option func(*Server)

func WithHost(host string) Option {
    return func(s *Server) {
        s.host = host
    }
}

func WithPort(port int) Option {
    return func(s *Server) {
        s.port = port
    }
}

func WithTimeout(timeout time.Duration) Option {
    return func(s *Server) {
        s.timeout = timeout
    }
}

func WithLogger(logger *log.Logger) Option {
    return func(s *Server) {
        s.logger = logger
    }
}

func NewServer(opts ...Option) *Server {
    s := &Server{
        host:    "localhost",
        port:    8080,
        timeout: 30 * time.Second,
        logger:  log.Default(),
    }

    for _, opt := range opts {
        opt(s)
    }

    return s
}

// Usage
server := NewServer(
    WithHost("0.0.0.0"),
    WithPort(3000),
    WithTimeout(60 * time.Second),
)
```

### Builder Pattern

```go
type Query struct {
    table      string
    where      []string
    orderBy    string
    limit      int
    offset     int
}

type QueryBuilder struct {
    query Query
}

func NewQueryBuilder(table string) *QueryBuilder {
    return &QueryBuilder{
        query: Query{table: table},
    }
}

func (b *QueryBuilder) Where(condition string) *QueryBuilder {
    b.query.where = append(b.query.where, condition)
    return b
}

func (b *QueryBuilder) OrderBy(field string) *QueryBuilder {
    b.query.orderBy = field
    return b
}

func (b *QueryBuilder) Limit(limit int) *QueryBuilder {
    b.query.limit = limit
    return b
}

func (b *QueryBuilder) Offset(offset int) *QueryBuilder {
    b.query.offset = offset
    return b
}

func (b *QueryBuilder) Build() Query {
    return b.query
}

// Usage
query := NewQueryBuilder("users").
    Where("age > 18").
    Where("active = true").
    OrderBy("created_at DESC").
    Limit(10).
    Offset(20).
    Build()
```

### Strategy Pattern

```go
// Strategy interface
type PaymentStrategy interface {
    Pay(amount float64) error
}

// Concrete strategies
type CreditCardPayment struct {
    cardNumber string
}

func (c *CreditCardPayment) Pay(amount float64) error {
    fmt.Printf("Paying $%.2f with credit card %s\n", amount, c.cardNumber)
    return nil
}

type PayPalPayment struct {
    email string
}

func (p *PayPalPayment) Pay(amount float64) error {
    fmt.Printf("Paying $%.2f with PayPal account %s\n", amount, p.email)
    return nil
}

type CryptoPayment struct {
    walletAddress string
}

func (c *CryptoPayment) Pay(amount float64) error {
    fmt.Printf("Paying $%.2f to wallet %s\n", amount, c.walletAddress)
    return nil
}

// Context
type PaymentProcessor struct {
    strategy PaymentStrategy
}

func NewPaymentProcessor(strategy PaymentStrategy) *PaymentProcessor {
    return &PaymentProcessor{strategy: strategy}
}

func (p *PaymentProcessor) ProcessPayment(amount float64) error {
    return p.strategy.Pay(amount)
}

// Usage
processor := NewPaymentProcessor(&CreditCardPayment{cardNumber: "1234-5678"})
processor.ProcessPayment(100.00)

processor = NewPaymentProcessor(&PayPalPayment{email: "user@example.com"})
processor.ProcessPayment(50.00)
```

### Observer Pattern

```go
type Observer interface {
    Update(event Event)
}

type Event struct {
    Type string
    Data interface{}
}

type Subject struct {
    observers []Observer
}

func (s *Subject) Attach(observer Observer) {
    s.observers = append(s.observers, observer)
}

func (s *Subject) Detach(observer Observer) {
    for i, obs := range s.observers {
        if obs == observer {
            s.observers = append(s.observers[:i], s.observers[i+1:]...)
            break
        }
    }
}

func (s *Subject) Notify(event Event) {
    for _, observer := range s.observers {
        observer.Update(event)
    }
}

// Concrete observer
type Logger struct {
    name string
}

func (l *Logger) Update(event Event) {
    fmt.Printf("[%s] Received event: %s\n", l.name, event.Type)
}

// Usage
subject := &Subject{}
logger1 := &Logger{name: "Logger1"}
logger2 := &Logger{name: "Logger2"}

subject.Attach(logger1)
subject.Attach(logger2)

subject.Notify(Event{Type: "UserCreated", Data: "user123"})
```

## Idiomatic Go Patterns

### Error Handling

**Sentinel Errors:**
```go
var (
    ErrNotFound     = errors.New("resource not found")
    ErrUnauthorized = errors.New("unauthorized access")
    ErrInvalidInput = errors.New("invalid input")
)

func GetUser(id string) (*User, error) {
    if id == "" {
        return nil, ErrInvalidInput
    }

    user := findUser(id)
    if user == nil {
        return nil, ErrNotFound
    }

    return user, nil
}

// Check with errors.Is
if errors.Is(err, ErrNotFound) {
    // Handle not found
}
```

**Custom Error Types:**
```go
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error on %s: %s", e.Field, e.Message)
}

// Check with errors.As
var valErr *ValidationError
if errors.As(err, &valErr) {
    fmt.Printf("Validation failed: %s\n", valErr.Field)
}
```

**Error Wrapping:**
```go
func ProcessUser(id string) error {
    user, err := GetUser(id)
    if err != nil {
        return fmt.Errorf("process user: %w", err)
    }

    if err := ValidateUser(user); err != nil {
        return fmt.Errorf("validate user %s: %w", id, err)
    }

    return nil
}
```

### Interface Patterns

**Small Interfaces:**
```go
// Good: Small, focused interfaces
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

type Closer interface {
    Close() error
}

// Compose interfaces
type ReadWriteCloser interface {
    Reader
    Writer
    Closer
}
```

**Interface Segregation:**
```go
// Instead of one large interface
type Repository interface {
    Create(ctx context.Context, user *User) error
    Read(ctx context.Context, id string) (*User, error)
    Update(ctx context.Context, user *User) error
    Delete(ctx context.Context, id string) error
    List(ctx context.Context) ([]*User, error)
    Search(ctx context.Context, query string) ([]*User, error)
}

// Better: Separate interfaces
type UserCreator interface {
    Create(ctx context.Context, user *User) error
}

type UserReader interface {
    Read(ctx context.Context, id string) (*User, error)
    List(ctx context.Context) ([]*User, error)
}

type UserUpdater interface {
    Update(ctx context.Context, user *User) error
}

type UserDeleter interface {
    Delete(ctx context.Context, id string) error
}

type UserSearcher interface {
    Search(ctx context.Context, query string) ([]*User, error)
}
```

### Context Patterns

**Proper Context Usage:**
```go
func FetchData(ctx context.Context, url string) ([]byte, error) {
    // Create request with context
    req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
    if err != nil {
        return nil, fmt.Errorf("create request: %w", err)
    }

    // Check for cancellation before expensive operation
    select {
    case <-ctx.Done():
        return nil, ctx.Err()
    default:
    }

    // Execute request
    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return nil, fmt.Errorf("execute request: %w", err)
    }
    defer resp.Body.Close()

    return io.ReadAll(resp.Body)
}

// Context with timeout
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

data, err := FetchData(ctx, "https://api.example.com/data")
```

**Context Values:**
```go
type contextKey string

const (
    requestIDKey contextKey = "requestID"
    userIDKey    contextKey = "userID"
)

func WithRequestID(ctx context.Context, requestID string) context.Context {
    return context.WithValue(ctx, requestIDKey, requestID)
}

func GetRequestID(ctx context.Context) (string, bool) {
    requestID, ok := ctx.Value(requestIDKey).(string)
    return requestID, ok
}

func WithUserID(ctx context.Context, userID string) context.Context {
    return context.WithValue(ctx, userIDKey, userID)
}

func GetUserID(ctx context.Context) (string, bool) {
    userID, ok := ctx.Value(userIDKey).(string)
    return userID, ok
}
```

## Best Practices

1. **Accept interfaces, return structs**
2. **Make the zero value useful**
3. **Use composition over inheritance**
4. **Handle errors explicitly**
5. **Use defer for cleanup**
6. **Prefer sync.RWMutex for read-heavy workloads**
7. **Use context for cancellation and timeouts**
8. **Keep interfaces small**
9. **Document exported identifiers**
10. **Use go fmt and go vet**

## Resources

Additional patterns and examples are available in the `assets/` directory:
- `examples/` - Complete code examples
- `patterns/` - Design pattern implementations
- `antipatterns/` - Common mistakes to avoid

See `references/` directory for:
- Links to official Go documentation
- Effective Go guidelines
- Go proverbs
- Community best practices

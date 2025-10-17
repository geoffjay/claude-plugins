---
name: go-concurrency
description: Advanced concurrency patterns with goroutines, channels, context, and synchronization primitives. Use when working with concurrent Go code, implementing parallel processing, or debugging race conditions.
---

# Go Concurrency Skill

This skill provides expert guidance on Go's concurrency primitives and patterns, covering goroutines, channels, synchronization, and best practices for building concurrent systems.

## When to Use

Activate this skill when:
- Implementing concurrent/parallel processing
- Working with goroutines and channels
- Using synchronization primitives (mutexes, wait groups, etc.)
- Debugging race conditions
- Optimizing concurrent performance
- Implementing worker pools or pipelines
- Handling context cancellation

## Goroutine Fundamentals

### Basic Goroutines

```go
// Simple goroutine
go func() {
    fmt.Println("Hello from goroutine")
}()

// Goroutine with parameters
go func(msg string) {
    fmt.Println(msg)
}("Hello")

// Goroutine with closure
message := "Hello"
go func() {
    fmt.Println(message) // Captures message
}()
```

### Common Pitfalls

```go
// ❌ BAD: Loop variable capture
for i := 0; i < 5; i++ {
    go func() {
        fmt.Println(i) // All goroutines may print 5
    }()
}

// ✅ GOOD: Pass as parameter
for i := 0; i < 5; i++ {
    go func(n int) {
        fmt.Println(n) // Each prints correct value
    }(i)
}

// ✅ GOOD: Create local copy
for i := 0; i < 5; i++ {
    i := i // Create new variable
    go func() {
        fmt.Println(i)
    }()
}
```

## Channel Patterns

### Channel Types

```go
// Unbuffered channel (synchronous)
ch := make(chan int)

// Buffered channel (asynchronous up to buffer size)
ch := make(chan int, 10)

// Send-only channel
func send(ch chan<- int) {
    ch <- 42
}

// Receive-only channel
func receive(ch <-chan int) {
    value := <-ch
}

// Bidirectional channel
ch := make(chan int)
```

### Channel Operations

```go
// Send
ch <- value

// Receive
value := <-ch

// Receive with ok check
value, ok := <-ch
if !ok {
    // Channel closed
}

// Close channel
close(ch)

// Range over channel
for value := range ch {
    fmt.Println(value)
}
```

### Select Statement

```go
// Wait for first available operation
select {
case msg1 := <-ch1:
    fmt.Println("Received from ch1:", msg1)
case msg2 := <-ch2:
    fmt.Println("Received from ch2:", msg2)
case ch3 <- value:
    fmt.Println("Sent to ch3")
default:
    fmt.Println("No channels ready")
}

// Timeout pattern
select {
case result := <-ch:
    return result, nil
case <-time.After(5 * time.Second):
    return nil, errors.New("timeout")
}

// Context cancellation
select {
case result := <-ch:
    return result, nil
case <-ctx.Done():
    return nil, ctx.Err()
}
```

## Synchronization Primitives

### Mutex

```go
type SafeCounter struct {
    mu    sync.Mutex
    count int
}

func (c *SafeCounter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count++
}

func (c *SafeCounter) Value() int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.count
}
```

### RWMutex

```go
type Cache struct {
    mu    sync.RWMutex
    items map[string]interface{}
}

func (c *Cache) Get(key string) (interface{}, bool) {
    c.mu.RLock() // Multiple readers allowed
    defer c.mu.RUnlock()
    value, ok := c.items[key]
    return value, ok
}

func (c *Cache) Set(key string, value interface{}) {
    c.mu.Lock() // Exclusive write access
    defer c.mu.Unlock()
    c.items[key] = value
}
```

### WaitGroup

```go
func processItems(items []Item) {
    var wg sync.WaitGroup

    for _, item := range items {
        wg.Add(1)
        go func(item Item) {
            defer wg.Done()
            process(item)
        }(item)
    }

    wg.Wait() // Wait for all goroutines
}
```

### Once

```go
type Database struct {
    instance *sql.DB
    once     sync.Once
}

func (d *Database) GetConnection() *sql.DB {
    d.once.Do(func() {
        d.instance, _ = sql.Open("postgres", "connection-string")
    })
    return d.instance
}
```

## Concurrency Patterns

### Worker Pool

```go
type WorkerPool struct {
    workerCount int
    jobs        chan Job
    results     chan Result
    wg          sync.WaitGroup
}

type Job struct {
    ID   int
    Data interface{}
}

type Result struct {
    JobID int
    Value interface{}
    Error error
}

func NewWorkerPool(workerCount int) *WorkerPool {
    return &WorkerPool{
        workerCount: workerCount,
        jobs:        make(chan Job, 100),
        results:     make(chan Result, 100),
    }
}

func (p *WorkerPool) Start(ctx context.Context) {
    for i := 0; i < p.workerCount; i++ {
        p.wg.Add(1)
        go p.worker(ctx)
    }
}

func (p *WorkerPool) worker(ctx context.Context) {
    defer p.wg.Done()

    for {
        select {
        case job, ok := <-p.jobs:
            if !ok {
                return
            }
            result := processJob(job)
            select {
            case p.results <- result:
            case <-ctx.Done():
                return
            }
        case <-ctx.Done():
            return
        }
    }
}

func (p *WorkerPool) Submit(job Job) {
    p.jobs <- job
}

func (p *WorkerPool) Results() <-chan Result {
    return p.results
}

func (p *WorkerPool) Close() {
    close(p.jobs)
    p.wg.Wait()
    close(p.results)
}

// Usage
ctx := context.Background()
pool := NewWorkerPool(10)
pool.Start(ctx)

for i := 0; i < 100; i++ {
    pool.Submit(Job{ID: i, Data: fmt.Sprintf("job-%d", i)})
}

go func() {
    for result := range pool.Results() {
        if result.Error != nil {
            log.Printf("Job %d failed: %v", result.JobID, result.Error)
        } else {
            log.Printf("Job %d completed: %v", result.JobID, result.Value)
        }
    }
}()

pool.Close()
```

### Pipeline Pattern

```go
// Generator stage
func generator(ctx context.Context, nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for _, n := range nums {
            select {
            case out <- n:
            case <-ctx.Done():
                return
            }
        }
    }()
    return out
}

// Processing stage
func square(ctx context.Context, in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range in {
            select {
            case out <- n * n:
            case <-ctx.Done():
                return
            }
        }
    }()
    return out
}

// Another processing stage
func double(ctx context.Context, in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range in {
            select {
            case out <- n * 2:
            case <-ctx.Done():
                return
            }
        }
    }()
    return out
}

// Usage - compose pipeline
ctx := context.Background()
numbers := generator(ctx, 1, 2, 3, 4, 5)
squared := square(ctx, numbers)
doubled := double(ctx, squared)

for result := range doubled {
    fmt.Println(result)
}
```

### Fan-Out/Fan-In

```go
// Fan-out: distribute work to multiple goroutines
func fanOut(ctx context.Context, input <-chan int, workers int) []<-chan int {
    channels := make([]<-chan int, workers)

    for i := 0; i < workers; i++ {
        channels[i] = worker(ctx, input)
    }

    return channels
}

func worker(ctx context.Context, input <-chan int) <-chan int {
    output := make(chan int)
    go func() {
        defer close(output)
        for n := range input {
            select {
            case output <- expensiveOperation(n):
            case <-ctx.Done():
                return
            }
        }
    }()
    return output
}

// Fan-in: merge multiple channels into one
func fanIn(ctx context.Context, channels ...<-chan int) <-chan int {
    var wg sync.WaitGroup
    output := make(chan int)

    multiplex := func(ch <-chan int) {
        defer wg.Done()
        for n := range ch {
            select {
            case output <- n:
            case <-ctx.Done():
                return
            }
        }
    }

    wg.Add(len(channels))
    for _, ch := range channels {
        go multiplex(ch)
    }

    go func() {
        wg.Wait()
        close(output)
    }()

    return output
}

// Usage
ctx := context.Background()
input := generator(ctx, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

// Fan-out to 3 workers
workers := fanOut(ctx, input, 3)

// Fan-in results
results := fanIn(ctx, workers...)

for result := range results {
    fmt.Println(result)
}
```

### Semaphore Pattern

```go
type Semaphore struct {
    sem chan struct{}
}

func NewSemaphore(maxConcurrency int) *Semaphore {
    return &Semaphore{
        sem: make(chan struct{}, maxConcurrency),
    }
}

func (s *Semaphore) Acquire() {
    s.sem <- struct{}{}
}

func (s *Semaphore) Release() {
    <-s.sem
}

// Usage
sem := NewSemaphore(5) // Max 5 concurrent operations

for _, item := range items {
    sem.Acquire()
    go func(item Item) {
        defer sem.Release()
        process(item)
    }(item)
}
```

### Rate Limiting

```go
// Token bucket rate limiter
type RateLimiter struct {
    ticker   *time.Ticker
    tokens   chan struct{}
}

func NewRateLimiter(rate time.Duration, burst int) *RateLimiter {
    rl := &RateLimiter{
        ticker: time.NewTicker(rate),
        tokens: make(chan struct{}, burst),
    }

    // Fill bucket initially
    for i := 0; i < burst; i++ {
        rl.tokens <- struct{}{}
    }

    // Refill tokens
    go func() {
        for range rl.ticker.C {
            select {
            case rl.tokens <- struct{}{}:
            default:
            }
        }
    }()

    return rl
}

func (rl *RateLimiter) Wait(ctx context.Context) error {
    select {
    case <-rl.tokens:
        return nil
    case <-ctx.Done():
        return ctx.Err()
    }
}

func (rl *RateLimiter) Stop() {
    rl.ticker.Stop()
}

// Usage
limiter := NewRateLimiter(time.Second/10, 5) // 10 requests per second, burst of 5
defer limiter.Stop()

for _, request := range requests {
    if err := limiter.Wait(ctx); err != nil {
        log.Printf("Rate limit error: %v", err)
        continue
    }
    processRequest(request)
}
```

## Error Handling in Concurrent Code

### errgroup Package

```go
import "golang.org/x/sync/errgroup"

func fetchURLs(ctx context.Context, urls []string) error {
    g, ctx := errgroup.WithContext(ctx)

    for _, url := range urls {
        url := url // Capture for goroutine
        g.Go(func() error {
            return fetchURL(ctx, url)
        })
    }

    // Wait for all goroutines, return first error
    return g.Wait()
}

// With limited concurrency
func fetchURLsLimited(ctx context.Context, urls []string) error {
    g, ctx := errgroup.WithContext(ctx)
    g.SetLimit(10) // Max 10 concurrent

    for _, url := range urls {
        url := url
        g.Go(func() error {
            return fetchURL(ctx, url)
        })
    }

    return g.Wait()
}
```

## Best Practices

1. **Always close channels from sender side**
2. **Use context for cancellation and timeouts**
3. **Avoid goroutine leaks - ensure they can exit**
4. **Use buffered channels to avoid blocking**
5. **Prefer sync.RWMutex for read-heavy workloads**
6. **Don't use defer in hot loops**
7. **Test with race detector: `go test -race`**
8. **Use errgroup for error propagation**
9. **Limit concurrent operations with worker pools**
10. **Profile before optimizing**

## Race Condition Detection

```bash
# Run tests with race detector
go test -race ./...

# Run program with race detector
go run -race main.go

# Build with race detector
go build -race
```

## Common Patterns to Avoid

```go
// ❌ BAD: Unbounded goroutine creation
for _, item := range millionItems {
    go process(item) // May create millions of goroutines
}

// ✅ GOOD: Use worker pool
pool := NewWorkerPool(100)
for _, item := range millionItems {
    pool.Submit(item)
}

// ❌ BAD: Goroutine leak
func leak() <-chan int {
    ch := make(chan int)
    go func() {
        ch <- expensiveComputation() // If receiver never reads, goroutine leaks
    }()
    return ch
}

// ✅ GOOD: Use context for cancellation
func noLeak(ctx context.Context) <-chan int {
    ch := make(chan int)
    go func() {
        defer close(ch)
        result := expensiveComputation()
        select {
        case ch <- result:
        case <-ctx.Done():
        }
    }()
    return ch
}
```

## Resources

Additional examples and patterns are available in:
- `assets/examples/` - Complete concurrency examples
- `assets/patterns/` - Common concurrency patterns
- `references/` - Links to Go concurrency resources and papers

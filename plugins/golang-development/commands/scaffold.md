---
name: golang-development:scaffold
description: Scaffold new Go projects with modern structure, Go modules, testing setup, CI/CD pipelines, and best practices
---

# Golang Development Scaffold Command

Create a new Go project with a production-ready structure, modern tooling, and best practices built-in.

## Usage

```bash
/golang-development:scaffold <project-name> [options]
```

## Arguments

- `$1` - Project name (required, will be used for module name)
- `$2` - Project type: `service`, `cli`, `library`, or `microservice` (optional, defaults to `service`)
- `$3` - Additional options as JSON (optional)

## Examples

```bash
# Create a basic HTTP service
/golang-development:scaffold my-api service

# Create a CLI application
/golang-development:scaffold my-tool cli

# Create a library
/golang-development:scaffold my-lib library

# Create a microservice with full features
/golang-development:scaffold user-service microservice '{"with_grpc": true, "with_db": true}'
```

## Project Structures

### Service (HTTP API)
```
my-api/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── handler/
│   │   └── health.go
│   ├── middleware/
│   │   └── logging.go
│   └── service/
│       └── user.go
├── pkg/
│   └── response/
│       └── response.go
├── api/
│   └── openapi.yaml
├── scripts/
│   └── build.sh
├── deployments/
│   ├── Dockerfile
│   └── k8s/
├── go.mod
├── go.sum
├── .gitignore
├── .golangci.yml
├── Makefile
└── README.md
```

### CLI Application
```
my-tool/
├── cmd/
│   └── my-tool/
│       └── main.go
├── internal/
│   ├── command/
│   │   ├── root.go
│   │   └── serve.go
│   └── config/
│       └── config.go
├── go.mod
├── go.sum
├── .gitignore
├── .golangci.yml
├── Makefile
└── README.md
```

### Library
```
my-lib/
├── example_test.go
├── lib.go
├── lib_test.go
├── go.mod
├── go.sum
├── .gitignore
├── .golangci.yml
├── LICENSE
└── README.md
```

### Microservice (Full Features)
```
user-service/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── domain/
│   │   └── user.go
│   ├── handler/
│   │   ├── http/
│   │   └── grpc/
│   ├── repository/
│   │   └── postgres/
│   ├── service/
│   │   └── user_service.go
│   └── infrastructure/
│       ├── database/
│       ├── cache/
│       └── messaging/
├── api/
│   ├── http/
│   │   └── openapi.yaml
│   └── grpc/
│       └── user.proto
├── pkg/
│   ├── logger/
│   ├── metrics/
│   └── tracing/
├── migrations/
│   └── 001_create_users.sql
├── deployments/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── k8s/
├── scripts/
├── go.mod
├── go.sum
├── .gitignore
├── .golangci.yml
├── Makefile
└── README.md
```

## Generated Files

### main.go (Service)
```go
package main

import (
    "context"
    "fmt"
    "log"
    "net/http"
    "os"
    "os/signal"
    "syscall"
    "time"

    "{{.ModuleName}}/internal/handler"
    "{{.ModuleName}}/internal/middleware"
)

func main() {
    // Setup router
    mux := http.NewServeMux()

    // Middleware
    handler := middleware.Logging(
        middleware.Recovery(mux),
    )

    // Routes
    mux.HandleFunc("/health", handler.Health)
    mux.HandleFunc("/ready", handler.Ready)

    // Server configuration
    port := os.Getenv("PORT")
    if port == "" {
        port = "8080"
    }

    server := &http.Server{
        Addr:         fmt.Sprintf(":%s", port),
        Handler:      handler,
        ReadTimeout:  15 * time.Second,
        WriteTimeout: 15 * time.Second,
        IdleTimeout:  60 * time.Second,
    }

    // Start server
    go func() {
        log.Printf("Server starting on port %s", port)
        if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatalf("Server error: %v", err)
        }
    }()

    // Graceful shutdown
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    log.Println("Shutting down server...")
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    if err := server.Shutdown(ctx); err != nil {
        log.Fatalf("Server forced to shutdown: %v", err)
    }

    log.Println("Server exited")
}
```

### Makefile
```makefile
.PHONY: build test lint run clean

# Variables
APP_NAME := {{.ProjectName}}
VERSION := $(shell git describe --tags --always --dirty)
BUILD_TIME := $(shell date -u '+%Y-%m-%d_%H:%M:%S')
LDFLAGS := -ldflags "-X main.Version=$(VERSION) -X main.BuildTime=$(BUILD_TIME)"

# Build
build:
	go build $(LDFLAGS) -o bin/$(APP_NAME) ./cmd/server

# Test
test:
	go test -v -race -coverprofile=coverage.out ./...

# Coverage
coverage:
	go tool cover -html=coverage.out

# Lint
lint:
	golangci-lint run

# Run
run:
	go run ./cmd/server

# Clean
clean:
	rm -rf bin/
	rm -f coverage.out

# Install tools
tools:
	go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Docker
docker-build:
	docker build -t $(APP_NAME):$(VERSION) .

docker-run:
	docker run -p 8080:8080 $(APP_NAME):$(VERSION)
```

### Dockerfile
```dockerfile
# Build stage
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Copy go mod files
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main ./cmd/server

# Runtime stage
FROM alpine:latest

RUN apk --no-cache add ca-certificates

WORKDIR /root/

# Copy binary from builder
COPY --from=builder /app/main .

EXPOSE 8080

CMD ["./main"]
```

### .golangci.yml
```yaml
linters:
  enable:
    - errcheck
    - gosimple
    - govet
    - ineffassign
    - staticcheck
    - unused
    - gofmt
    - goimports
    - misspell
    - gocritic
    - gosec
    - revive

linters-settings:
  errcheck:
    check-blank: true
  govet:
    check-shadowing: true
  gofmt:
    simplify: true

issues:
  exclude-use-default: false
  max-issues-per-linter: 0
  max-same-issues: 0
```

### GitHub Actions CI (.github/workflows/ci.yml)
```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Set up Go
      uses: actions/setup-go@v4
      with:
        go-version: '1.21'

    - name: Install dependencies
      run: go mod download

    - name: Run tests
      run: go test -v -race -coverprofile=coverage.out ./...

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.out

  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Set up Go
      uses: actions/setup-go@v4
      with:
        go-version: '1.21'

    - name: golangci-lint
      uses: golangci/golangci-lint-action@v3
      with:
        version: latest

  build:
    runs-on: ubuntu-latest
    needs: [test, lint]
    steps:
    - uses: actions/checkout@v3

    - name: Set up Go
      uses: actions/setup-go@v4
      with:
        go-version: '1.21'

    - name: Build
      run: go build -v ./cmd/server
```

## Configuration Options

The command accepts a JSON configuration object:

```json
{
  "with_grpc": true,
  "with_db": true,
  "with_redis": true,
  "with_kafka": true,
  "with_docker": true,
  "with_k8s": true,
  "with_ci": true,
  "db_driver": "postgres",
  "module_path": "github.com/user/project"
}
```

## Implementation Steps

1. Parse arguments and configuration
2. Create project directory structure
3. Initialize Go module
4. Generate main.go and core files
5. Create Makefile and build scripts
6. Add Dockerfile and Docker Compose
7. Generate CI/CD configuration
8. Create README with usage instructions
9. Initialize git repository
10. Run `go mod tidy`

## Features Included

- **Modern Project Structure**: Clean architecture with separation of concerns
- **HTTP Server**: Production-ready with graceful shutdown
- **Middleware**: Logging, recovery, CORS, authentication templates
- **Health Checks**: Health and readiness endpoints
- **Testing**: Test structure and examples
- **Linting**: golangci-lint configuration
- **CI/CD**: GitHub Actions workflow
- **Docker**: Multi-stage Dockerfile
- **Kubernetes**: Basic manifests (if requested)
- **Documentation**: Comprehensive README

## Post-Scaffold Steps

After scaffolding, the command will suggest:

```bash
cd {{.ProjectName}}
go mod tidy
make test
make run
```

## When to Use

Use this command to:
- Start new Go projects quickly
- Ensure consistent project structure
- Set up best practices from the start
- Include modern tooling and CI/CD
- Scaffold microservices or APIs
- Create CLI tools with proper structure

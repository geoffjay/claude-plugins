---
description: Review Sinatra code for security issues, performance problems, route conflicts, and framework best practices
---

# Sinatra Review Command

Performs comprehensive code review of Sinatra applications, identifying security vulnerabilities, performance issues, routing conflicts, and deviations from best practices.

## Arguments

- **$1: path** (optional) - Path to review (defaults to current directory)

## Usage Examples

```bash
# Review current directory
/sinatra-review

# Review specific directory
/sinatra-review /path/to/sinatra-app

# Review specific file
/sinatra-review app/controllers/users_controller.rb
```

## Workflow

### Step 1: Scan and Identify Application Files

**Discovery Phase:**
1. Locate `config.ru` to identify Rack application
2. Find Sinatra application files (controllers, routes)
3. Identify application structure (classic vs modular)
4. Scan for middleware configuration
5. Locate view templates and helpers
6. Find configuration files
7. Identify database and model files

**File Patterns to Search:**
```bash
# Application files
*.rb files inheriting from Sinatra::Base
config.ru
app.rb (classic style)
app/controllers/*.rb
lib/**/*.rb

# View templates
views/**/*.erb
views/**/*.haml
views/**/*.slim

# Configuration
config/*.rb
Gemfile
.env files
```

### Step 2: Analyze Route Definitions

**Route Conflict Detection:**

Check for:
1. **Duplicate routes** with same path and HTTP method
2. **Overlapping routes** where order matters (specific before generic)
3. **Missing route constraints** leading to ambiguous matching
4. **Wildcard route conflicts**

**Examples of Issues:**

```ruby
# ISSUE: Route order conflict
get '/users/new' do
  # Never reached because of wildcard below
end

get '/users/:id' do
  # This catches /users/new
end

# FIX: Specific routes before wildcards
get '/users/new' do
  # Now reached first
end

get '/users/:id' do
  # Only catches other IDs
end

# ISSUE: Duplicate routes
get '/api/users' do
  # First definition
end

get '/api/users' do
  # Overwrites first - only this runs
end

# ISSUE: Missing validation
get '/users/:id' do
  user = User.find(params[:id])  # What if id is not numeric?
end

# FIX: Add validation
get '/users/:id', id: /\d+/ do
  user = User.find(params[:id])
end
```

**Route Analysis Report:**
```
Route Analysis:
  Total routes: 25
  GET: 15, POST: 5, PUT: 3, DELETE: 2

  ⚠ Warnings:
    - Route order issue in app/controllers/users_controller.rb:15
      GET /users/:id should be after GET /users/new

    - Missing parameter validation in app/controllers/posts_controller.rb:32
      Route GET /posts/:id should validate :id is numeric
```

### Step 3: Security Analysis

**Security Checklist:**

**1. CSRF Protection:**
```ruby
# CHECK: Is CSRF protection enabled?
use Rack::Protection
# or
use Rack::Protection::AuthenticityToken

# ISSUE: Missing CSRF for POST/PUT/DELETE
post '/users' do
  User.create(params[:user])  # Vulnerable to CSRF
end

# FIX: Ensure Rack::Protection is enabled
```

**2. XSS Prevention:**
```ruby
# CHECK: Are templates auto-escaping HTML?
# ERB: Use <%= %> (escapes) not <%== %> (raw)

# ISSUE: Raw user input in template
<div><%== @user.bio %></div>

# FIX: Escape user input
<div><%= @user.bio %></div>

# CHECK: JSON responses properly encoded
# ISSUE: Manual JSON creation
get '/api/users' do
  "{ \"name\": \"#{user.name}\" }"  # XSS if name contains quotes
end

# FIX: Use JSON library
get '/api/users' do
  json({ name: user.name })
end
```

**3. SQL Injection:**
```ruby
# ISSUE: String interpolation in queries
DB["SELECT * FROM users WHERE email = '#{params[:email]}'"]

# FIX: Use parameterized queries
DB["SELECT * FROM users WHERE email = ?", params[:email]]

# ISSUE: Unsafe ActiveRecord
User.where("email = '#{params[:email]}'")

# FIX: Use hash conditions
User.where(email: params[:email])
```

**4. Authentication & Authorization:**
```ruby
# CHECK: Protected routes have authentication
# ISSUE: Admin route without auth check
delete '/users/:id' do
  User.find(params[:id]).destroy  # No auth check!
end

# FIX: Add authentication
before '/admin/*' do
  halt 401 unless current_user&.admin?
end

# CHECK: Session security
# ISSUE: Weak session configuration
use Rack::Session::Cookie, secret: 'easy'

# FIX: Strong secret and secure flags
use Rack::Session::Cookie,
  secret: ENV['SESSION_SECRET'],  # Long random string
  same_site: :strict,
  httponly: true,
  secure: production?
```

**5. Mass Assignment:**
```ruby
# ISSUE: Accepting all params
User.create(params)

# FIX: Whitelist allowed attributes
def user_params
  params.slice(:name, :email, :bio)
end

User.create(user_params)
```

**6. File Upload Security:**
```ruby
# ISSUE: Unrestricted file uploads
post '/upload' do
  File.write("uploads/#{params[:file][:filename]}", params[:file][:tempfile].read)
end

# FIX: Validate file type and sanitize filename
post '/upload' do
  file = params[:file]

  # Validate content type
  halt 400 unless ['image/jpeg', 'image/png'].include?(file[:type])

  # Sanitize filename
  filename = File.basename(file[:filename]).gsub(/[^a-zA-Z0-9\._-]/, '')

  # Save with random name
  secure_name = "#{SecureRandom.hex}-#{filename}"
  File.write("uploads/#{secure_name}", file[:tempfile].read)
end
```

**7. Information Disclosure:**
```ruby
# ISSUE: Detailed error messages in production
configure :production do
  set :show_exceptions, true  # Exposes stack traces
end

# FIX: Hide errors in production
configure :production do
  set :show_exceptions, false
  set :dump_errors, false
end

error do
  log_error(env['sinatra.error'])
  json({ error: 'Internal server error' }, 500)
end
```

**Security Report:**
```
Security Analysis:
  ✓ CSRF protection enabled (Rack::Protection)
  ✓ Session configured securely
  ⚠ Potential Issues:
    - SQL injection risk in app/models/user.rb:45
    - Raw HTML output in views/profile.erb:12
    - Missing authentication check in app/controllers/admin_controller.rb:23
    - Weak session secret detected

  Critical: 1
  High: 2
  Medium: 3
  Low: 2
```

### Step 4: Review Middleware Configuration

**Middleware Analysis:**

Check for:
1. **Missing essential middleware** (Protection, CommonLogger)
2. **Incorrect ordering** (e.g., session after auth)
3. **Performance issues** (e.g., no compression)
4. **Security middleware** properly configured

**Common Issues:**

```ruby
# ISSUE: Missing compression
# FIX: Add Rack::Deflater
use Rack::Deflater

# ISSUE: Session middleware after authentication
use TokenAuth
use Rack::Session::Cookie  # Session needed by auth!

# FIX: Session before authentication
use Rack::Session::Cookie
use TokenAuth

# ISSUE: No security headers
# FIX: Add Rack::Protection
use Rack::Protection, except: [:session_hijacking]

# ISSUE: Static file serving after application
run MyApp
use Rack::Static  # Never reached!

# FIX: Static before application
use Rack::Static, urls: ['/css', '/js'], root: 'public'
run MyApp
```

**Middleware Report:**
```
Middleware Configuration:
  ✓ Rack::CommonLogger (logging)
  ✓ Rack::Session::Cookie (sessions)
  ✓ Rack::Protection (security)
  ⚠ Warnings:
    - Missing Rack::Deflater (compression)
    - Middleware order issue: Session should be before CustomAuth
    - Consider adding Rack::Attack for rate limiting
```

### Step 5: Performance Assessment

**Performance Patterns to Check:**

**1. Database Query Optimization:**
```ruby
# ISSUE: N+1 queries
get '/users' do
  users = User.all
  users.map { |u| { name: u.name, posts: u.posts.count } }
  # Queries DB for each user's posts
end

# FIX: Eager load or use counter cache
get '/users' do
  users = User.eager(:posts).all
  users.map { |u| { name: u.name, posts: u.posts.count } }
end

# ISSUE: Loading entire collection
get '/users' do
  json User.all.map(&:to_hash)  # Load all users in memory
end

# FIX: Paginate
get '/users' do
  page = params[:page]&.to_i || 1
  per_page = 50

  users = User.limit(per_page).offset((page - 1) * per_page)
  json users.map(&:to_hash)
end
```

**2. Caching Opportunities:**
```ruby
# ISSUE: Expensive operation on every request
get '/stats' do
  json calculate_expensive_stats  # Takes 2 seconds
end

# FIX: Add caching
get '/stats' do
  stats = cache.fetch('stats', expires_in: 300) do
    calculate_expensive_stats
  end
  json stats
end

# ISSUE: No HTTP caching headers
get '/public/data' do
  json PublicData.all
end

# FIX: Add cache control
get '/public/data' do
  cache_control :public, max_age: 3600
  json PublicData.all
end
```

**3. Response Optimization:**
```ruby
# ISSUE: Rendering large response synchronously
get '/large-export' do
  csv = generate_large_csv  # Blocks for 30 seconds
  send_file csv
end

# FIX: Stream or queue as background job
get '/large-export' do
  stream do |out|
    CSV.generate(out) do |csv|
      User.find_each do |user|
        csv << user.to_csv_row
      end
    end
  end
end
```

**Performance Report:**
```
Performance Analysis:
  ⚠ Issues Detected:
    - Potential N+1 query in app/controllers/users_controller.rb:42
    - Missing pagination in GET /api/posts (returns all records)
    - No caching headers on GET /api/public/data
    - Expensive operation in GET /stats without caching

  Recommendations:
    - Add database query optimization (eager loading)
    - Implement pagination for collection endpoints
    - Add HTTP caching headers for static content
    - Consider Redis caching for expensive operations
```

### Step 6: Error Handling Review

**Error Handling Patterns:**

```ruby
# ISSUE: No error handlers defined
get '/users/:id' do
  User.find(params[:id])  # Raises if not found, shows stack trace
end

# FIX: Add error handlers
error ActiveRecord::RecordNotFound do
  json({ error: 'Not found' }, 404)
end

error 404 do
  json({ error: 'Endpoint not found' }, 404)
end

error 500 do
  json({ error: 'Internal server error' }, 500)
end

# ISSUE: Not handling exceptions in routes
post '/users' do
  User.create!(params)  # Raises on validation error
end

# FIX: Handle exceptions
post '/users' do
  user = User.create(params)
  if user.persisted?
    json(user.to_hash, 201)
  else
    json({ errors: user.errors }, 422)
  end
end
```

### Step 7: Testing Coverage

**Test Analysis:**

Check for:
1. Test files exist
2. Route coverage
3. Error case testing
4. Integration vs unit tests
5. Test quality and patterns

**Report:**
```
Testing Analysis:
  Framework: RSpec
  Total specs: 45
  Coverage: 78%

  ⚠ Missing Tests:
    - No tests for POST /api/users
    - Error cases not tested in app/controllers/posts_controller.rb
    - Missing integration tests for authentication flow

  Recommendations:
    - Add tests for all POST/PUT/DELETE routes
    - Test error scenarios (404, 422, 500)
    - Increase coverage to 90%+
```

### Step 8: Generate Comprehensive Report

**Final Report Structure:**

```
================================================================================
SINATRA CODE REVIEW REPORT
================================================================================

Project: my-sinatra-app
Path: /path/to/app
Date: 2024-01-15
Reviewer: Sinatra Review Tool

--------------------------------------------------------------------------------
SUMMARY
--------------------------------------------------------------------------------
  Total Issues: 15
    Critical: 2
    High: 4
    Medium: 6
    Low: 3

  Categories:
    Security: 5 issues
    Performance: 4 issues
    Best Practices: 6 issues

--------------------------------------------------------------------------------
CRITICAL ISSUES
--------------------------------------------------------------------------------

1. SQL Injection Vulnerability
   Location: app/models/user.rb:45
   Severity: Critical

   Issue:
     DB["SELECT * FROM users WHERE email = '#{email}'"]

   Fix:
     DB["SELECT * FROM users WHERE email = ?", email]

   Impact: Attacker can execute arbitrary SQL queries

2. Missing Authentication on Admin Route
   Location: app/controllers/admin_controller.rb:23
   Severity: Critical

   Issue:
     delete '/users/:id' do
       User.find(params[:id]).destroy
     end

   Fix:
     before '/admin/*' do
       authenticate_admin!
     end

   Impact: Unauthorized users can delete records

--------------------------------------------------------------------------------
HIGH PRIORITY ISSUES
--------------------------------------------------------------------------------

[List high priority issues...]

--------------------------------------------------------------------------------
RECOMMENDATIONS
--------------------------------------------------------------------------------

Security:
  - Enable Rack::Protection::AuthenticityToken for CSRF
  - Rotate session secret to strong random value
  - Implement rate limiting with Rack::Attack
  - Add Content-Security-Policy headers

Performance:
  - Add Rack::Deflater for response compression
  - Implement caching strategy (Redis or Memcached)
  - Add pagination to collection endpoints
  - Optimize database queries (N+1 issues)

Testing:
  - Increase test coverage to 90%+
  - Add integration tests for critical flows
  - Test error scenarios
  - Add security-focused tests

Best Practices:
  - Extract business logic to service objects
  - Use helpers for repeated code
  - Implement proper error handling
  - Add API documentation

--------------------------------------------------------------------------------
DETAILED FINDINGS
--------------------------------------------------------------------------------

[Full list of all issues with locations, descriptions, and fixes]

================================================================================
END REPORT
================================================================================
```

## Review Categories

### Security
- CSRF protection
- XSS prevention
- SQL injection
- Authentication/Authorization
- Session security
- Mass assignment
- File upload security
- Information disclosure
- Secure headers

### Performance
- Database query optimization
- N+1 queries
- Caching opportunities
- Response optimization
- Static asset handling
- Connection pooling

### Best Practices
- Route organization
- Error handling
- Code organization
- Helper usage
- Configuration management
- Logging
- Documentation

### Testing
- Test coverage
- Test quality
- Missing tests
- Test organization

## Output Format

- Console output with colored severity indicators
- Detailed report with file locations and line numbers
- Suggested fixes with code examples
- Priority-sorted issue list
- Summary statistics

## Error Handling

- Handle non-Sinatra Ruby applications gracefully
- Report when application structure cannot be determined
- Skip non-readable files
- Handle parse errors in Ruby files

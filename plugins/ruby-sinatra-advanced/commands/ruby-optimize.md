---
description: Analyze and optimize Ruby code for performance, memory usage, and idiomatic patterns
---

# Ruby Optimize Command

Analyzes Ruby code and provides optimization recommendations for performance, memory usage, code readability, and idiomatic Ruby patterns.

## Arguments

- **$1: path** (required) - File or directory path to optimize
- **$2: focus** (optional) - Optimization focus: `performance`, `memory`, `readability`, or `all` (default: `all`)

## Usage Examples

```bash
# Analyze and optimize all aspects
/ruby-optimize app/models/user.rb

# Focus on performance only
/ruby-optimize app/services/ performance

# Focus on memory optimization
/ruby-optimize lib/data_processor.rb memory

# Focus on readability and idioms
/ruby-optimize app/ readability

# Optimize entire project
/ruby-optimize . all
```

## Workflow

### Step 1: Profile and Analyze Code

**Discovery Phase:**

1. Parse Ruby files in specified path
2. Identify methods and code patterns
3. Detect performance anti-patterns
4. Analyze memory allocation patterns
5. Check for idiomatic Ruby usage
6. Measure complexity metrics

**Analysis Tools:**
```ruby
# Use Ruby parser
require 'parser/current'

# AST analysis for pattern detection
ast = Parser::CurrentRuby.parse(source_code)

# Complexity analysis
require 'flog'
flog = Flog.new
flog.flog(file_path)
```

### Step 2: Performance Analysis

**Detect Performance Anti-Patterns:**

**1. Inefficient Enumeration:**
```ruby
# ISSUE: Using each when map is appropriate
def process_users
  result = []
  users.each do |user|
    result << user.name.upcase
  end
  result
end

# OPTIMIZED: Use map
def process_users
  users.map { |user| user.name.upcase }
end

# Benchmark improvement: 15-20% faster, less memory
```

**2. Repeated Object Creation:**
```ruby
# ISSUE: Creating regex in loop
def filter_emails(emails)
  emails.select { |email| email.match(/@gmail\.com/) }
end

# OPTIMIZED: Create regex once
EMAIL_PATTERN = /@gmail\.com/

def filter_emails(emails)
  emails.select { |email| email.match(EMAIL_PATTERN) }
end

# Benchmark improvement: 30-40% faster for large datasets
```

**3. N+1 Query Detection:**
```ruby
# ISSUE: N+1 queries
def user_with_posts
  users = User.all
  users.map do |user|
    {
      name: user.name,
      posts_count: user.posts.count  # Separate query for each user
    }
  end
end

# OPTIMIZED: Eager load or use counter cache
def user_with_posts
  users = User.eager(:posts).all
  users.map do |user|
    {
      name: user.name,
      posts_count: user.posts.count
    }
  end
end

# Or with counter cache
def user_with_posts
  users = User.all
  users.map do |user|
    {
      name: user.name,
      posts_count: user.posts_count  # From counter cache
    }
  end
end

# Benchmark improvement: 10-100x faster depending on data size
```

**4. Inefficient String Building:**
```ruby
# ISSUE: String concatenation in loop
def build_csv(records)
  csv = ""
  records.each do |record|
    csv += "#{record.id},#{record.name}\n"
  end
  csv
end

# OPTIMIZED: Use array join or StringIO
def build_csv(records)
  records.map { |r| "#{r.id},#{r.name}" }.join("\n")
end

# Or for very large datasets
require 'stringio'

def build_csv(records)
  StringIO.new.tap do |io|
    records.each do |record|
      io.puts "#{record.id},#{record.name}"
    end
  end.string
end

# Benchmark improvement: 5-10x faster for large datasets
```

**5. Unnecessary Sorting:**
```ruby
# ISSUE: Sorting entire collection when only need max/min
def highest_score(users)
  users.sort_by(&:score).last
end

# OPTIMIZED: Use max_by
def highest_score(users)
  users.max_by(&:score)
end

# Benchmark improvement: O(n) vs O(n log n)
```

**6. Block Performance:**
```ruby
# ISSUE: Symbol#to_proc with arguments
users.map { |u| u.name.upcase }

# OPTIMIZED: Use method chaining where possible
users.map(&:name).map(&:upcase)

# ISSUE: Creating proc in loop
items.select { |item| item.active? }

# OPTIMIZED: Use symbol to_proc
items.select(&:active?)

# Benchmark improvement: 10-15% faster
```

**7. Hash Access Patterns:**
```ruby
# ISSUE: Checking key and accessing value separately
if hash.key?(:name)
  value = hash[:name]
  process(value)
end

# OPTIMIZED: Use fetch or safe navigation
if value = hash[:name]
  process(value)
end

# Or with default
value = hash.fetch(:name, default_value)
process(value)

# ISSUE: Using Hash#merge in loop
result = {}
items.each do |item|
  result = result.merge(item.to_hash)
end

# OPTIMIZED: Use Hash#merge! or each_with_object
result = items.each_with_object({}) do |item, hash|
  hash.merge!(item.to_hash)
end

# Benchmark improvement: 2-3x faster
```

### Step 3: Memory Optimization

**Detect Memory Issues:**

**1. String Allocation:**
```ruby
# ISSUE: Creating new strings in loop
1000.times do
  hash['key'] = value  # Creates new 'key' string each time
end

# OPTIMIZED: Use symbols or frozen strings
1000.times do
  hash[:key] = value  # Reuses same symbol
end

# Or with frozen string literal
# frozen_string_literal: true

# Memory saved: ~40 bytes per string
```

**2. Array/Hash Allocation:**
```ruby
# ISSUE: Building large array without size hint
data = []
10_000.times do |i|
  data << i
end

# OPTIMIZED: Preallocate size
data = Array.new(10_000)
10_000.times do |i|
  data[i] = i
end

# Or use a different approach
data = (0...10_000).to_a

# Memory improvement: Fewer reallocations
```

**3. Object Copying:**
```ruby
# ISSUE: Unnecessary duplication
def process(data)
  temp = data.dup
  temp.map! { |item| item * 2 }
  temp
end

# OPTIMIZED: Use map without dup if original not needed
def process(data)
  data.map { |item| item * 2 }
end

# Memory saved: Full array copy avoided
```

**4. Lazy Evaluation:**
```ruby
# ISSUE: Loading everything into memory
File.readlines('large_file.txt').each do |line|
  process(line)
end

# OPTIMIZED: Process line by line
File.foreach('large_file.txt') do |line|
  process(line)
end

# Or use lazy enumeration
File.readlines('large_file.txt').lazy.each do |line|
  process(line)
end

# Memory saved: File size - line size
```

**5. Memoization Leaks:**
```ruby
# ISSUE: Unbounded memoization cache
def expensive_calculation(input)
  @cache ||= {}
  @cache[input] ||= perform_calculation(input)
end

# OPTIMIZED: Use bounded cache (LRU)
require 'lru_redux'

def expensive_calculation(input)
  @cache ||= LruRedux::Cache.new(1000)
  @cache.getset(input) { perform_calculation(input) }
end

# Memory saved: Prevents cache from growing unbounded
```

### Step 4: Readability and Idiom Analysis

**Detect Non-Idiomatic Code:**

**1. Conditional Assignment:**
```ruby
# NON-IDIOMATIC
if user.name.nil?
  user.name = 'Guest'
end

# IDIOMATIC
user.name ||= 'Guest'

# NON-IDIOMATIC
if value == nil
  value = default
else
  value = value
end

# IDIOMATIC
value ||= default
```

**2. Safe Navigation:**
```ruby
# NON-IDIOMATIC
if user && user.profile && user.profile.avatar
  display(user.profile.avatar)
end

# IDIOMATIC
display(user&.profile&.avatar) if user&.profile&.avatar
# or
if avatar = user&.profile&.avatar
  display(avatar)
end
```

**3. Enumerable Methods:**
```ruby
# NON-IDIOMATIC
found = nil
users.each do |user|
  if user.active?
    found = user
    break
  end
end

# IDIOMATIC
found = users.find(&:active?)

# NON-IDIOMATIC
actives = []
users.each do |user|
  actives << user if user.active?
end

# IDIOMATIC
actives = users.select(&:active?)

# NON-IDIOMATIC
total = 0
prices.each { |price| total += price }

# IDIOMATIC
total = prices.sum
# or
total = prices.reduce(:+)
```

**4. Guard Clauses:**
```ruby
# NON-IDIOMATIC
def process(user)
  if user
    if user.active?
      if user.verified?
        # Main logic here
        perform_action(user)
      end
    end
  end
end

# IDIOMATIC
def process(user)
  return unless user
  return unless user.active?
  return unless user.verified?

  perform_action(user)
end
```

**5. Pattern Matching (Ruby 3.0+):**
```ruby
# LESS IDIOMATIC (Ruby 3.0+)
if response.is_a?(Hash) && response[:status] == 'success'
  handle_success(response[:data])
elsif response.is_a?(Hash) && response[:status] == 'error'
  handle_error(response[:error])
end

# MORE IDIOMATIC (Ruby 3.0+)
case response
in { status: 'success', data: }
  handle_success(data)
in { status: 'error', error: }
  handle_error(error)
end
```

**6. Block Syntax:**
```ruby
# NON-IDIOMATIC: do/end for single line
users.map do |u| u.name end

# IDIOMATIC: braces for single line
users.map { |u| u.name }

# NON-IDIOMATIC: braces for multi-line
users.select { |u|
  u.active? &&
  u.verified?
}

# IDIOMATIC: do/end for multi-line
users.select do |u|
  u.active? && u.verified?
end
```

**7. String Interpolation:**
```ruby
# NON-IDIOMATIC
"Hello " + user.name + "!"

# IDIOMATIC
"Hello #{user.name}!"

# NON-IDIOMATIC
'Total: ' + total.to_s

# IDIOMATIC
"Total: #{total}"
```

### Step 5: Generate Benchmarks

**Create Benchmark Comparisons:**

```ruby
# Generated benchmark file: benchmarks/optimization_comparison.rb
require 'benchmark'

puts "Performance Comparison"
puts "=" * 50

# Original implementation
def original_method
  # Original code
end

# Optimized implementation
def optimized_method
  # Optimized code
end

Benchmark.bm(20) do |x|
  x.report("Original:") do
    10_000.times { original_method }
  end

  x.report("Optimized:") do
    10_000.times { optimized_method }
  end
end

# Memory profiling
require 'memory_profiler'

puts "\nMemory Comparison"
puts "=" * 50

report = MemoryProfiler.report do
  original_method
end

puts "Original Memory Usage:"
puts "  Total allocated: #{report.total_allocated_memsize} bytes"
puts "  Total retained: #{report.total_retained_memsize} bytes"

report = MemoryProfiler.report do
  optimized_method
end

puts "\nOptimized Memory Usage:"
puts "  Total allocated: #{report.total_allocated_memsize} bytes"
puts "  Total retained: #{report.total_retained_memsize} bytes"
```

### Step 6: Generate Optimization Report

**Comprehensive Report Structure:**

```
================================================================================
RUBY OPTIMIZATION REPORT
================================================================================

File: app/services/data_processor.rb
Focus: all
Date: 2024-01-15

--------------------------------------------------------------------------------
SUMMARY
--------------------------------------------------------------------------------
  Total Issues Found: 18
    Performance: 8
    Memory: 5
    Readability: 5

  Potential Improvements:
    Estimated Speed Gain: 2.5x faster
    Estimated Memory Reduction: 45%
    Code Quality: +15 readability score

--------------------------------------------------------------------------------
PERFORMANCE OPTIMIZATIONS
--------------------------------------------------------------------------------

1. Inefficient Enumeration (Line 23)
   Severity: Medium
   Impact: 20% speed improvement

   Current:
     result = []
     users.each { |u| result << u.name.upcase }
     result

   Optimized:
     users.map { |u| u.name.upcase }

   Benchmark:
     Before: 1.45ms per 1000 items
     After:  1.15ms per 1000 items
     Improvement: 20.7% faster

2. N+1 Query Pattern (Line 45)
   Severity: High
   Impact: 10-100x speed improvement

   Current:
     users.map { |u| { name: u.name, posts: u.posts.count } }

   Optimized:
     users.eager(:posts).map { |u| { name: u.name, posts: u.posts.count } }

   Benchmark:
     Before: 1250ms for 100 users with 10 posts each
     After:  25ms for 100 users with 10 posts each
     Improvement: 50x faster

[... more performance issues ...]

--------------------------------------------------------------------------------
MEMORY OPTIMIZATIONS
--------------------------------------------------------------------------------

1. String Allocation in Loop (Line 67)
   Severity: Medium
   Impact: 400 bytes saved per 1000 iterations

   Current:
     1000.times { hash['key'] = value }

   Optimized:
     1000.times { hash[:key] = value }

   Memory:
     Before: 40KB allocated
     After:  160 bytes allocated
     Savings: 99.6%

[... more memory issues ...]

--------------------------------------------------------------------------------
READABILITY IMPROVEMENTS
--------------------------------------------------------------------------------

1. Non-Idiomatic Conditional (Line 89)
   Severity: Low
   Impact: Improved code clarity

   Current:
     if user.name.nil?
       user.name = 'Guest'
     end

   Idiomatic:
     user.name ||= 'Guest'

[... more readability issues ...]

--------------------------------------------------------------------------------
COMPLEXITY METRICS
--------------------------------------------------------------------------------

Method Complexity (Flog scores):
  process_data: 45.2 (High - consider refactoring)
  transform_records: 23.1 (Medium)
  validate_input: 8.5 (Low)

Recommendations:
  - Extract methods from process_data to reduce complexity
  - Consider using service objects for complex operations

--------------------------------------------------------------------------------
BENCHMARKS
--------------------------------------------------------------------------------

File Generated: benchmarks/data_processor_comparison.rb

Run benchmarks:
  ruby benchmarks/data_processor_comparison.rb

Expected Results:
  Original:   2.450s
  Optimized:  0.980s
  Speedup:    2.5x

--------------------------------------------------------------------------------
ACTION ITEMS
--------------------------------------------------------------------------------

High Priority:
  1. Fix N+1 query in line 45 (50x performance gain)
  2. Optimize string building in line 67 (99% memory reduction)
  3. Refactor process_data method (complexity: 45.2)

Medium Priority:
  4. Use map instead of each+append (20% speed gain)
  5. Cache regex patterns (30% speed gain)
  6. Implement guard clauses in validate_input

Low Priority:
  7. Use idiomatic Ruby patterns throughout
  8. Apply consistent block syntax
  9. Improve variable naming

--------------------------------------------------------------------------------
AUTOMATIC FIXES
--------------------------------------------------------------------------------

Low-risk changes that can be auto-applied:
  - String to symbol conversion (5 occurrences)
  - each to map conversion (3 occurrences)
  - Conditional to ||= conversion (4 occurrences)

Apply automatic fixes? [y/N]

================================================================================
END REPORT
================================================================================
```

### Step 7: Optional - Apply Automatic Fixes

**Safe Transformations:**

For low-risk, well-defined improvements:

```ruby
# Create optimized version of file
# app/services/data_processor_optimized.rb

# Apply automatic transformations:
# - String literals to symbols
# - each+append to map
# - if/nil? to ||=
# - Block syntax corrections

# Generate diff
# Show side-by-side comparison
# Offer to replace original or keep both
```

## Output Formats

### Console Output
- Colored severity indicators (red/yellow/green)
- Progress indicator during analysis
- Summary statistics
- Top issues highlighted

### Report Files
- Detailed markdown report
- Generated benchmark files
- Optional optimized code files
- Diff files for review

### JSON Output (Optional)
```json
{
  "file": "app/services/data_processor.rb",
  "summary": {
    "total_issues": 18,
    "performance": 8,
    "memory": 5,
    "readability": 5
  },
  "issues": [
    {
      "type": "performance",
      "severity": "high",
      "line": 45,
      "description": "N+1 query pattern",
      "impact": "50x speed improvement",
      "suggestion": "Use eager loading"
    }
  ]
}
```

## Error Handling

- Handle invalid Ruby syntax gracefully
- Skip non-Ruby files
- Report files that cannot be parsed
- Handle missing dependencies
- Warn about risky optimizations
- Preserve backups before modifications

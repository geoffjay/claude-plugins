---
name: gpui-review
description: Review GPUI code for idiomatic patterns, performance issues, state management correctness, and framework best practices
---

# GPUI Code Review

Perform comprehensive code review of GPUI applications, identifying issues with patterns, performance, state management, and suggesting improvements.

## Arguments

- `$1`: Path (optional) - Specific file or directory to review. If not provided, reviews entire project.

## Workflow

### 1. Search for GPUI Code

- Locate all `.rs` files in the project or specified path
- Identify files using GPUI (imports `gpui::*` or specific GPUI types)
- Categorize files by type:
  - View components (impl Render)
  - Models (application state)
  - Main entry points
  - Utility code

### 2. Analyze Component Patterns

Review each component for:

#### Component Structure
- [ ] Proper use of View vs Model types
- [ ] Clear separation of concerns
- [ ] Component has single responsibility
- [ ] Props/dependencies passed explicitly
- [ ] Proper lifetime management

#### Anti-patterns
- [ ] God components (doing too much)
- [ ] Tight coupling between components
- [ ] Improper state ownership
- [ ] Missing error handling
- [ ] Inconsistent naming conventions

Example issues to flag:

```rust
// BAD: Component doing too much
impl Render for GodComponent {
    fn render(&mut self, cx: &mut ViewContext<Self>) -> impl IntoElement {
        // Fetching data
        // Computing business logic
        // Rendering UI
        // Handling all events
        // Managing multiple concerns
    }
}

// GOOD: Focused component
impl Render for FocusedComponent {
    fn render(&mut self, cx: &mut ViewContext<Self>) -> impl IntoElement {
        let state = self.model.read(cx);
        div().child(format!("Count: {}", state.count))
    }
}
```

### 3. Check State Management

Review state management for:

#### Model Usage
- [ ] State properly encapsulated in Model types
- [ ] Appropriate use of `cx.new_model()`
- [ ] State updates use `model.update()`
- [ ] No direct state mutation outside updates
- [ ] Proper state ownership hierarchy

#### Subscription Management
- [ ] Subscriptions created during initialization, not render
- [ ] Subscriptions stored to prevent cleanup
- [ ] `cx.observe()` used for model changes
- [ ] No subscription leaks
- [ ] Proper cleanup in Drop if needed

Example issues to flag:

```rust
// BAD: Subscription in render (memory leak)
impl Render for BadView {
    fn render(&mut self, cx: &mut ViewContext<Self>) -> impl IntoElement {
        cx.observe(&self.model, |_, _, cx| cx.notify());  // Leak!
        div()
    }
}

// GOOD: Subscription stored
struct GoodView {
    model: Model<Data>,
    _subscription: Subscription,
}

impl GoodView {
    fn new(model: Model<Data>, cx: &mut ViewContext<Self>) -> Self {
        let _subscription = cx.observe(&model, |_, _, cx| cx.notify());
        Self { model, _subscription }
    }
}
```

#### Context Usage
- [ ] Appropriate context types (WindowContext, ViewContext, ModelContext)
- [ ] Global state used sparingly with `cx.global::<T>()`
- [ ] Context not stored (lifetime issues)
- [ ] Proper use of `cx.notify()` for updates

### 4. Review Render Performance

Analyze for performance issues:

#### Unnecessary Renders
- [ ] No expensive computations in render()
- [ ] Cached/memoized expensive operations
- [ ] Minimal `cx.notify()` calls
- [ ] No rendering on every tick/timer
- [ ] Proper use of derived state

#### Element Efficiency
- [ ] Minimal element nesting depth
- [ ] No repeated identical elements
- [ ] Efficient list rendering (consider virtualization)
- [ ] Appropriate use of keys for dynamic lists
- [ ] No unnecessary cloning in render

Example issues to flag:

```rust
// BAD: Expensive computation in render
impl Render for BadComponent {
    fn render(&mut self, cx: &mut ViewContext<Self>) -> impl IntoElement {
        let result = expensive_computation();  // Every render!
        div().child(result)
    }
}

// GOOD: Compute on state change
struct GoodComponent {
    cached_result: String,
}

impl GoodComponent {
    fn update_data(&mut self, data: Data, cx: &mut ViewContext<Self>) {
        self.cached_result = expensive_computation(&data);
        cx.notify();
    }
}
```

#### Layout Performance
- [ ] Avoid deep nesting
- [ ] Use flex layout efficiently
- [ ] Minimize layout recalculations
- [ ] Appropriate use of fixed vs dynamic sizing
- [ ] No layout thrashing

### 5. Identify Anti-Patterns

Flag common GPUI anti-patterns:

#### Memory Issues
```rust
// BAD: Circular reference
struct CircularRef {
    self_view: Option<View<Self>>,  // Circular!
}

// BAD: Unbounded growth
struct UnboundedList {
    items: Vec<Item>,  // Grows forever
}
```

#### Incorrect Context Usage
```rust
// BAD: Storing context
struct BadComponent {
    cx: ViewContext<Self>,  // Won't compile, lifetime issues
}

// GOOD: Use context in methods
impl BadComponent {
    fn do_something(&mut self, cx: &mut ViewContext<Self>) {
        // Use cx here
    }
}
```

#### Event Handling Issues
```rust
// BAD: Not preventing default when needed
div()
    .on_click(|_, cx| {
        // Action taken but event still propagates
    })

// GOOD: Prevent propagation when appropriate
div()
    .on_click(|event, cx| {
        event.stop_propagation();
        // Action taken
    })
```

### 6. Provide Actionable Suggestions

For each issue found, provide:

1. **Location**: File and line number
2. **Issue**: Clear description of the problem
3. **Why**: Explain why it's problematic
4. **Fix**: Show concrete code example of how to fix it
5. **Priority**: Critical, High, Medium, or Low

Example output format:

```
📁 src/ui/views/main_view.rs:45

❌ Issue: Subscription created in render method
Severity: Critical (Memory Leak)

Problem:
  cx.observe(&self.model, |_, _, cx| cx.notify());

This creates a new subscription every render, causing a memory leak.
Subscriptions are never cleaned up.

Fix:
  1. Add subscription field to struct:
     struct MainView {
         model: Model<Data>,
         _subscription: Subscription,
     }

  2. Create subscription in constructor:
     fn new(model: Model<Data>, cx: &mut ViewContext<Self>) -> Self {
         let _subscription = cx.observe(&model, |_, _, cx| cx.notify());
         Self { model, _subscription }
     }
```

### 7. Check Framework Best Practices

Review for GPUI best practices:

- [ ] Proper use of Element trait
- [ ] Appropriate render trait implementations
- [ ] Correct action system usage
- [ ] Proper theme integration
- [ ] Accessibility attributes where appropriate
- [ ] Error handling and user feedback
- [ ] Type safety leveraged
- [ ] Documentation for public APIs

### 8. Generate Summary Report

Provide summary including:

- Total files reviewed
- Issues found by severity (Critical, High, Medium, Low)
- Common patterns identified
- Overall code quality assessment
- Top priority fixes
- Positive patterns to highlight

Example summary:

```
GPUI Code Review Summary
========================

Files Reviewed: 15
Total Issues: 23

By Severity:
  Critical: 2  (Memory leaks, state corruption)
  High: 5      (Performance issues, anti-patterns)
  Medium: 10   (Code organization, minor inefficiencies)
  Low: 6       (Style, documentation)

Top Priority Fixes:
  1. Fix subscription leaks in MainView and SidebarView
  2. Move expensive computations out of render methods
  3. Implement proper state ownership hierarchy
  4. Add error handling for async operations
  5. Reduce component nesting depth in ComplexView

Positive Patterns:
  ✓ Good separation between UI and business logic
  ✓ Consistent theming throughout
  ✓ Proper use of Model types for state
  ✓ Good component composition in most areas

Recommendations:
  - Consider extracting reusable components from large views
  - Implement virtual scrolling for long lists
  - Add integration tests for critical user flows
  - Document component APIs and state flow
```

## Review Categories

### Architecture
- Project structure
- Module organization
- Dependency management
- Separation of concerns

### State Management
- Model usage
- Subscription patterns
- Context usage
- State ownership

### Performance
- Render efficiency
- Layout optimization
- Memory management
- Async operations

### Code Quality
- Idiomatic Rust
- Error handling
- Type safety
- Documentation

### UI/UX
- Component reusability
- Consistent styling
- Accessibility
- User feedback

## Example Usage

```bash
# Review entire project
/gpui-review

# Review specific file
/gpui-review src/ui/views/main_view.rs

# Review directory
/gpui-review src/ui/components/
```

## Notes

- Focuses on GPUI-specific patterns and idioms
- Considers both correctness and performance
- Provides educational feedback with explanations
- Prioritizes actionable, concrete suggestions
- Highlights both issues and good patterns

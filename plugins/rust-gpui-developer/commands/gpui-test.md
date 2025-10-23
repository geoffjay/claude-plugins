---
name: gpui-test
description: Generate comprehensive tests for GPUI components, views, state management, and user interactions
---

# GPUI Test Generation

Generate comprehensive tests for GPUI components including unit tests, integration tests, state management tests, and user interaction tests.

## Arguments

- `$1`: Component path (required) - Path to the component file to generate tests for

## Workflow

### 1. Analyze Component Structure

- Read the component file
- Identify component type (View, Model, Element)
- Extract component struct and fields
- Identify render method and UI structure
- Find state management patterns
- Locate event handlers and actions
- Identify dependencies and injected services

### 2. Generate Unit Tests

Create unit tests for component logic:

#### Component Initialization Tests

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use gpui::*;

    #[gpui::test]
    fn test_component_initialization() {
        App::test(|cx| {
            let state = cx.new_model(|_| AppState::default());
            let view = cx.new_view(|cx| MyComponent::new(state.clone(), cx));

            assert!(view.is_some());
        });
    }

    #[gpui::test]
    fn test_initial_state() {
        App::test(|cx| {
            let state = cx.new_model(|_| AppState {
                count: 0,
                items: vec![],
            });
            let view = cx.new_view(|cx| MyComponent::new(state.clone(), cx));

            view.update(cx, |view, cx| {
                let state = view.state.read(cx);
                assert_eq!(state.count, 0);
                assert_eq!(state.items.len(), 0);
            });
        });
    }
}
```

#### State Management Tests

```rust
#[gpui::test]
fn test_state_updates() {
    App::test(|cx| {
        let state = cx.new_model(|_| AppState { count: 0 });
        let view = cx.new_view(|cx| Counter::new(state.clone(), cx));

        // Update state
        state.update(cx, |state, cx| {
            state.count = 5;
            cx.notify();
        });

        // Verify view reflects change
        view.update(cx, |view, cx| {
            let state = view.state.read(cx);
            assert_eq!(state.count, 5);
        });
    });
}

#[gpui::test]
fn test_subscription_updates() {
    App::test(|cx| {
        let state = cx.new_model(|_| AppState { count: 0 });
        let view = cx.new_view(|cx| Counter::new(state.clone(), cx));

        let initial_render_count = view.render_count();

        // Update should trigger rerender via subscription
        state.update(cx, |state, cx| {
            state.count += 1;
            cx.notify();
        });

        assert_eq!(view.render_count(), initial_render_count + 1);
    });
}
```

### 3. Create Integration Tests

Generate integration tests for component interactions:

#### User Interaction Tests

```rust
#[gpui::test]
fn test_button_click() {
    App::test(|cx| {
        let state = cx.new_model(|_| AppState { count: 0 });
        let view = cx.new_view(|cx| Counter::new(state.clone(), cx));

        // Simulate button click
        view.update(cx, |view, cx| {
            view.handle_increment(cx);
        });

        // Verify state updated
        state.update(cx, |state, _| {
            assert_eq!(state.count, 1);
        });
    });
}

#[gpui::test]
fn test_input_change() {
    App::test(|cx| {
        let state = cx.new_model(|_| FormState::default());
        let view = cx.new_view(|cx| Form::new(state.clone(), cx));

        // Simulate input change
        view.update(cx, |view, cx| {
            view.handle_input_change("test value", cx);
        });

        // Verify state updated
        state.update(cx, |state, _| {
            assert_eq!(state.input_value, "test value");
        });
    });
}
```

#### Action Handling Tests

```rust
#[gpui::test]
fn test_action_dispatch() {
    App::test(|cx| {
        let state = cx.new_model(|_| AppState { count: 0 });
        let view = cx.new_view(|cx| Counter::new(state.clone(), cx));

        // Dispatch action
        view.update(cx, |view, cx| {
            cx.dispatch_action(Increment);
        });

        // Verify action handled
        state.update(cx, |state, _| {
            assert_eq!(state.count, 1);
        });
    });
}
```

### 4. Add Interaction Tests

Test complex user interactions:

#### Multi-Step Interactions

```rust
#[gpui::test]
fn test_complete_user_flow() {
    App::test(|cx| {
        let state = cx.new_model(|_| TodoState::default());
        let view = cx.new_view(|cx| TodoList::new(state.clone(), cx));

        view.update(cx, |view, cx| {
            // Add item
            view.handle_add_todo("Buy milk", cx);

            // Mark complete
            view.handle_toggle_todo(0, cx);

            // Delete item
            view.handle_delete_todo(0, cx);
        });

        state.update(cx, |state, _| {
            assert_eq!(state.todos.len(), 0);
        });
    });
}
```

#### Edge Cases

```rust
#[gpui::test]
fn test_empty_state() {
    App::test(|cx| {
        let state = cx.new_model(|_| AppState::default());
        let view = cx.new_view(|cx| MyComponent::new(state.clone(), cx));

        // Verify graceful handling of empty state
        view.update(cx, |view, cx| {
            let element = view.render(cx);
            // Assert renders without panic
        });
    });
}

#[gpui::test]
fn test_boundary_conditions() {
    App::test(|cx| {
        let state = cx.new_model(|_| CounterState { count: i32::MAX });
        let view = cx.new_view(|cx| Counter::new(state.clone(), cx));

        // Test overflow handling
        view.update(cx, |view, cx| {
            view.handle_increment(cx);
        });

        state.update(cx, |state, _| {
            // Should handle overflow gracefully
            assert!(state.count == i32::MAX || state.count == 0);
        });
    });
}
```

### 5. Generate Test Utilities

Create helper functions for testing:

```rust
// Test helpers
mod test_utils {
    use super::*;
    use gpui::*;

    pub fn create_test_state() -> AppState {
        AppState {
            count: 0,
            items: vec!["item1".to_string(), "item2".to_string()],
            is_loading: false,
        }
    }

    pub fn create_test_view(cx: &mut WindowContext) -> View<MyComponent> {
        let state = cx.new_model(|_| create_test_state());
        cx.new_view(|cx| MyComponent::new(state, cx))
    }

    pub fn assert_state_equals(state: &Model<AppState>, expected_count: i32, cx: &mut AppContext) {
        state.update(cx, |state, _| {
            assert_eq!(state.count, expected_count);
        });
    }
}
```

### 6. Provide Coverage Report

Generate overview of test coverage:

```rust
// Coverage targets:
// - Component initialization: ✓
// - State updates: ✓
// - User interactions: ✓
// - Action handling: ✓
// - Edge cases: ✓
// - Error handling: ⚠ (needs work)
// - Async operations: ⚠ (needs work)
```

### 7. Add Async Tests

For components with async operations:

```rust
#[gpui::test]
async fn test_async_data_loading() {
    App::test(|cx| async move {
        let state = cx.new_model(|_| DataState::default());
        let view = cx.new_view(|cx| DataView::new(state.clone(), cx));

        // Trigger async load
        view.update(cx, |view, cx| {
            view.load_data(cx);
        });

        // Wait for completion
        cx.run_until_parked();

        // Verify data loaded
        state.update(cx, |state, _| {
            assert!(state.is_loaded);
            assert!(!state.data.is_empty());
        });
    });
}

#[gpui::test]
async fn test_async_error_handling() {
    App::test(|cx| async move {
        let state = cx.new_model(|_| DataState::default());
        let view = cx.new_view(|cx| DataView::new(state.clone(), cx));

        // Trigger async operation that will fail
        view.update(cx, |view, cx| {
            view.load_data_with_error(cx);
        });

        cx.run_until_parked();

        // Verify error handled
        state.update(cx, |state, _| {
            assert!(state.error.is_some());
            assert!(!state.is_loaded);
        });
    });
}
```

### 8. Generate Property-Based Tests

For complex logic, generate property-based tests:

```rust
#[cfg(test)]
mod property_tests {
    use super::*;
    use proptest::prelude::*;

    proptest! {
        #[test]
        fn test_counter_never_negative(increments in 0..100u32, decrements in 0..100u32) {
            App::test(|cx| {
                let state = cx.new_model(|_| CounterState { count: 0 });

                state.update(cx, |state, _| {
                    for _ in 0..increments {
                        state.count += 1;
                    }
                    for _ in 0..decrements {
                        state.count = state.count.saturating_sub(1);
                    }
                });

                state.update(cx, |state, _| {
                    prop_assert!(state.count >= 0);
                    Ok(())
                }).unwrap();
            });
        }
    }
}
```

### 9. Add Benchmark Tests

Create performance benchmarks:

```rust
// benches/component_bench.rs
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn render_benchmark(c: &mut Criterion) {
    c.bench_function("component render", |b| {
        App::test(|cx| {
            let state = cx.new_model(|_| create_large_state());
            let view = cx.new_view(|cx| MyComponent::new(state, cx));

            b.iter(|| {
                view.update(cx, |view, cx| {
                    black_box(view.render(cx));
                });
            });
        });
    });
}

criterion_group!(benches, render_benchmark);
criterion_main!(benches);
```

### 10. Generate Test Documentation

Create documentation for tests:

```rust
//! Component Tests
//!
//! This module contains comprehensive tests for MyComponent including:
//!
//! - Unit tests for component logic and state management
//! - Integration tests for user interactions
//! - Async tests for data loading
//! - Property-based tests for invariants
//! - Performance benchmarks
//!
//! ## Running Tests
//!
//! ```bash
//! # Run all tests
//! cargo test
//!
//! # Run specific test
//! cargo test test_state_updates
//!
//! # Run with output
//! cargo test -- --nocapture
//!
//! # Run benchmarks
//! cargo bench
//! ```
```

## Test Categories

### Unit Tests
- Component initialization
- State management
- Helper functions
- Pure logic

### Integration Tests
- User interactions
- Component composition
- Event propagation
- Action handling

### UI Tests
- Render output
- Layout calculations
- Style application
- Theme integration

### Performance Tests
- Render benchmarks
- State update performance
- Memory usage
- Subscription efficiency

## Example Usage

```bash
# Generate tests for specific component
/gpui-test src/ui/views/counter.rs

# Generate tests for all components in directory
/gpui-test src/ui/components/

# Generate tests with benchmarks
/gpui-test src/ui/views/data_view.rs --with-benchmarks
```

## Best Practices

- Test behavior, not implementation
- Use descriptive test names
- Test edge cases and error conditions
- Keep tests focused and independent
- Use test utilities for common setup
- Document complex test scenarios
- Maintain high coverage (>80%)
- Run tests in CI/CD pipeline

## Output Structure

```
tests/
├── component_name_test.rs
│   ├── Unit tests
│   ├── Integration tests
│   └── Test utilities
└── benches/
    └── component_name_bench.rs
```

---
name: gpui-component
description: Generate reusable GPUI components with proper typing, state management, styling, and documentation
---

# GPUI Component Generator

Generate reusable, well-structured GPUI components with proper typing, state management, styling, and comprehensive documentation.

## Arguments

- `$1`: Component name (required) - Name of the component in PascalCase (e.g., "Button", "DataTable", "SearchInput")
- `$2`: Component type (optional) - Either "stateless" (default) or "stateful"

## Workflow

### 1. Gather Component Requirements

Ask user for:
- Component purpose and description
- Props/configuration needed
- Whether component needs internal state
- Event handlers required
- Styling requirements
- Accessibility needs

### 2. Generate Component Struct

Create component struct based on type:

#### Stateless Component

```rust
use gpui::*;

/// A reusable button component
///
/// # Examples
///
/// ```
/// Button::new("Click me")
///     .on_click(|cx| {
///         println!("Clicked!");
///     })
/// ```
pub struct Button {
    label: String,
    variant: ButtonVariant,
    disabled: bool,
    on_click: Option<Box<dyn Fn(&mut WindowContext)>>,
}

#[derive(Clone, Copy, PartialEq)]
pub enum ButtonVariant {
    Primary,
    Secondary,
    Destructive,
    Ghost,
}

impl Button {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            variant: ButtonVariant::Primary,
            disabled: false,
            on_click: None,
        }
    }

    pub fn variant(mut self, variant: ButtonVariant) -> Self {
        self.variant = variant;
        self
    }

    pub fn disabled(mut self, disabled: bool) -> Self {
        self.disabled = disabled;
        self
    }

    pub fn on_click(mut self, handler: impl Fn(&mut WindowContext) + 'static) -> Self {
        self.on_click = Some(Box::new(handler));
        self
    }
}
```

#### Stateful Component

```rust
use gpui::*;

/// A search input with autocomplete
pub struct SearchInput {
    query: String,
    suggestions: Vec<String>,
    selected_index: Option<usize>,
    on_search: Option<Box<dyn Fn(&str, &mut WindowContext)>>,
}

impl SearchInput {
    pub fn new() -> Self {
        Self {
            query: String::new(),
            suggestions: Vec::new(),
            selected_index: None,
            on_search: None,
        }
    }

    pub fn on_search(mut self, handler: impl Fn(&str, &mut WindowContext) + 'static) -> Self {
        self.on_search = Some(Box::new(handler));
        self
    }

    fn handle_input(&mut self, value: String, cx: &mut ViewContext<Self>) {
        self.query = value;
        self.update_suggestions(cx);
        cx.notify();
    }

    fn update_suggestions(&mut self, cx: &mut ViewContext<Self>) {
        // Update suggestions based on query
        if let Some(handler) = &self.on_search {
            handler(&self.query, cx);
        }
    }

    fn handle_key_down(&mut self, event: &KeyDownEvent, cx: &mut ViewContext<Self>) {
        match event.key.as_str() {
            "ArrowDown" => {
                self.selected_index = Some(
                    self.selected_index
                        .map(|i| (i + 1).min(self.suggestions.len() - 1))
                        .unwrap_or(0)
                );
                cx.notify();
            }
            "ArrowUp" => {
                self.selected_index = self.selected_index
                    .and_then(|i| i.checked_sub(1));
                cx.notify();
            }
            "Enter" => {
                if let Some(index) = self.selected_index {
                    self.query = self.suggestions[index].clone();
                    self.suggestions.clear();
                    cx.notify();
                }
            }
            _ => {}
        }
    }
}
```

### 3. Implement Element/Render Traits

#### Stateless Component Render

```rust
impl Render for Button {
    fn render(&mut self, cx: &mut ViewContext<Self>) -> impl IntoElement {
        let theme = cx.global::<Theme>();
        let (bg_color, text_color, hover_color) = match self.variant {
            ButtonVariant::Primary => (
                theme.primary,
                theme.primary_foreground,
                theme.primary_hover,
            ),
            ButtonVariant::Secondary => (
                theme.secondary,
                theme.secondary_foreground,
                theme.secondary_hover,
            ),
            ButtonVariant::Destructive => (
                theme.destructive,
                theme.destructive_foreground,
                theme.destructive_hover,
            ),
            ButtonVariant::Ghost => (
                hsla(0.0, 0.0, 0.0, 0.0),
                theme.foreground,
                theme.muted,
            ),
        };

        div()
            .px_4()
            .py_2()
            .bg(bg_color)
            .text_color(text_color)
            .rounded_md()
            .font_medium()
            .when(!self.disabled, |this| {
                this.cursor_pointer()
                    .hover(|this| this.bg(hover_color))
            })
            .when(self.disabled, |this| {
                this.opacity(0.5)
                    .cursor_not_allowed()
            })
            .when_some(self.on_click.take(), |this, handler| {
                this.on_click(move |_, cx| {
                    if !self.disabled {
                        handler(cx);
                    }
                })
            })
            .child(self.label.clone())
    }
}
```

#### Stateful Component Render

```rust
impl Render for SearchInput {
    fn render(&mut self, cx: &mut ViewContext<Self>) -> impl IntoElement {
        let theme = cx.global::<Theme>();

        div()
            .flex()
            .flex_col()
            .relative()
            .child(
                div()
                    .flex()
                    .items_center()
                    .px_3()
                    .py_2()
                    .bg(theme.background)
                    .border_1()
                    .border_color(theme.border)
                    .rounded_md()
                    .child(
                        input()
                            .flex_1()
                            .placeholder("Search...")
                            .value(&self.query)
                            .on_input(cx.listener(|this, value, cx| {
                                this.handle_input(value, cx);
                            }))
                            .on_key_down(cx.listener(|this, event, cx| {
                                this.handle_key_down(event, cx);
                            }))
                    )
            )
            .when(!self.suggestions.is_empty(), |this| {
                this.child(
                    div()
                        .absolute()
                        .top_full()
                        .left_0()
                        .right_0()
                        .mt_1()
                        .bg(theme.background)
                        .border_1()
                        .border_color(theme.border)
                        .rounded_md()
                        .shadow_lg()
                        .max_h_64()
                        .overflow_y_auto()
                        .children(
                            self.suggestions.iter().enumerate().map(|(i, suggestion)| {
                                div()
                                    .px_3()
                                    .py_2()
                                    .cursor_pointer()
                                    .when(self.selected_index == Some(i), |this| {
                                        this.bg(theme.accent)
                                    })
                                    .hover(|this| this.bg(theme.muted))
                                    .child(suggestion.as_str())
                            })
                        )
                )
            })
    }
}
```

### 4. Add State Management

For stateful components:

```rust
impl SearchInput {
    pub fn set_suggestions(&mut self, suggestions: Vec<String>, cx: &mut ViewContext<Self>) {
        self.suggestions = suggestions;
        self.selected_index = None;
        cx.notify();
    }

    pub fn clear(&mut self, cx: &mut ViewContext<Self>) {
        self.query.clear();
        self.suggestions.clear();
        self.selected_index = None;
        cx.notify();
    }

    pub fn query(&self) -> &str {
        &self.query
    }
}
```

### 5. Generate Styling

Create styled variants and theme integration:

```rust
// Component-specific theme
pub struct ButtonTheme {
    pub primary_bg: Hsla,
    pub primary_fg: Hsla,
    pub primary_hover: Hsla,
    pub secondary_bg: Hsla,
    pub secondary_fg: Hsla,
    pub secondary_hover: Hsla,
    pub border_radius: Pixels,
    pub padding_x: Pixels,
    pub padding_y: Pixels,
}

impl ButtonTheme {
    pub fn from_app_theme(theme: &AppTheme) -> Self {
        Self {
            primary_bg: theme.colors.primary,
            primary_fg: theme.colors.primary_foreground,
            primary_hover: theme.colors.primary_hover,
            secondary_bg: theme.colors.secondary,
            secondary_fg: theme.colors.secondary_foreground,
            secondary_hover: theme.colors.secondary_hover,
            border_radius: px(6.0),
            padding_x: px(16.0),
            padding_y: px(8.0),
        }
    }
}
```

### 6. Create Documentation

Generate comprehensive documentation:

```rust
//! Button Component
//!
//! A flexible, accessible button component with multiple variants and states.
//!
//! # Features
//!
//! - Multiple variants (Primary, Secondary, Destructive, Ghost)
//! - Disabled state support
//! - Customizable click handlers
//! - Full keyboard accessibility
//! - Theme integration
//!
//! # Examples
//!
//! ## Basic Usage
//!
//! ```rust
//! let button = Button::new("Click me")
//!     .on_click(|cx| {
//!         println!("Button clicked!");
//!     });
//! ```
//!
//! ## With Variants
//!
//! ```rust
//! let primary = Button::new("Primary").variant(ButtonVariant::Primary);
//! let secondary = Button::new("Secondary").variant(ButtonVariant::Secondary);
//! let destructive = Button::new("Delete").variant(ButtonVariant::Destructive);
//! ```
//!
//! ## Disabled State
//!
//! ```rust
//! let button = Button::new("Disabled")
//!     .disabled(true);
//! ```
//!
//! # Accessibility
//!
//! - Supports keyboard navigation (Enter/Space to activate)
//! - Proper ARIA attributes
//! - Focus indicators
//! - Disabled state communicated to screen readers
```

### 7. Provide Usage Examples

Create example usage code:

```rust
// examples/button_example.rs
use gpui::*;

fn main() {
    App::new("com.example.button-demo", |cx| {
        cx.open_window(
            WindowOptions::default(),
            |cx| cx.new_view(|cx| ButtonDemo::new(cx))
        )
    }).run();
}

struct ButtonDemo;

impl ButtonDemo {
    fn new(cx: &mut ViewContext<Self>) -> Self {
        Self
    }
}

impl Render for ButtonDemo {
    fn render(&mut self, cx: &mut ViewContext<Self>) -> impl IntoElement {
        div()
            .flex()
            .flex_col()
            .gap_4()
            .p_8()
            .child(
                Button::new("Primary Button")
                    .variant(ButtonVariant::Primary)
                    .on_click(|cx| {
                        println!("Primary clicked!");
                    })
            )
            .child(
                Button::new("Secondary Button")
                    .variant(ButtonVariant::Secondary)
                    .on_click(|cx| {
                        println!("Secondary clicked!");
                    })
            )
            .child(
                Button::new("Destructive Button")
                    .variant(ButtonVariant::Destructive)
                    .on_click(|cx| {
                        println!("Destructive clicked!");
                    })
            )
            .child(
                Button::new("Disabled Button")
                    .disabled(true)
            )
    }
}
```

### 8. Add Component Tests

Generate tests for the component:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[gpui::test]
    fn test_button_creation() {
        App::test(|cx| {
            let button = Button::new("Test");
            assert_eq!(button.label, "Test");
            assert_eq!(button.variant, ButtonVariant::Primary);
            assert!(!button.disabled);
        });
    }

    #[gpui::test]
    fn test_button_click() {
        App::test(|cx| {
            let clicked = Rc::new(RefCell::new(false));
            let clicked_clone = clicked.clone();

            let button = Button::new("Test")
                .on_click(move |_| {
                    *clicked_clone.borrow_mut() = true;
                });

            // Simulate click
            if let Some(handler) = button.on_click {
                handler(cx);
            }

            assert!(*clicked.borrow());
        });
    }
}
```

### 9. Generate Component Module

Create module file with exports:

```rust
// src/ui/components/button/mod.rs

mod button;
mod theme;

pub use button::{Button, ButtonVariant};
pub use theme::ButtonTheme;
```

### 10. Provide Integration Instructions

Output integration guide:

```
✓ Created Button component

Files created:
  - src/ui/components/button/button.rs
  - src/ui/components/button/theme.rs
  - src/ui/components/button/mod.rs
  - examples/button_example.rs
  - tests/button_test.rs

Next steps:

1. Add to your components module:
   In src/ui/components/mod.rs:
   pub mod button;
   pub use button::Button;

2. Use in your views:
   use crate::ui::components::Button;

   Button::new("Click me")
       .variant(ButtonVariant::Primary)
       .on_click(|cx| {
           // Handle click
       })

3. Run example:
   cargo run --example button_example

4. Run tests:
   cargo test button

Documentation: See generated component docs for full API
```

## Component Types

### Stateless Components
- No internal state
- Pure rendering based on props
- Examples: Button, Icon, Label

### Stateful Components
- Internal state management
- User input handling
- Examples: Input, SearchBox, Dropdown

### Container Components
- Manage child components
- State coordination
- Examples: Form, List, Tabs

### Composite Components
- Combine multiple components
- Complex functionality
- Examples: DataTable, Dialog, Wizard

## Best Practices

- Builder pattern for configuration
- Theme integration
- Accessibility attributes
- Comprehensive documentation
- Usage examples
- Unit tests
- Type safety
- Error handling

## Example Usage

```bash
# Generate stateless component
/gpui-component Button

# Generate stateful component
/gpui-component SearchInput stateful

# Generate with custom requirements
/gpui-component DataTable stateful --with-examples --with-tests
```

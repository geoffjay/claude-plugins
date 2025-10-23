---
name: gpui-scaffold
description: Scaffold new GPUI applications with modern structure, Cargo workspace setup, component organization, and best practices
---

# GPUI Project Scaffolding

Scaffold a new GPUI application with modern project structure, best practices, and example components.

## Arguments

- `$1`: Project name (required) - Name for the new GPUI project (hyphen-case recommended)
- `$2`: Template type (optional) - Either "app" (default) or "library"

## Workflow

### 1. Validate Project Name

- Check that project name is provided
- Validate naming convention (lowercase, hyphens, no spaces)
- Check that directory doesn't already exist
- Confirm project creation with user if needed

### 2. Create Directory Structure

Create the following structure:

```
project-name/
├── Cargo.toml
├── .gitignore
├── README.md
├── src/
│   ├── main.rs (for app) or lib.rs (for library)
│   ├── app.rs
│   ├── ui/
│   │   ├── mod.rs
│   │   ├── views/
│   │   │   ├── mod.rs
│   │   │   └── main_view.rs
│   │   ├── components/
│   │   │   ├── mod.rs
│   │   │   ├── button.rs
│   │   │   └── input.rs
│   │   └── theme.rs
│   ├── models/
│   │   ├── mod.rs
│   │   └── app_state.rs
│   └── utils/
│       └── mod.rs
├── examples/
│   └── basic.rs
└── tests/
    └── integration_test.rs
```

### 3. Generate Cargo.toml

Create `Cargo.toml` with:

```toml
[package]
name = "project-name"
version = "0.1.0"
edition = "2021"

[dependencies]
gpui = { git = "https://github.com/zed-industries/zed" }
anyhow = "1.0"
log = "0.4"
env_logger = "0.11"

[dev-dependencies]
criterion = "0.5"

[[bench]]
name = "rendering"
harness = false
```

### 4. Create Main Entry Point

For applications (`main.rs`):

```rust
use gpui::*;
mod app;
mod ui;
mod models;
mod utils;

use app::App;

fn main() {
    env_logger::init();

    App::new("com.example.project-name", |cx| {
        let app = cx.new_model(|cx| app::AppModel::new(cx));
        let window = cx.open_window(
            WindowOptions {
                bounds: WindowBounds::Fixed(Bounds {
                    origin: point(px(100.0), px(100.0)),
                    size: size(px(1200.0), px(800.0)),
                }),
                ..Default::default()
            },
            |cx| cx.new_view(|cx| ui::views::MainView::new(app.clone(), cx)),
        );

        window.unwrap()
    })
    .run();
}
```

For libraries (`lib.rs`):

```rust
pub mod ui;
pub mod models;
pub mod utils;

pub use ui::*;
pub use models::*;
```

### 5. Create App Model

Generate `src/app.rs`:

```rust
use gpui::*;
use crate::models::AppState;

pub struct AppModel {
    state: Model<AppState>,
}

impl AppModel {
    pub fn new(cx: &mut ModelContext<Self>) -> Self {
        Self {
            state: cx.new_model(|_| AppState::default()),
        }
    }

    pub fn state(&self) -> &Model<AppState> {
        &self.state
    }
}
```

### 6. Create Component Structure

Generate main view (`src/ui/views/main_view.rs`):

```rust
use gpui::*;
use crate::app::AppModel;
use crate::ui::components::{Button, Input};

pub struct MainView {
    app: Model<AppModel>,
    _subscription: Subscription,
}

impl MainView {
    pub fn new(app: Model<AppModel>, cx: &mut ViewContext<Self>) -> Self {
        let subscription = cx.observe(&app, |_, _, cx| cx.notify());

        Self {
            app,
            _subscription: subscription,
        }
    }
}

impl Render for MainView {
    fn render(&mut self, cx: &mut ViewContext<Self>) -> impl IntoElement {
        let theme = cx.global::<Theme>();

        div()
            .flex()
            .flex_col()
            .size_full()
            .bg(theme.background)
            .child(
                div()
                    .flex()
                    .items_center()
                    .justify_center()
                    .flex_1()
                    .child("Welcome to your GPUI app!")
            )
    }
}
```

Generate reusable components (`src/ui/components/button.rs`, `src/ui/components/input.rs`).

### 7. Add Example Components

Create example button component:

```rust
use gpui::*;

pub struct Button {
    label: String,
    on_click: Option<Box<dyn Fn(&mut WindowContext)>>,
}

impl Button {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            on_click: None,
        }
    }

    pub fn on_click(mut self, handler: impl Fn(&mut WindowContext) + 'static) -> Self {
        self.on_click = Some(Box::new(handler));
        self
    }
}

impl Render for Button {
    fn render(&mut self, cx: &mut ViewContext<Self>) -> impl IntoElement {
        let theme = cx.global::<Theme>();
        let on_click = self.on_click.take();

        div()
            .px_4()
            .py_2()
            .bg(theme.primary)
            .text_color(theme.primary_foreground)
            .rounded_md()
            .cursor_pointer()
            .hover(|style| style.bg(theme.primary_hover))
            .when_some(on_click, |this, handler| {
                this.on_click(move |_, cx| handler(cx))
            })
            .child(self.label.clone())
    }
}
```

### 8. Generate Theme System

Create `src/ui/theme.rs`:

```rust
use gpui::*;

#[derive(Clone)]
pub struct Theme {
    pub background: Hsla,
    pub foreground: Hsla,
    pub primary: Hsla,
    pub primary_foreground: Hsla,
    pub primary_hover: Hsla,
    pub border: Hsla,
}

impl Default for Theme {
    fn default() -> Self {
        Self::light()
    }
}

impl Theme {
    pub fn light() -> Self {
        Self {
            background: rgb(0xffffff),
            foreground: rgb(0x000000),
            primary: rgb(0x2563eb),
            primary_foreground: rgb(0xffffff),
            primary_hover: rgb(0x1d4ed8),
            border: rgb(0xe5e7eb),
        }
    }

    pub fn dark() -> Self {
        Self {
            background: rgb(0x1f2937),
            foreground: rgb(0xf9fafb),
            primary: rgb(0x3b82f6),
            primary_foreground: rgb(0xffffff),
            primary_hover: rgb(0x2563eb),
            border: rgb(0x374151),
        }
    }
}
```

### 9. Generate README

Create comprehensive README.md with:
- Project description
- Installation instructions
- Usage examples
- Development setup
- Building and running instructions
- Testing guidelines
- Contributing information

### 10. Add .gitignore

```
/target/
Cargo.lock
*.swp
*.swo
.DS_Store
```

### 11. Initialize Git Repository (Optional)

- Run `git init`
- Create initial commit
- Ask user if they want to push to remote

### 12. Provide Next Steps

Output guidance:
```
✓ Created GPUI project: project-name

Next steps:
  cd project-name
  cargo build
  cargo run

Project structure:
  - src/main.rs: Application entry point
  - src/app.rs: Application model
  - src/ui/: UI components and views
  - src/models/: Application state models
  - src/utils/: Utility functions

To add components:
  - Create new files in src/ui/components/
  - Add to src/ui/components/mod.rs
  - Use in your views

Documentation:
  - GPUI: https://github.com/zed-industries/zed/tree/main/crates/gpui
  - Examples: See examples/ directory
```

## Best Practices Included

- Modern project structure with clear separation of concerns
- Theme system for consistent styling
- Reusable component patterns
- Example components to get started
- Proper subscription management
- Type-safe state management
- Development tools (examples, tests)

## Example Usage

```bash
# Scaffold new application
/gpui-scaffold my-gpui-app

# Scaffold library project
/gpui-scaffold my-gpui-lib library
```

## Notes

- Uses latest GPUI from git (stable API)
- Follows Rust 2021 edition conventions
- Includes development dependencies for testing
- Sets up proper module structure
- Includes example code for common patterns

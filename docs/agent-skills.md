# Agent Skills Reference

This document catalogs all agent skills with progressive disclosure patterns across the marketplace.

## Overview

- **Total Skills**: 25
- **Total Plugins**: 7
- **Last Updated**: 2025-11-04 11:27:39

---

## What are Agent Skills?

Agent skills are modular knowledge packages that use progressive disclosure architecture:

1. **Metadata** (Frontmatter) - Always loaded
2. **Instructions** - Core guidance loaded when activated
3. **Resources** (assets/) - Loaded on demand

All skills follow the [Anthropic Agent Skills Specification](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md).

---


## claude-plugin

**Description**: Plugin management and scaffolding tools for creating and maintaining Claude Code plugins

**Version**: 1.0.0


**Skills**:



### marketplace-update

Updates the .claude-plugin/marketplace.json file when plugins are added, modified, or removed. Use when creating or updating plugin entries in the marketplace catalog.

**Location**: `plugins/claude-plugin/skills/marketplace-update/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation




### documentation-update

Regenerates documentation files (agents.md, agent-skills.md, plugins.md, usage.md) from marketplace data using Jinja templates. Use when plugins are added, updated, or removed to keep documentation in sync.

**Location**: `plugins/claude-plugin/skills/documentation-update/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation



















































---


## golang-development

**Description**: Experienced Go development patterns and tools

**Version**: 1.0.0


**Skills**:







### go-patterns

Modern Go patterns, idioms, and best practices from Go 1.18+. Use when user needs guidance on idiomatic Go code, design patterns, or modern Go features like generics and workspaces.

**Location**: `plugins/golang-development/skills/go-patterns/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation




### go-concurrency

Advanced concurrency patterns with goroutines, channels, context, and synchronization primitives. Use when working with concurrent Go code, implementing parallel processing, or debugging race conditions.

**Location**: `plugins/golang-development/skills/go-concurrency/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation




### go-optimization

Performance optimization techniques including profiling, memory management, benchmarking, and runtime tuning. Use when optimizing Go code performance, reducing memory usage, or analyzing bottlenecks.

**Location**: `plugins/golang-development/skills/go-optimization/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation













































---


## ruby-sinatra-advanced

**Description**: Advanced Ruby development tools with a focus on the Sinatra web framework

**Version**: 1.0.0


**Skills**:













### sinatra-patterns

Common Sinatra patterns, routing strategies, error handling, and application organization. Use when building Sinatra applications or designing routes.

**Location**: `plugins/ruby-sinatra-advanced/skills/sinatra-patterns/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation




### ruby-patterns

Modern Ruby idioms, design patterns, metaprogramming techniques, and best practices. Use when writing Ruby code or refactoring for clarity.

**Location**: `plugins/ruby-sinatra-advanced/skills/ruby-patterns/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation




### sinatra-security

Security best practices for Sinatra applications including input validation, CSRF protection, and authentication patterns. Use when hardening applications or conducting security reviews.

**Location**: `plugins/ruby-sinatra-advanced/skills/sinatra-security/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation




### rack-middleware

Rack middleware development, configuration, and integration patterns. Use when working with middleware stacks or creating custom middleware.

**Location**: `plugins/ruby-sinatra-advanced/skills/rack-middleware/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation





































---


## git

**Description**: Git focused utilities with namespaced commands for advanced workflows

**Version**: 1.0.0


**Skills**:





















### git-conventions



**Location**: `plugins/git/skills/git-conventions/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation




### git-advanced



**Location**: `plugins/git/skills/git-advanced/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation




### git-troubleshooting



**Location**: `plugins/git/skills/git-troubleshooting/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation




### git-repository



**Location**: `plugins/git/skills/git-repository/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation





























---


## rust-gpui-developer

**Description**: Experienced Rust developer with expertise in user interface development using the gpui crate

**Version**: 1.0.0


**Skills**:





























### gpui-patterns

Common GPUI patterns including component composition, state management strategies, event handling, and action dispatching. Use when user needs guidance on GPUI patterns, component design, or state management approaches.

**Location**: `plugins/rust-gpui-developer/skills/gpui-patterns/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation




### gpui-styling

GPUI styling system including theme design, responsive layouts, visual design patterns, and style composition. Use when user needs help with styling, theming, or visual design in GPUI.

**Location**: `plugins/rust-gpui-developer/skills/gpui-styling/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation




### gpui-performance

Performance optimization techniques for GPUI including rendering optimization, layout performance, memory management, and profiling strategies. Use when user needs to optimize GPUI application performance or debug performance issues.

**Location**: `plugins/rust-gpui-developer/skills/gpui-performance/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation




### rust-ui-architecture

Architecture patterns for Rust UI applications including GPUI-specific patterns, code organization, modularity, and scalability. Use when user needs guidance on application architecture, code organization, or scaling UI applications.

**Location**: `plugins/rust-gpui-developer/skills/rust-ui-architecture/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation





















---


## rust-tokio-expert

**Description**: Experienced Rust developer with expertise in building reliable network applications using the Tokio library and its associated stack

**Version**: 1.0.0


**Skills**:





































### tokio-patterns

Common Tokio patterns and idioms for async programming. Use when implementing worker pools, request-response patterns, pub/sub, timeouts, retries, or graceful shutdown.

**Location**: `plugins/rust-tokio-expert/skills/tokio-patterns/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation




### tokio-concurrency

Advanced concurrency patterns for Tokio including fan-out/fan-in, pipeline processing, rate limiting, and coordinated shutdown. Use when building high-concurrency async systems.

**Location**: `plugins/rust-tokio-expert/skills/tokio-concurrency/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation




### tokio-networking

Network programming patterns with Hyper, Tonic, and Tower. Use when building HTTP services, gRPC applications, implementing middleware, connection pooling, or health checks.

**Location**: `plugins/rust-tokio-expert/skills/tokio-networking/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation




### tokio-troubleshooting

Debugging and troubleshooting Tokio applications using tokio-console, detecting deadlocks, memory leaks, and performance issues. Use when diagnosing async runtime problems.

**Location**: `plugins/rust-tokio-expert/skills/tokio-troubleshooting/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation













---


## rust-cli-developer

**Description**: Experienced Rust developer with expertise in building delightful CLI applications using Clap and the Rust CLI ecosystem

**Version**: 1.0.0


**Skills**:













































### clap-patterns

Common Clap patterns and idioms for argument parsing, validation, and CLI design. Use when implementing CLI arguments with Clap v4+.

**Location**: `plugins/rust-cli-developer/skills/clap-patterns/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation




### cli-ux-patterns

CLI user experience best practices for error messages, colors, progress indicators, and output formatting. Use when improving CLI usability and user experience.

**Location**: `plugins/rust-cli-developer/skills/cli-ux-patterns/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation




### cli-configuration

Configuration management patterns including file formats, precedence, environment variables, and XDG directories. Use when implementing configuration systems for CLI applications.

**Location**: `plugins/rust-cli-developer/skills/cli-configuration/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation




### cli-distribution

Distribution and packaging patterns including shell completions, man pages, cross-compilation, and release automation. Use when preparing CLI tools for distribution.

**Location**: `plugins/rust-cli-developer/skills/cli-distribution/`

**Structure**:
- `SKILL.md` - Skill definition with frontmatter
- `assets/` - Templates, configurations, examples
- `references/` - Additional documentation





---



## Progressive Disclosure Benefits

- **Token Efficiency**: Load only relevant knowledge when needed
- **Specialized Expertise**: Deep domain knowledge without bloat
- **Clear Activation**: Explicit triggers prevent unwanted invocation
- **Composability**: Mix and match skills across workflows
- **Maintainability**: Isolated updates don't affect other skills

## Using Skills

Skills are automatically invoked by agents when their trigger conditions are met. You can also manually invoke skills when needed for specific operations.

---

*This documentation is automatically generated from the marketplace catalog.*
*Last updated: 2025-11-04 11:27:39*
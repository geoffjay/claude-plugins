# Usage Guide

Comprehensive guide for using Claude Code plugins, agents, commands, and skills from this marketplace.

## Overview

This marketplace provides 5 plugin(s) with:
- 12 specialized agent(s)
- 23 command(s)
- 17 skill(s)

**Last Updated**: 2025-10-23 15:35:28

---

## Quick Start

### Using Agents

Agents are specialized domain experts invoked via the Task tool:

```
Use Task tool with subagent_type="<agent-name>"
```

**Example**:
```
Use Task tool with subagent_type="plugin-architect" to design a new plugin
```

### Using Commands

Commands are slash commands for specific workflows:

```bash
/<command-name> [arguments]
```

**Available Commands**:


- `claude-plugin:create` - Create a new Claude Code plugin with agents, commands, and/or skills
  - Plugin: claude-plugin
  - File: `plugins/claude-plugin/commands/create.md`

- `claude-plugin:update` - Update an existing Claude Code plugin by adding, modifying, or removing components
  - Plugin: claude-plugin
  - File: `plugins/claude-plugin/commands/update.md`

- `claude-plugin:documentation` - Regenerate all documentation files from marketplace data and plugin metadata
  - Plugin: claude-plugin
  - File: `plugins/claude-plugin/commands/documentation.md`

- `golang-development:scaffold` - Scaffold new Go projects with modern structure, Go modules, testing setup, CI/CD pipelines, and best practices
  - Plugin: golang-development
  - File: `plugins/golang-development/commands/scaffold.md`

- `golang-development:review` - Review Go code for idiomatic patterns, performance issues, security vulnerabilities, and common pitfalls with actionable suggestions
  - Plugin: golang-development
  - File: `plugins/golang-development/commands/review.md`

- `golang-development:test` - Generate comprehensive tests including unit tests, table-driven tests, benchmarks, and examples with high coverage
  - Plugin: golang-development
  - File: `plugins/golang-development/commands/test.md`

- `sinatra-scaffold` - Scaffold new Sinatra applications with modern structure, best practices, testing setup, and deployment configuration
  - Plugin: ruby-sinatra-advanced
  - File: `plugins/ruby-sinatra-advanced/commands/sinatra-scaffold.md`

- `sinatra-review` - Review Sinatra code for security issues, performance problems, route conflicts, and framework best practices
  - Plugin: ruby-sinatra-advanced
  - File: `plugins/ruby-sinatra-advanced/commands/sinatra-review.md`

- `sinatra-test` - Generate comprehensive tests for Sinatra routes, middleware, and helpers using RSpec or Minitest
  - Plugin: ruby-sinatra-advanced
  - File: `plugins/ruby-sinatra-advanced/commands/sinatra-test.md`

- `ruby-optimize` - Analyze and optimize Ruby code for performance, memory usage, and idiomatic patterns
  - Plugin: ruby-sinatra-advanced
  - File: `plugins/ruby-sinatra-advanced/commands/ruby-optimize.md`

- `bisect` - 
  - Plugin: git
  - File: `plugins/git/commands/bisect.md`

- `commit` - 
  - Plugin: git
  - File: `plugins/git/commands/commit.md`

- `worktree` - 
  - Plugin: git
  - File: `plugins/git/commands/worktree.md`

- `rebase-interactive` - 
  - Plugin: git
  - File: `plugins/git/commands/rebase-interactive.md`

- `stash-manager` - 
  - Plugin: git
  - File: `plugins/git/commands/stash-manager.md`

- `branch-cleanup` - 
  - Plugin: git
  - File: `plugins/git/commands/branch-cleanup.md`

- `fixup` - 
  - Plugin: git
  - File: `plugins/git/commands/fixup.md`

- `cherry-pick-helper` - 
  - Plugin: git
  - File: `plugins/git/commands/cherry-pick-helper.md`

- `reflog-recover` - 
  - Plugin: git
  - File: `plugins/git/commands/reflog-recover.md`

- `gpui-scaffold` - Scaffold new GPUI applications with modern structure, Cargo workspace setup, component organization, and best practices
  - Plugin: rust-gpui-developer
  - File: `plugins/rust-gpui-developer/commands/gpui-scaffold.md`

- `gpui-review` - Review GPUI code for idiomatic patterns, performance issues, state management correctness, and framework best practices
  - Plugin: rust-gpui-developer
  - File: `plugins/rust-gpui-developer/commands/gpui-review.md`

- `gpui-test` - Generate comprehensive tests for GPUI components, views, state management, and user interactions
  - Plugin: rust-gpui-developer
  - File: `plugins/rust-gpui-developer/commands/gpui-test.md`

- `gpui-component` - Generate reusable GPUI components with proper typing, state management, styling, and documentation
  - Plugin: rust-gpui-developer
  - File: `plugins/rust-gpui-developer/commands/gpui-component.md`


### Using Skills

Skills are automatically invoked by agents when their trigger conditions are met. Skills provide:

- Modular knowledge packages
- Progressive disclosure (metadata → instructions → resources)
- Spec-compliant with Anthropic guidelines

**Available Skills**:


- `marketplace-update` - Updates the .claude-plugin/marketplace.json file when plugins are added, modified, or removed. Use when creating or updating plugin entries in the marketplace catalog.
  - Plugin: claude-plugin
  - Path: `plugins/claude-plugin/skills/marketplace-update/`

- `documentation-update` - Regenerates documentation files (agents.md, agent-skills.md, plugins.md, usage.md) from marketplace data using Jinja templates. Use when plugins are added, updated, or removed to keep documentation in sync.
  - Plugin: claude-plugin
  - Path: `plugins/claude-plugin/skills/documentation-update/`

- `go-patterns` - Modern Go patterns, idioms, and best practices from Go 1.18+. Use when user needs guidance on idiomatic Go code, design patterns, or modern Go features like generics and workspaces.
  - Plugin: golang-development
  - Path: `plugins/golang-development/skills/go-patterns/`

- `go-concurrency` - Advanced concurrency patterns with goroutines, channels, context, and synchronization primitives. Use when working with concurrent Go code, implementing parallel processing, or debugging race conditions.
  - Plugin: golang-development
  - Path: `plugins/golang-development/skills/go-concurrency/`

- `go-optimization` - Performance optimization techniques including profiling, memory management, benchmarking, and runtime tuning. Use when optimizing Go code performance, reducing memory usage, or analyzing bottlenecks.
  - Plugin: golang-development
  - Path: `plugins/golang-development/skills/go-optimization/`

- `sinatra-patterns` - Common Sinatra patterns, routing strategies, error handling, and application organization. Use when building Sinatra applications or designing routes.
  - Plugin: ruby-sinatra-advanced
  - Path: `plugins/ruby-sinatra-advanced/skills/sinatra-patterns/`

- `ruby-patterns` - Modern Ruby idioms, design patterns, metaprogramming techniques, and best practices. Use when writing Ruby code or refactoring for clarity.
  - Plugin: ruby-sinatra-advanced
  - Path: `plugins/ruby-sinatra-advanced/skills/ruby-patterns/`

- `sinatra-security` - Security best practices for Sinatra applications including input validation, CSRF protection, and authentication patterns. Use when hardening applications or conducting security reviews.
  - Plugin: ruby-sinatra-advanced
  - Path: `plugins/ruby-sinatra-advanced/skills/sinatra-security/`

- `rack-middleware` - Rack middleware development, configuration, and integration patterns. Use when working with middleware stacks or creating custom middleware.
  - Plugin: ruby-sinatra-advanced
  - Path: `plugins/ruby-sinatra-advanced/skills/rack-middleware/`

- `git-conventions` - 
  - Plugin: git
  - Path: `plugins/git/skills/git-conventions/`

- `git-advanced` - 
  - Plugin: git
  - Path: `plugins/git/skills/git-advanced/`

- `git-troubleshooting` - 
  - Plugin: git
  - Path: `plugins/git/skills/git-troubleshooting/`

- `git-repository` - 
  - Plugin: git
  - Path: `plugins/git/skills/git-repository/`

- `gpui-patterns` - Common GPUI patterns including component composition, state management strategies, event handling, and action dispatching. Use when user needs guidance on GPUI patterns, component design, or state management approaches.
  - Plugin: rust-gpui-developer
  - Path: `plugins/rust-gpui-developer/skills/gpui-patterns/`

- `gpui-styling` - GPUI styling system including theme design, responsive layouts, visual design patterns, and style composition. Use when user needs help with styling, theming, or visual design in GPUI.
  - Plugin: rust-gpui-developer
  - Path: `plugins/rust-gpui-developer/skills/gpui-styling/`

- `gpui-performance` - Performance optimization techniques for GPUI including rendering optimization, layout performance, memory management, and profiling strategies. Use when user needs to optimize GPUI application performance or debug performance issues.
  - Plugin: rust-gpui-developer
  - Path: `plugins/rust-gpui-developer/skills/gpui-performance/`

- `rust-ui-architecture` - Architecture patterns for Rust UI applications including GPUI-specific patterns, code organization, modularity, and scalability. Use when user needs guidance on application architecture, code organization, or scaling UI applications.
  - Plugin: rust-gpui-developer
  - Path: `plugins/rust-gpui-developer/skills/rust-ui-architecture/`


---

## Common Workflows

### Creating a New Plugin

Use the `claude-plugin` plugin to create new plugins:

```bash
# Create a new plugin
/create <plugin-name> "<description>" [components]

# Example
/create golang-advanced "Advanced Go development tools" agents,commands,skills
```

### Updating an Existing Plugin

Modify plugins by adding, updating, or removing components:

```bash
# Add a new agent
/update <plugin-name> add agent <agent-name>

# Modify a command
/update <plugin-name> modify command <command-name>

# Remove a skill
/update <plugin-name> remove skill <skill-name>
```

### Working with Agents

Invoke agents for specialized tasks:

```
# For architecture and design
Use Task tool with subagent_type="plugin-architect"

# Add your task description
[Describe what you need the agent to do]
```

---

## Plugin Architecture

### Directory Structure

```
plugins/
├── <plugin-name>/
│   ├── agents/           # Specialized agents (optional)
│   │   └── agent.md
│   ├── commands/         # Slash commands (optional)
│   │   └── command.md
│   └── skills/           # Agent skills (optional)
│       └── skill-name/
│           ├── SKILL.md
│           ├── assets/
│           └── references/
```

### Component Requirements

Each plugin must have:
- At least one agent OR one command
- Proper YAML frontmatter in all files
- Clear, focused purpose
- Entry in marketplace.json

---

## Agent Reference

### Available Agents


#### plugin-architect

- **Plugin**: claude-plugin
- **Model**: claude-sonnet-4
- **Description**: Expert agent for designing and implementing Claude Code plugins following granular, composable architecture principles
- **Invocation**: `Use Task tool with subagent_type="plugin-architect"`


#### golang-pro

- **Plugin**: golang-development
- **Model**: claude-sonnet-4-20250514
- **Description**: Master Go 1.21+ with modern patterns, advanced concurrency, performance optimization, and production-ready microservices. Expert in the latest Go ecosystem including generics, workspaces, and cutting-edge frameworks. Use PROACTIVELY for Go development, architecture design, or performance optimization.
- **Invocation**: `Use Task tool with subagent_type="golang-pro"`


#### go-architect

- **Plugin**: golang-development
- **Model**: claude-sonnet-4-20250514
- **Description**: System architect specializing in Go microservices, distributed systems, and production-ready architecture. Expert in scalability, reliability, observability, and cloud-native patterns. Use PROACTIVELY for architecture design, system design reviews, or scaling strategies.
- **Invocation**: `Use Task tool with subagent_type="go-architect"`


#### go-performance

- **Plugin**: golang-development
- **Model**: claude-sonnet-4-20250514
- **Description**: Performance optimization specialist focusing on profiling, benchmarking, memory management, and Go runtime tuning. Expert in identifying bottlenecks and implementing high-performance solutions. Use PROACTIVELY for performance optimization, memory profiling, or benchmark analysis.
- **Invocation**: `Use Task tool with subagent_type="go-performance"`


#### sinatra-pro

- **Plugin**: ruby-sinatra-advanced
- **Model**: claude-sonnet-4-20250514
- **Description**: Master Sinatra 3.x+ framework with modern patterns, advanced routing, middleware composition, and production-ready applications. Expert in testing, performance, and deployment.
- **Invocation**: `Use Task tool with subagent_type="sinatra-pro"`


#### ruby-pro

- **Plugin**: ruby-sinatra-advanced
- **Model**: claude-sonnet-4-20250514
- **Description**: Master Ruby 3.x+ with modern features, advanced metaprogramming, performance optimization, and idiomatic patterns. Expert in gems, stdlib, and language internals.
- **Invocation**: `Use Task tool with subagent_type="ruby-pro"`


#### rack-specialist

- **Plugin**: ruby-sinatra-advanced
- **Model**: claude-sonnet-4-20250514
- **Description**: Specialist in Rack middleware development, web server integration, and low-level HTTP handling. Expert in custom middleware, performance tuning, and server configuration.
- **Invocation**: `Use Task tool with subagent_type="rack-specialist"`


#### sinatra-architect

- **Plugin**: ruby-sinatra-advanced
- **Model**: claude-sonnet-4-20250514
- **Description**: System architect for Sinatra applications focusing on scalability, API design, microservices patterns, and modular architecture. Expert in large-scale Sinatra systems.
- **Invocation**: `Use Task tool with subagent_type="sinatra-architect"`


#### rust-gpui-pro

- **Plugin**: rust-gpui-developer
- **Model**: claude-sonnet-4-5
- **Description**: Master Rust GPUI framework expert with deep knowledge of UI architecture, state management, component patterns, and performance optimization. Use PROACTIVELY for GPUI development, code review, or architecture decisions.
- **Invocation**: `Use Task tool with subagent_type="rust-gpui-pro"`


#### gpui-architect

- **Plugin**: rust-gpui-developer
- **Model**: claude-sonnet-4-5
- **Description**: System architect specializing in GPUI application design, component composition patterns, state management strategies, and scalable UI architecture. Use PROACTIVELY for architecture design, system design reviews, or scaling strategies.
- **Invocation**: `Use Task tool with subagent_type="gpui-architect"`


#### rust-ui-specialist

- **Plugin**: rust-gpui-developer
- **Model**: claude-sonnet-4-5
- **Description**: Rust UI specialist focused on GPUI layout system, styling, theming, responsive design, and reactive patterns. Use PROACTIVELY for UI implementation, styling decisions, or layout optimization.
- **Invocation**: `Use Task tool with subagent_type="rust-ui-specialist"`


#### gpui-performance

- **Plugin**: rust-gpui-developer
- **Model**: claude-sonnet-4-5
- **Description**: Performance optimization specialist for GPUI applications, focusing on rendering performance, memory management, profiling, and runtime tuning. Use PROACTIVELY for performance optimization, profiling analysis, or benchmark improvements.
- **Invocation**: `Use Task tool with subagent_type="gpui-performance"`



### Model Selection

Agents use different models based on task complexity:

- **Haiku**: Fast execution for deterministic tasks
  - Code generation from specs
  - Test creation
  - Documentation generation

- **Sonnet**: Complex reasoning and architecture
  - System design
  - Security audits
  - Language expertise
  - Multi-agent orchestration

---

## Best Practices

### When Creating Plugins

1. **Single Responsibility**: One plugin, one purpose
2. **Clear Naming**: Use hyphen-case, be descriptive
3. **Complete Documentation**: Include frontmatter and examples
4. **Spec Compliance**: Follow Anthropic guidelines
5. **Test Thoroughly**: Verify functionality before committing

### When Using Agents

1. **Choose the Right Agent**: Match agent expertise to task
2. **Provide Clear Context**: Detailed task descriptions
3. **Use Appropriate Models**: Haiku for speed, Sonnet for complexity
4. **Compose When Needed**: Combine multiple agents for complex workflows

### When Working with Skills

1. **Progressive Disclosure**: Load only what's needed
2. **Clear Triggers**: Use explicit activation criteria
3. **Modular Design**: Keep skills focused and reusable
4. **Document Well**: Include usage examples

---

## Marketplace Management

### Adding Plugins

Plugins are added via the marketplace update process:

1. Create plugin directory and components
2. Update `.claude-plugin/marketplace.json`
3. Regenerate documentation

### Updating Documentation

Documentation is automatically generated from the marketplace:

```bash
# Regenerate all docs
python plugins/claude-plugin/skills/documentation-update/doc_generator.py

# Generate specific file
python plugins/claude-plugin/skills/documentation-update/doc_generator.py --file agents
```

---

## Categories

Plugins are organized by category:


### Plugin-Management


- **claude-plugin** - Plugin management and scaffolding tools for creating and maintaining Claude Code plugins



### Languages


- **golang-development** - Experienced Go development patterns and tools

- **ruby-sinatra-advanced** - Advanced Ruby development tools with a focus on the Sinatra web framework

- **rust-gpui-developer** - Experienced Rust developer with expertise in user interface development using the gpui crate



### Utilities


- **git** - Git focused utilities with namespaced commands for advanced workflows




---

## Getting Help

- **Documentation**: See `docs/` directory for detailed references
- **Architecture**: See `docs/architecture.md` for design principles
- **Contributing**: See `.github/CONTRIBUTING.md` for contribution guidelines

---

## Resources

- [Architecture Documentation](./architecture.md)
- [Agent Reference](./agents.md)
- [Skills Reference](./agent-skills.md)
- [Plugin Directory](./plugins.md)

---

*This documentation is automatically generated from the marketplace catalog.*
*Last updated: 2025-10-23 15:35:28*
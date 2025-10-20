# Agent Skills Reference

This document catalogs all agent skills with progressive disclosure patterns across the marketplace.

## Overview

- **Total Skills**: 9
- **Total Plugins**: 3
- **Last Updated**: 2025-10-20 14:55:44

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
*Last updated: 2025-10-20 14:55:44*
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal Claude Code plugins marketplace repository following a granular, composable architecture. The project is currently in early development stage - the plugin infrastructure and documentation exist, but the actual plugins are not yet implemented.

## Architecture Philosophy

### Core Principles

- **Single Responsibility**: Each plugin does one thing well (Unix philosophy)
- **Composability**: Mix and match plugins based on needs rather than forced bundling
- **Context Efficiency**: Smaller, focused tools for better LLM performance
- **Progressive Disclosure**: Skills use three-tier architecture (metadata → instructions → resources)

### Target Structure

The repository is designed to support:

- **Specialized Agents**: Domain experts with deep knowledge, model-optimized (Haiku/Sonnet)
- **Workflow Orchestrators**: Multi-agent coordination systems for complex operations
- **Development Tools**: Project scaffolding, security scanning, test generation utilities
- **Agent Skills**: Modular knowledge packages following Anthropic's Agent Skills Specification

## Repository Structure

```
claude-plugins/
├── .claude-plugin/
│   └── marketplace.json          # Plugin marketplace catalog (currently empty)
├── plugins/                       # Plugin directories (to be created)
│   └── {plugin-name}/
│       ├── agents/                # Specialized agents (optional)
│       ├── commands/              # Tools and workflows (optional)
│       └── skills/                # Modular knowledge packages (optional)
├── docs/
│   └── architecture.md            # Detailed architecture documentation
├── .github/
│   ├── CONTRIBUTING.md            # Contribution guidelines
│   ├── CODE_OF_CONDUCT.md         # Community standards
│   └── ISSUE_TEMPLATE/            # Issue templates
└── README.md                      # Quick start guide
```

## Plugin Development Guidelines

### Creating a New Plugin

1. Create plugin directory: `plugins/{plugin-name}/`
2. Add at least one agent OR one command (minimum requirement)
3. Optionally add skills following progressive disclosure pattern
4. Update `.claude-plugin/marketplace.json` with plugin entry
5. Use hyphen-case for all naming

### Agent Files

Location: `plugins/{plugin-name}/agents/{agent-name}.md`

Requirements:

- Include frontmatter with name, description, and model
- Write comprehensive system prompt
- Choose appropriate model (Haiku for deterministic tasks, Sonnet for complex reasoning)

### Command Files

Location: `plugins/{plugin-name}/commands/{command-name}.md`

Purpose: Tools and workflow automation specific to the plugin domain

### Skill Files

Location: `plugins/{plugin-name}/skills/{skill-name}/SKILL.md`

Requirements:

- YAML frontmatter with `name` and `description` (include "Use when" trigger)
- Follow three-tier progressive disclosure architecture
- Comply with Anthropic Agent Skills Specification
- Keep description under 1024 characters

Example frontmatter:

```yaml
---
name: skill-name
description: What the skill does. Use when [trigger criteria].
---
```

## Quality Standards

When contributing to this repository:

- **Clear naming**: Use hyphen-case, descriptive names
- **Focused scope**: Maintain single responsibility per plugin
- **Complete documentation**: Document what, when, and how
- **Spec compliance**: Follow Anthropic guidelines for agents and skills
- **Professional tone**: No promotional content or off-topic material
- **Safety considerations**: No malicious capabilities

## Model Selection Strategy

**Use Haiku for:**

- Code generation from well-defined specs
- Test creation following established patterns
- Documentation with clear templates
- Infrastructure operations
- Deployment pipelines

**Use Sonnet for:**

- System architecture design
- Technology selection decisions
- Security audits
- Complex AI/ML pipelines
- Language-specific expertise
- Multi-agent workflow orchestration

## Current State

**Note**: This repository is in early development. The architectural framework and documentation are in place, but the `plugins/` directory is not yet populated. The `.claude-plugin/marketplace.json` file exists but is empty.

## References

- Project inspired by [wshobson/agents](https://github.com/wshobson/agents)
- Full architecture details in `docs/architecture.md`
- Contribution process in `.github/CONTRIBUTING.md`

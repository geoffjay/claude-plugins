# Usage Guide

Comprehensive guide for using Claude Code plugins, agents, commands, and skills from this marketplace.

## Overview

This marketplace provides 1 plugin(s) with:
- 1 specialized agent(s)
- 3 command(s)
- 2 skill(s)

**Last Updated**: 2025-10-17 13:44:36

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
*Last updated: 2025-10-17 13:44:36*
# Agent Skills Reference

This document catalogs all agent skills with progressive disclosure patterns across the marketplace.

## Overview

- **Total Skills**: 2
- **Total Plugins**: 1
- **Last Updated**: 2025-10-17 13:44:36

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
*Last updated: 2025-10-17 13:44:36*
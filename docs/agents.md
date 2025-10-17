# Agent Reference

This document provides a comprehensive reference of all agents available across plugins in the marketplace.

## Overview

- **Total Agents**: 1
- **Total Plugins**: 1
- **Last Updated**: 2025-10-17 13:44:36

---


## Plugin-Management Agents


### claude-plugin

**Description**: Plugin management and scaffolding tools for creating and maintaining Claude Code plugins

**Version**: 1.0.0


**Agents**:



#### plugin-architect

- **Model**: `claude-sonnet-4`
- **Description**: Expert agent for designing and implementing Claude Code plugins following granular, composable architecture principles
- **Location**: `plugins/claude-plugin/agents/plugin-architect.md`





---




## Usage

To use an agent from the command line:

```bash
# Invoke with Task tool
Use Task tool with subagent_type="<agent-name>"
```

## Model Distribution

Agents are optimized for specific models based on their complexity:

- **Haiku**: Fast execution for deterministic tasks
- **Sonnet**: Complex reasoning and architecture decisions

---

*This documentation is automatically generated from the marketplace catalog.*
*Last updated: 2025-10-17 13:44:36*
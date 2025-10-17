# Agent Reference

This document provides a comprehensive reference of all agents available across plugins in the marketplace.

## Overview

- **Total Agents**: 4
- **Total Plugins**: 2
- **Last Updated**: 2025-10-17 14:16:39

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



## Languages Agents


### golang-development

**Description**: Experienced Go development patterns and tools

**Version**: 1.0.0


**Agents**:





#### golang-pro

- **Model**: `claude-sonnet-4-20250514`
- **Description**: Master Go 1.21+ with modern patterns, advanced concurrency, performance optimization, and production-ready microservices. Expert in the latest Go ecosystem including generics, workspaces, and cutting-edge frameworks. Use PROACTIVELY for Go development, architecture design, or performance optimization.
- **Location**: `plugins/golang-development/agents/golang-pro.md`




#### go-architect

- **Model**: `claude-sonnet-4-20250514`
- **Description**: System architect specializing in Go microservices, distributed systems, and production-ready architecture. Expert in scalability, reliability, observability, and cloud-native patterns. Use PROACTIVELY for architecture design, system design reviews, or scaling strategies.
- **Location**: `plugins/golang-development/agents/go-architect.md`




#### go-performance

- **Model**: `claude-sonnet-4-20250514`
- **Description**: Performance optimization specialist focusing on profiling, benchmarking, memory management, and Go runtime tuning. Expert in identifying bottlenecks and implementing high-performance solutions. Use PROACTIVELY for performance optimization, memory profiling, or benchmark analysis.
- **Location**: `plugins/golang-development/agents/go-performance.md`





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
*Last updated: 2025-10-17 14:16:39*
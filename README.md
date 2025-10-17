# Personal Claude Plugins Marketplace

> [!WARNING]
> For now this is just a place to try out Claude plugins, not much to see here.

## Quick Start

### Step 1: Add the Marketplace

Add this marketplace to Claude Code:

```bash
/plugin marketplace add geoffjay/claude-plugins
```

This makes all plugins available for installation, but does not load any agents or tools into the Claude context.

### Step 2: Install Plugins

Browse available plugins:

```bash
/plugin
```

Install the plugins you need:

```bash
/plugin install golang-development
```

Each installed plugin only loads its specific agents, commands, and skills into the Claude context.

## Architecture Highlights

### Granular Design

- **Single responsibility** - Each plugin does one thing well
- **Minimal token usage** - Average 3.4 components per plugin
- **Composable** - Mix and match for complex workflows
- **100% coverage** - All 85 agents accessible across plugins

### Progressive Disclosure (Skills)

Three-tier architecture for token efficiency:

1. **Metadata** - Name and activation criteria (always loaded)
2. **Instructions** - Core guidance (loaded when activated)
3. **Resources** - Examples and templates (loaded on demand)

### Repository Structure

```
claude-agents/
├── .claude-plugin/
│   └── marketplace.json          # all plugins
├── plugins/
│   ├── golang-development/
│   │   ├── agents/               # Expert definitions
│   │   ├── commands/             # Scaffolding tool
│   │   └── skills/               # Specialized skills
│   └── ... (more plugins)
├── docs/                         # Comprehensive documentation
└── README.md                     # This file
```

[→ View architecture details](docs/architecture.md)

## Contributing

To add new agents, skills, or commands:

1. Identify or create the appropriate plugin directory in `plugins/`
2. Create `.md` files in the appropriate subdirectory:
   - `agents/` - For specialized agents
   - `commands/` - For tools and workflows
   - `skills/` - For modular knowledge packages
3. Follow naming conventions (lowercase, hyphen-separated)
4. Write clear activation criteria and comprehensive content
5. Update the plugin definition in `.claude-plugin/marketplace.json`

See [Architecture Documentation](docs/architecture.md) for detailed guidelines.

## Resources

### Documentation

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/overview)
- [Plugins Guide](https://docs.claude.com/en/docs/claude-code/plugins)
- [Subagents Guide](https://docs.claude.com/en/docs/claude-code/sub-agents)
- [Agent Skills Guide](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Slash Commands Reference](https://docs.claude.com/en/docs/claude-code/slash-commands)

## Attribution

This project borrows considerably from [wshobson/agents](https://github.com/wshobson/agents).

## License

MIT License - see [LICENSE](LICENSE) file for details.

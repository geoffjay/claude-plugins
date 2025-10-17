---
name: claude-plugin:create
description: Create a new Claude Code plugin with agents, commands, and/or skills
---

# Create Plugin Command

Create a new Claude Code plugin following granular, composable architecture principles.

## Arguments

- `$1` - Plugin name (required, hyphen-case format)
- `$2` - Plugin description (required)
- `$3` - Components to create: `agents`, `commands`, `skills`, or combinations like `agents,commands` (optional, defaults to prompting)
- `$4` - Additional configuration as JSON (optional)

## Usage

```bash
# Basic usage - will prompt for details
/claude-plugin:create my-plugin-name "Plugin description"

# Specify components
/claude-plugin:create my-plugin-name "Plugin description" agents,commands

# Full configuration
/claude-plugin:create golang-advanced "Advanced Go development tools" agents,commands,skills '{"category":"languages","model":"claude-sonnet-4"}'
```

## Workflow

This command orchestrates plugin creation by:

1. **Validating Input**

   - Verify plugin name follows hyphen-case convention
   - Ensure plugin doesn't already exist
   - Validate component specifications

2. **Gathering Requirements**

   - If components not specified, ask user what to create
   - Request additional details about agents (names, purposes, models)
   - Request command details (names, purposes, workflows)
   - Request skill details (names, triggers, content structure)

3. **Creating Plugin Structure**

   - Create plugin directory: `plugins/$PLUGIN_NAME/`
   - Create component directories as needed
   - Set up skill subdirectories (SKILL.md, assets/, references/)

4. **Generating Components**

   - Use Task tool with subagent_type="claude-plugin" to design and implement components
   - Create agent files with proper frontmatter
   - Create command files with argument handling
   - Create skill files with progressive disclosure

5. **Updating Marketplace**
   - Invoke marketplace-update skill to add plugin entry
   - Invoke documentation-update skill to update docs

---

## Implementation

**Plugin Name:** ${1:-"[REQUIRED]"}
**Description:** ${2:-"[REQUIRED]"}
**Components:** ${3:-"[PROMPT USER]"}
**Configuration:** ${4:-"{}"}

### Step 1: Validate Plugin Name

The plugin name must:

- Be in hyphen-case format (e.g., `my-plugin-name`)
- Not already exist in `plugins/` directory
- Be descriptive and focused on a single purpose

### Step 2: Determine Components

If components are not specified in `$3`, ask the user:

**"What components should this plugin include?"**

Options:

- **Agents** - Specialized domain experts with deep knowledge
- **Commands** - Tools and workflow automation
- **Skills** - Modular knowledge packages with progressive disclosure

The plugin must have at least one agent OR one command.

### Step 3: Gather Component Details

For each component type selected:

#### Agents

- Agent name (hyphen-case)
- Agent purpose and description
- Recommended model (haiku for deterministic tasks, sonnet for complex reasoning)
- Key capabilities
- Example use cases

#### Commands

- Command name (hyphen-case)
- Command purpose and description
- Expected arguments
- Workflow steps
- Integration points

#### Skills

- Skill name (hyphen-case)
- Skill description with "Use when" trigger
- Progressive disclosure structure
- Required assets (templates, examples)
- Reference documentation needs

### Step 4: Invoke Plugin Architect

Use Task tool with subagent_type="claude-plugin" to design and implement the plugin:

```
I need to create a new plugin called "$PLUGIN_NAME" with the following specifications:

Description: $PLUGIN_DESCRIPTION
Components: $COMPONENTS
Details: [collected from user]

Please design and implement this plugin following the architecture principles:
- Single responsibility
- Composability
- Context efficiency
- Spec compliance

Create all necessary files with proper frontmatter, documentation, and examples.
```

### Step 5: Update Repository

After plugin creation:

1. **Update Marketplace**

   Invoke the marketplace-update skill by running the Python script:

   ```bash
   python plugins/claude-plugin/skills/marketplace-update/marketplace_update.py add \
     --name "$PLUGIN_NAME" \
     --description "$PLUGIN_DESCRIPTION" \
     --version "1.0.0" \
     --category "$CATEGORY" \
     --agents "$(ls plugins/$PLUGIN_NAME/agents/*.md 2>/dev/null | xargs -n1 basename | tr '\n' ',')" \
     --commands "$(ls plugins/$PLUGIN_NAME/commands/*.md 2>/dev/null | xargs -n1 basename | tr '\n' ',')" \
     --skills "$(ls -d plugins/$PLUGIN_NAME/skills/*/ 2>/dev/null | xargs -n1 basename | tr '\n' ',')"
   ```

2. **Update Documentation**

   Invoke the documentation-update skill by running the Python script:

   ```bash
   python plugins/claude-plugin/skills/documentation-update/doc_generator.py
   ```

   This regenerates:
   - `docs/agents.md` - Agent reference
   - `docs/agent-skills.md` - Skills catalog
   - `docs/plugins.md` - Plugin directory
   - `docs/usage.md` - Usage guide

3. **Verify Structure**
   - Check all files have proper frontmatter
   - Verify naming conventions
   - Ensure documentation is complete
   - Confirm marketplace.json is valid
   - Verify all documentation files were regenerated

### Step 6: Confirm Success

Report to the user:

- ✓ Plugin created at `plugins/$PLUGIN_NAME/`
- ✓ Components created: [list]
- ✓ Marketplace updated
- ✓ Documentation updated
- Next steps or usage instructions

## Examples

### Example 1: Create Language Plugin

```bash
/claude-plugin:create rust-development "Rust language development tools" agents,commands,skills
```

This would:

- Create `plugins/rust-development/`
- Prompt for agent details (e.g., rust-pro agent)
- Prompt for command details (e.g., rust-scaffold command)
- Prompt for skill details (e.g., rust-patterns skill)
- Generate all components with proper structure
- Update marketplace and documentation

### Example 2: Create Security Plugin

```bash
/claude-plugin:create security-scanning "Security vulnerability scanning and analysis" agents,commands
```

This would:

- Create `plugins/security-scanning/`
- Prompt for security agent details
- Prompt for scanning command details
- Generate components without skills
- Update marketplace and documentation

### Example 3: Create Minimal Plugin

```bash
/claude-plugin:create test-helper "Test generation helper utilities" commands
```

This would:

- Create `plugins/test-helper/`
- Prompt for command details only
- Generate command file
- Update marketplace and documentation

## Error Handling

Common issues and resolutions:

### Plugin Already Exists

If `plugins/$PLUGIN_NAME/` exists:

- Error: "Plugin '$PLUGIN_NAME' already exists. Use /claude-plugin:update to modify existing plugins."
- Suggest using `/claude-plugin:update` command instead

### Invalid Plugin Name

If plugin name is not hyphen-case:

- Error: "Plugin name must be in hyphen-case format (e.g., 'my-plugin-name')"
- Suggest correct format

### No Components Specified

If user doesn't specify components and doesn't respond to prompts:

- Error: "At least one component (agent or command) is required"
- Prompt again with clear options

### Missing Required Arguments

If `$1` or `$2` are not provided:

- Error: "Usage: /claude-plugin:create <plugin-name> <description> [components] [config]"
- Show examples

## Notes

- This command creates new plugins only. Use `/claude-plugin:update` to modify existing plugins.
- All generated files will include proper YAML frontmatter
- The plugin-architect agent ensures adherence to architecture principles
- Skills are invoked automatically for marketplace and documentation updates
- Generated code follows best practices and spec compliance

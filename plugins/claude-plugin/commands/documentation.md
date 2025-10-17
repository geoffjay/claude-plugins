---
name: claude-plugin:documentation
description: Regenerate all documentation files from marketplace data and plugin metadata
---

# Documentation Generation Command

Regenerate all documentation files (agents.md, agent-skills.md, plugins.md, usage.md) from the marketplace catalog and plugin metadata using Jinja2 templates.

## Arguments

- `$1` - Specific file to generate: `agents`, `agent-skills`, `plugins`, `usage`, or `all` (optional, defaults to `all`)
- `$2` - Additional options as JSON (optional)

## Usage

```bash
# Regenerate all documentation files
/claude-plugin:documentation

# Regenerate specific file
/claude-plugin:documentation agents

# Dry run to preview changes
/claude-plugin:documentation all '{"dry_run": true}'

# Specify custom paths
/claude-plugin:documentation all '{"marketplace": ".claude-plugins/marketplace.json", "output": "docs"}'
```

## Workflow

This command orchestrates documentation generation by:

1. **Validating Prerequisites**

   - Verify marketplace.json exists and is valid
   - Check template files exist in documentation-update skill
   - Ensure plugin directories are accessible
   - Verify output directory exists or can be created

2. **Preparing Context**

   - Load marketplace catalog
   - Scan all plugin directories
   - Extract agent/command/skill metadata
   - Build component indexes
   - Calculate statistics

3. **Generating Documentation**

   - Invoke documentation-update skill
   - Render Jinja2 templates with context
   - Write output to docs/ directory
   - Report any warnings or errors

4. **Verifying Output**
   - Check all requested files were generated
   - Verify file formatting and structure
   - Validate links and references
   - Report success and statistics

---

## Implementation

**Target File:** ${1:-"all"}
**Options:** ${2:-"{}"}

### Step 1: Validate Prerequisites

Check that all required components exist:

```bash
# Check marketplace exists
if [ ! -f .claude-plugins/marketplace.json ]; then
  echo "Error: Marketplace file not found at .claude-plugins/marketplace.json"
  exit 1
fi

# Check skill exists
if [ ! -f plugins/claude-plugin/skills/documentation-update/doc_generator.py ]; then
  echo "Error: Documentation update skill not found"
  exit 1
fi

# Check templates exist
if [ ! -d plugins/claude-plugin/skills/documentation-update/assets ]; then
  echo "Error: Template directory not found"
  exit 1
fi

# Create docs directory if needed
mkdir -p docs
```

### Step 2: Parse Options

Extract configuration from `$2` JSON parameter:

- `dry_run`: Preview output without writing files
- `marketplace`: Custom path to marketplace.json
- `templates`: Custom path to template directory
- `output`: Custom output directory
- `verbose`: Show detailed progress

### Step 3: Invoke Documentation Update Skill

Run the documentation generation script:

```bash
# Build command with options
PYTHON_CMD="python plugins/claude-plugin/skills/documentation-update/doc_generator.py"

# Add file filter if specified
if [ "$TARGET_FILE" != "all" ]; then
  PYTHON_CMD="$PYTHON_CMD --file $TARGET_FILE"
fi

# Add custom paths if provided
if [ -n "$MARKETPLACE_PATH" ]; then
  PYTHON_CMD="$PYTHON_CMD --marketplace $MARKETPLACE_PATH"
fi

if [ -n "$TEMPLATES_PATH" ]; then
  PYTHON_CMD="$PYTHON_CMD --templates $TEMPLATES_PATH"
fi

if [ -n "$OUTPUT_PATH" ]; then
  PYTHON_CMD="$PYTHON_CMD --output $OUTPUT_PATH"
fi

# Add dry-run flag if requested
if [ "$DRY_RUN" = "true" ]; then
  PYTHON_CMD="$PYTHON_CMD --dry-run"
fi

# Add verbose flag if requested
if [ "$VERBOSE" = "true" ]; then
  PYTHON_CMD="$PYTHON_CMD --verbose"
fi

# Execute command
echo "Generating documentation..."
eval $PYTHON_CMD
```

### Step 4: Report Results

After successful generation:

```
✓ Documentation generation completed

Files generated:
- docs/agents.md (25 agents across 10 plugins)
- docs/agent-skills.md (30 skills with progressive disclosure)
- docs/plugins.md (10 plugins in 4 categories)
- docs/usage.md (Usage guide and examples)

Statistics:
- Total plugins: 10
- Total agents: 25
- Total commands: 15
- Total skills: 30

All documentation files are now synchronized with the marketplace catalog.
```

If errors occurred:

```
❌ Documentation generation failed

Errors encountered:
- Template not found: assets/agents.md.j2
- Invalid frontmatter in plugins/example/agents/test.md

Please fix the errors above and run the command again.
```

## Examples

### Example 1: Full Documentation Update

```bash
/claude-plugin:documentation
```

**Output:**
```
Generating documentation...
✓ Loading marketplace.json
✓ Scanning plugin directories
✓ Extracting metadata from 10 plugins
✓ Building component indexes
✓ Rendering templates
✓ Writing docs/agents.md
✓ Writing docs/agent-skills.md
✓ Writing docs/plugins.md
✓ Writing docs/usage.md

Documentation generation completed successfully.
```

### Example 2: Generate Single File

```bash
/claude-plugin:documentation agents
```

**Output:**
```
Generating documentation...
✓ Loading marketplace.json
✓ Scanning plugin directories
✓ Extracting agent metadata
✓ Rendering agents.md.j2 template
✓ Writing docs/agents.md

Generated docs/agents.md with 25 agents.
```

### Example 3: Dry Run

```bash
/claude-plugin:documentation all '{"dry_run": true}'
```

**Output:**
```
Dry run mode - no files will be written

Preview of docs/agents.md:
===========================
# Agent Reference

This document lists all agents available across plugins in the marketplace.

## Languages

### rust-development
...

Preview of docs/agent-skills.md:
=================================
...

Dry run completed. Run without --dry-run to write files.
```

### Example 4: Custom Paths

```bash
/claude-plugin:documentation all '{"marketplace": "custom/marketplace.json", "output": "generated-docs"}'
```

**Output:**
```
Generating documentation...
✓ Loading custom/marketplace.json
✓ Using default templates
✓ Output directory: generated-docs
✓ Generating all documentation files
✓ Writing generated-docs/agents.md
✓ Writing generated-docs/agent-skills.md
✓ Writing generated-docs/plugins.md
✓ Writing generated-docs/usage.md

Documentation generation completed successfully.
```

## Generated Files

This command generates the following documentation files:

### 1. docs/agents.md

**Purpose:** Complete reference of all agents across all plugins

**Contents:**
- Agents organized by plugin and category
- Agent name, description, and model
- Links to agent files
- Agent capabilities and use cases
- Statistics on total agents

**Example Structure:**
```markdown
# Agent Reference

## Languages

### rust-development

**Agents:**

- **rust-pro** (`claude-sonnet-4`)
  - Master Rust 1.75+ with modern async patterns...
  - File: `plugins/rust-development/agents/rust-pro.md`
```

### 2. docs/agent-skills.md

**Purpose:** Catalog of all skills with progressive disclosure details

**Contents:**
- Skills organized by plugin
- Skill name and description
- "Use when" triggers
- Skill structure and location
- Statistics on total skills

**Example Structure:**
```markdown
# Agent Skills Reference

## Plugin Management

### claude-plugin

**Skills:**

#### documentation-update

Regenerates documentation files from marketplace data using Jinja templates. Use when plugins are added, updated, or removed.

- **Location:** `plugins/claude-plugin/skills/documentation-update/`
- **Structure:** SKILL.md + assets/ + references/
```

### 3. docs/plugins.md

**Purpose:** Directory of all plugins in the marketplace

**Contents:**
- Plugins organized by category
- Plugin name, description, and version
- List of components (agents, commands, skills)
- Installation and usage information
- Statistics on total plugins

**Example Structure:**
```markdown
# Plugin Directory

## Plugin Management

### claude-plugin (v1.0.0)

Plugin management and scaffolding tools.

**Components:**
- Agents: plugin-architect
- Commands: create, update, documentation
- Skills: marketplace-update, documentation-update

**Installation:** Available by default
```

### 4. docs/usage.md

**Purpose:** Usage guide and command reference

**Contents:**
- Getting started instructions
- Command usage examples
- Workflow patterns
- Integration guides
- Best practices

**Example Structure:**
```markdown
# Usage Guide

## Getting Started

This marketplace provides Claude Code plugins following a granular, composable architecture...

## Creating Plugins

Use the `/claude-plugin:create` command to create new plugins:

\`\`\`bash
/claude-plugin:create my-plugin "Plugin description"
\`\`\`

## Updating Documentation

After making changes to plugins, regenerate documentation:

\`\`\`bash
/claude-plugin:documentation
\`\`\`
```

## Integration with Other Commands

This command is automatically invoked by:

### /claude-plugin:create

After creating a new plugin:
```
✓ Plugin created at plugins/my-plugin/
✓ Marketplace updated
⏳ Updating documentation...
✓ Documentation updated
```

### /claude-plugin:update

After updating an existing plugin:
```
✓ Plugin updated at plugins/my-plugin/
✓ Marketplace updated
⏳ Updating documentation...
✓ Documentation updated
```

### Manual Invocation

Users can also run this command manually:
- After editing plugin files directly
- To refresh documentation after git pull
- To verify documentation is up to date
- To preview changes with dry-run

## Error Handling

Common issues and resolutions:

### Marketplace Not Found

```
Error: Marketplace file not found at .claude-plugins/marketplace.json

Suggestion:
- Verify you're in the repository root
- Check that .claude-plugins/marketplace.json exists
- Run /claude-plugin:create to create your first plugin
```

### Template Not Found

```
Error: Template file not found: assets/agents.md.j2

Suggestion:
- Verify claude-plugin plugin is properly installed
- Check that all template files exist in:
  plugins/claude-plugin/skills/documentation-update/assets/
- Reinstall the claude-plugin plugin if needed
```

### Invalid Frontmatter

```
Warning: Could not parse frontmatter in plugins/my-plugin/agents/my-agent.md

Suggestion:
- Check YAML frontmatter syntax in the agent file
- Ensure frontmatter is enclosed in --- markers
- Verify required fields: name, description
- Fix syntax errors and run command again
```

### Missing Plugin Directory

```
Warning: Plugin 'my-plugin' in marketplace.json but directory not found

Suggestion:
- Verify plugins/my-plugin/ directory exists
- Remove stale entry from marketplace.json
- Recreate plugin if it was accidentally deleted
```

### Permission Denied

```
Error: Permission denied writing to docs/agents.md

Suggestion:
- Check write permissions on docs/ directory
- Ensure docs/ directory is not read-only
- Run with appropriate permissions
```

### Python Not Found

```
Error: python command not found

Suggestion:
- Install Python 3.8 or later
- Ensure python is in your PATH
- Try using python3 instead of python
```

## Template System

The documentation generation uses Jinja2 templates located in:

```
plugins/claude-plugin/skills/documentation-update/assets/
├── agents.md.j2
├── agent-skills.md.j2
├── plugins.md.j2
└── usage.md.j2
```

### Template Context

All templates receive the following context:

```python
{
  "marketplace": {
    "name": "marketplace-name",
    "owner": {...},
    "metadata": {...},
    "plugins": [...]
  },
  "plugins_by_category": {
    "category-name": [plugin1, plugin2, ...]
  },
  "all_agents": [...],
  "all_skills": [...],
  "all_commands": [...],
  "stats": {
    "total_plugins": 10,
    "total_agents": 25,
    "total_commands": 15,
    "total_skills": 30
  },
  "now": "2025-10-17"
}
```

### Customizing Templates

To customize documentation output:

1. **Edit Existing Templates**
   - Modify templates in assets/ directory
   - Use Jinja2 syntax for dynamic content
   - Test with dry-run before committing

2. **Add New Templates**
   - Create new template file in assets/
   - Update doc_generator.py to render new template
   - Define output path for new file

3. **Test Changes**
   - Run with --dry-run to preview
   - Verify formatting and structure
   - Check for template errors

## Best Practices

1. **Run After Every Plugin Change**
   - Documentation should always reflect current state
   - Commit documentation with plugin changes
   - Include in pull request reviews

2. **Use Dry Run for Testing**
   - Preview changes before writing
   - Test template modifications
   - Verify output structure

3. **Keep Templates Simple**
   - Use clear Jinja2 syntax
   - Document template variables
   - Handle missing data gracefully

4. **Validate Output**
   - Check generated files for correctness
   - Verify all links work
   - Test formatting renders properly

5. **Version Control**
   - Commit documentation changes
   - Include meaningful commit messages
   - Tag major documentation updates

## Success Criteria

After running this command:

- ✓ All requested documentation files generated
- ✓ Content matches marketplace state
- ✓ All links are valid and correct
- ✓ Formatting is consistent
- ✓ Statistics are accurate
- ✓ No template rendering errors
- ✓ All plugins represented
- ✓ Metadata correctly extracted

## Troubleshooting

### Templates Not Rendering

**Problem:** Templates fail to render with Jinja2 errors

**Solutions:**
- Check Jinja2 syntax in templates
- Verify all variables are defined
- Use default filters for optional values
- Test templates with minimal data first

### Missing Component Data

**Problem:** Some agents/commands/skills not appearing in docs

**Solutions:**
- Verify frontmatter exists and is valid
- Check file naming follows conventions
- Ensure files have correct extensions (.md)
- Verify plugin directory structure

### Outdated Documentation

**Problem:** Documentation doesn't match current plugin state

**Solutions:**
- Run this command to regenerate
- Check marketplace.json is up to date
- Verify all plugin files exist
- Look for stale cache or old files

### Performance Issues

**Problem:** Generation takes too long with many plugins

**Solutions:**
- Use --file option to generate single files
- Optimize template complexity
- Consider caching marketplace data
- Profile doc_generator.py for bottlenecks

## Related Commands

- `/claude-plugin:create` - Create new plugin (auto-generates docs)
- `/claude-plugin:update` - Update existing plugin (auto-generates docs)

## Related Skills

- `marketplace-update` - Update marketplace.json catalog
- `documentation-update` - The skill this command invokes

## Notes

- This command is idempotent - safe to run multiple times
- Generated files should be committed to version control
- Templates use Python's built-in string formatting (no external dependencies)
- The command will create the docs/ directory if it doesn't exist
- Existing documentation files are overwritten without backup
- The documentation-update skill has no external dependencies

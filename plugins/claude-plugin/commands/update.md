---
name: update
description: Update an existing Claude Code plugin by adding, modifying, or removing components
---

# Update Plugin Command

Update an existing Claude Code plugin by adding new components, modifying existing ones, or removing obsolete components.

## Arguments

- `$1` - Plugin name (required, must exist in plugins/)
- `$2` - Update operation: `add`, `modify`, or `remove` (required)
- `$3` - Component type: `agent`, `command`, or `skill` (required)
- `$4` - Component name (required for modify/remove, optional for add)
- `$5` - Additional configuration as JSON (optional)

## Usage

```bash
# Add a new agent to existing plugin
/update golang-development add agent golang-testing

# Modify an existing command
/update golang-development modify command golang-scaffold

# Remove a skill
/update golang-development remove skill golang-patterns

# Add with configuration
/update rust-development add agent rust-async '{"model":"claude-sonnet-4","description":"Async Rust expert"}'
```

## Workflow

This command orchestrates plugin updates by:

1. **Validating Input**
   - Verify plugin exists in `plugins/` directory
   - Validate operation type (add/modify/remove)
   - Ensure component type is valid
   - Check component existence for modify/remove operations

2. **Gathering Requirements**
   - For **add**: collect new component details
   - For **modify**: identify what needs to change
   - For **remove**: confirm removal and check dependencies

3. **Performing Update**
   - Use Task tool with subagent_type="claude-plugin" to execute changes
   - Create, modify, or remove component files
   - Maintain spec compliance and naming conventions

4. **Updating Marketplace**
   - Invoke marketplace-update skill to update plugin entry
   - Invoke documentation-update skill to regenerate docs

---

## Implementation

**Plugin Name:** ${1:-"[REQUIRED]"}
**Operation:** ${2:-"[REQUIRED: add|modify|remove]"}
**Component Type:** ${3:-"[REQUIRED: agent|command|skill]"}
**Component Name:** ${4:-"[REQUIRED for modify/remove]"}
**Configuration:** ${5:-"{}"}

### Step 1: Validate Plugin Exists

Check that `plugins/$PLUGIN_NAME/` exists:
- If not found: Error "Plugin '$PLUGIN_NAME' not found. Use /create to create new plugins."
- If found: Continue to operation validation

### Step 2: Validate Operation

Based on `$2` operation type:

#### Add Operation
- Create new component in existing plugin
- Component name can be provided in `$4` or prompted
- Gather full component specifications

#### Modify Operation
- Update existing component
- Component name must be provided in `$4`
- Verify component file exists
- Ask what needs to be changed

#### Remove Operation
- Delete existing component
- Component name must be provided in `$4`
- Verify component file exists
- Confirm removal with user
- Check for dependencies

### Step 3: Execute Operation

Use Task tool with subagent_type="claude-plugin" to perform the update:

#### For Add Operation

```
I need to add a new $COMPONENT_TYPE to the "$PLUGIN_NAME" plugin:

Component Name: $COMPONENT_NAME
Component Type: $COMPONENT_TYPE
Configuration: $CONFIGURATION

Please design and implement this component following architecture principles:
- Single responsibility
- Spec compliance
- Proper frontmatter
- Complete documentation

Integrate it with the existing plugin structure.
```

#### For Modify Operation

```
I need to modify the $COMPONENT_TYPE named "$COMPONENT_NAME" in the "$PLUGIN_NAME" plugin:

Changes Requested: [gathered from user]
Configuration: $CONFIGURATION

Please update the component while:
- Maintaining backward compatibility
- Following spec compliance
- Updating documentation
- Preserving existing functionality where appropriate
```

#### For Remove Operation

```
I need to remove the $COMPONENT_TYPE named "$COMPONENT_NAME" from the "$PLUGIN_NAME" plugin:

Reason: [gathered from user if needed]

Please:
- Remove the component file
- Check for and warn about any dependencies
- Update plugin structure
- Clean up any orphaned assets
```

### Step 4: Update Repository

After component update:

1. **Update Marketplace**
   - Invoke marketplace-update skill
   - Update plugin entry with new component list
   - Update version if needed

2. **Update Documentation**
   - Invoke documentation-update skill
   - Regenerate affected documentation files

3. **Verify Integrity**
   - Check plugin still has at least one agent or command
   - Verify all references are valid
   - Ensure frontmatter is correct

### Step 5: Confirm Success

Report to the user:
- ✓ Operation completed: [$OPERATION $COMPONENT_TYPE $COMPONENT_NAME]
- ✓ Plugin updated at `plugins/$PLUGIN_NAME/`
- ✓ Marketplace updated
- ✓ Documentation updated
- ✓ Current plugin structure: [list components]

## Operation Details

### Add Operation

When adding a new component:

**For Agents:**
- Prompt for agent name (hyphen-case)
- Prompt for purpose and description
- Prompt for model selection (haiku/sonnet)
- Prompt for capabilities and guidelines
- Create `plugins/$PLUGIN_NAME/agents/$AGENT_NAME.md`

**For Commands:**
- Prompt for command name (hyphen-case)
- Prompt for purpose and description
- Prompt for arguments and workflow
- Create `plugins/$PLUGIN_NAME/commands/$COMMAND_NAME.md`

**For Skills:**
- Prompt for skill name (hyphen-case)
- Prompt for description with "Use when" trigger
- Prompt for asset requirements
- Create skill directory structure:
  - `plugins/$PLUGIN_NAME/skills/$SKILL_NAME/SKILL.md`
  - `plugins/$PLUGIN_NAME/skills/$SKILL_NAME/assets/`
  - `plugins/$PLUGIN_NAME/skills/$SKILL_NAME/references/`

### Modify Operation

When modifying an existing component:

1. **Read Current Component**
   - Load existing file
   - Parse frontmatter and content
   - Show current structure to user

2. **Identify Changes**
   - Ask user what needs to change:
     - Update description
     - Change model (agents only)
     - Modify workflow
     - Update examples
     - Add/remove sections

3. **Apply Changes**
   - Update file maintaining structure
   - Preserve frontmatter format
   - Update version if significant changes

4. **Validate**
   - Ensure spec compliance
   - Verify frontmatter is valid
   - Check documentation completeness

### Remove Operation

When removing a component:

1. **Confirm Removal**
   - Show component details
   - Ask user to confirm deletion
   - Warn about potential impacts

2. **Check Dependencies**
   - Search for references to this component
   - Warn if other plugins depend on it
   - List commands that invoke this agent (if removing agent)

3. **Execute Removal**
   - Delete component file
   - Remove from marketplace entry
   - Clean up orphaned directories

4. **Verify Plugin Integrity**
   - Ensure plugin still has at least one agent or command
   - If removing last component: warn and confirm plugin deletion

## Examples

### Example 1: Add New Agent

```bash
/update golang-development add agent gin-expert
```

This would:
- Verify `plugins/golang-development/` exists
- Prompt for agent details (description, model, capabilities)
- Create `plugins/golang-development/agents/gin-expert.md`
- Update marketplace.json
- Update documentation

### Example 2: Modify Existing Command

```bash
/update security-scanning modify command sast-scan
```

This would:
- Load existing `plugins/security-scanning/commands/sast-scan.md`
- Show current configuration
- Ask what needs to change
- Update the file
- Update documentation

### Example 3: Remove Skill

```bash
/update kubernetes-operations remove skill helm-charts
```

This would:
- Confirm removal
- Check for dependencies
- Delete `plugins/kubernetes-operations/skills/helm-charts/`
- Update marketplace.json
- Update documentation

### Example 4: Add Agent with Configuration

```bash
/update python-development add agent fastapi-pro '{"model":"claude-sonnet-4","description":"FastAPI framework expert"}'
```

This would:
- Use provided configuration
- Create agent with Sonnet model
- Generate comprehensive system prompt
- Update marketplace and docs

## Error Handling

Common issues and resolutions:

### Plugin Not Found
If `plugins/$PLUGIN_NAME/` doesn't exist:
- Error: "Plugin '$PLUGIN_NAME' not found. Use /create to create new plugins."
- List available plugins

### Component Already Exists (Add)
If trying to add a component that exists:
- Error: "Component '$COMPONENT_NAME' already exists. Use 'modify' operation to update it."
- Show current component details

### Component Not Found (Modify/Remove)
If component doesn't exist:
- Error: "Component '$COMPONENT_NAME' not found in plugin '$PLUGIN_NAME'."
- List available components in plugin

### Invalid Operation
If `$2` is not add/modify/remove:
- Error: "Invalid operation. Must be: add, modify, or remove"
- Show usage examples

### Removing Last Component
If removing the last agent and command:
- Warning: "This is the last component in the plugin. Removing it will leave an empty plugin."
- Confirm: "Do you want to remove the entire plugin?"

### Dependencies Detected (Remove)
If other components reference the component being removed:
- Warning: "The following components reference '$COMPONENT_NAME': [list]"
- Confirm: "Proceed with removal? You may need to update dependent components."

## Version Management

When updating plugins:

### Minor Updates
- Adding new components
- Enhancing existing components
- Adding examples or documentation
- Increment patch version (1.0.0 → 1.0.1)

### Major Updates
- Modifying component interfaces
- Changing agent models
- Removing components
- Breaking changes
- Increment minor or major version (1.0.0 → 1.1.0 or 2.0.0)

## Notes

- This command updates existing plugins only. Use `/create` for new plugins.
- All changes maintain spec compliance and proper frontmatter
- The plugin-architect agent ensures consistency with architecture principles
- Skills are invoked automatically for marketplace and documentation updates
- Backward compatibility should be maintained when possible
- Always test updated components before committing changes

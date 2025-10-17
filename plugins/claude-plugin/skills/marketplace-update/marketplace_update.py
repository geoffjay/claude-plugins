#!/usr/bin/env python3
"""
Marketplace Update Script

Updates the .claude-plugin/marketplace.json file when plugins are added,
modified, or removed.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import argparse


class MarketplaceUpdater:
    """Handles marketplace.json updates"""

    def __init__(self, marketplace_path: str = ".claude-plugin/marketplace.json"):
        self.marketplace_path = Path(marketplace_path)
        self.marketplace_data: Dict[str, Any] = {}

    def load(self) -> None:
        """Load marketplace.json file"""
        if not self.marketplace_path.exists():
            raise FileNotFoundError(f"Marketplace file not found: {self.marketplace_path}")

        try:
            with open(self.marketplace_path, 'r') as f:
                self.marketplace_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in marketplace file: {e}")

    def save(self) -> None:
        """Save marketplace.json file"""
        with open(self.marketplace_path, 'w') as f:
            json.dump(self.marketplace_data, f, indent=2)
            f.write('\n')  # Add trailing newline

    def add_plugin(
        self,
        name: str,
        description: str,
        version: str,
        category: str = "general",
        agents: Optional[List[str]] = None,
        commands: Optional[List[str]] = None,
        skills: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None,
        license: str = "MIT",
        strict: bool = False,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
    ) -> None:
        """Add a new plugin to the marketplace"""
        self.load()

        # Check if plugin already exists
        if "plugins" not in self.marketplace_data:
            self.marketplace_data["plugins"] = []

        existing_plugin = self._find_plugin(name)
        if existing_plugin:
            raise ValueError(f"Plugin '{name}' already exists in marketplace")

        # Build plugin entry
        plugin_entry: Dict[str, Any] = {
            "name": name,
            "source": f"./plugins/{name}",
            "description": description,
            "version": version,
            "category": category,
            "license": license,
            "strict": strict,
        }

        # Add author if provided, otherwise use marketplace owner
        if author_name or author_url:
            plugin_entry["author"] = {}
            if author_name:
                plugin_entry["author"]["name"] = author_name
            if author_url:
                plugin_entry["author"]["url"] = author_url
        elif "owner" in self.marketplace_data:
            plugin_entry["author"] = {
                "name": self.marketplace_data["owner"].get("name", ""),
                "url": self.marketplace_data["owner"].get("url", ""),
            }

        # Add homepage and repository from owner if available
        if "owner" in self.marketplace_data and "url" in self.marketplace_data["owner"]:
            base_url = self.marketplace_data["owner"]["url"]
            # Extract repo name from URL if it's a GitHub URL
            if "github.com" in base_url:
                plugin_entry["homepage"] = base_url
                plugin_entry["repository"] = base_url

        # Add optional fields
        if keywords:
            plugin_entry["keywords"] = keywords

        if agents:
            plugin_entry["agents"] = [f"./agents/{agent}" for agent in agents]

        if commands:
            plugin_entry["commands"] = [f"./commands/{cmd}" for cmd in commands]

        if skills:
            plugin_entry["skills"] = [f"./skills/{skill}" for skill in skills]

        # Add plugin to marketplace
        self.marketplace_data["plugins"].append(plugin_entry)
        self.save()

        print(f"✓ Added plugin '{name}' to marketplace")

    def update_plugin(
        self,
        name: str,
        description: Optional[str] = None,
        version: Optional[str] = None,
        category: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        add_agent: Optional[str] = None,
        remove_agent: Optional[str] = None,
        add_command: Optional[str] = None,
        remove_command: Optional[str] = None,
        add_skill: Optional[str] = None,
        remove_skill: Optional[str] = None,
    ) -> None:
        """Update an existing plugin"""
        self.load()

        plugin = self._find_plugin(name)
        if not plugin:
            raise ValueError(f"Plugin '{name}' not found in marketplace")

        # Update basic fields
        if description:
            plugin["description"] = description
        if version:
            plugin["version"] = version
        if category:
            plugin["category"] = category
        if keywords:
            plugin["keywords"] = keywords

        # Update agents
        if add_agent:
            if "agents" not in plugin:
                plugin["agents"] = []
            agent_path = f"./agents/{add_agent}"
            if agent_path not in plugin["agents"]:
                plugin["agents"].append(agent_path)

        if remove_agent:
            if "agents" in plugin:
                agent_path = f"./agents/{remove_agent}"
                if agent_path in plugin["agents"]:
                    plugin["agents"].remove(agent_path)

        # Update commands
        if add_command:
            if "commands" not in plugin:
                plugin["commands"] = []
            cmd_path = f"./commands/{add_command}"
            if cmd_path not in plugin["commands"]:
                plugin["commands"].append(cmd_path)

        if remove_command:
            if "commands" in plugin:
                cmd_path = f"./commands/{remove_command}"
                if cmd_path in plugin["commands"]:
                    plugin["commands"].remove(cmd_path)

        # Update skills
        if add_skill:
            if "skills" not in plugin:
                plugin["skills"] = []
            skill_path = f"./skills/{add_skill}"
            if skill_path not in plugin["skills"]:
                plugin["skills"].append(skill_path)

        if remove_skill:
            if "skills" in plugin:
                skill_path = f"./skills/{remove_skill}"
                if skill_path in plugin["skills"]:
                    plugin["skills"].remove(skill_path)

        self.save()
        print(f"✓ Updated plugin '{name}' in marketplace")

    def remove_plugin(self, name: str) -> None:
        """Remove a plugin from the marketplace"""
        self.load()

        plugin = self._find_plugin(name)
        if not plugin:
            raise ValueError(f"Plugin '{name}' not found in marketplace")

        self.marketplace_data["plugins"].remove(plugin)
        self.save()

        print(f"✓ Removed plugin '{name}' from marketplace")

    def validate(self) -> bool:
        """Validate marketplace structure"""
        self.load()

        errors = []
        warnings = []

        # Check required top-level fields
        required_fields = ["name", "owner", "metadata", "plugins"]
        for field in required_fields:
            if field not in self.marketplace_data:
                errors.append(f"Missing required field: {field}")

        # Validate plugins
        if "plugins" in self.marketplace_data:
            plugin_names = set()
            for i, plugin in enumerate(self.marketplace_data["plugins"]):
                # Check required plugin fields
                plugin_required = ["name", "source", "description", "version"]
                for field in plugin_required:
                    if field not in plugin:
                        errors.append(f"Plugin {i}: Missing required field '{field}'")

                # Check for duplicate names
                if "name" in plugin:
                    if plugin["name"] in plugin_names:
                        errors.append(f"Duplicate plugin name: {plugin['name']}")
                    plugin_names.add(plugin["name"])

                    # Validate component file paths
                    plugin_dir = Path(f"plugins/{plugin['name']}")

                    if "agents" in plugin:
                        for agent in plugin["agents"]:
                            agent_path = plugin_dir / agent
                            if not agent_path.exists():
                                warnings.append(
                                    f"Plugin '{plugin['name']}': Agent file not found: {agent_path}"
                                )

                    if "commands" in plugin:
                        for command in plugin["commands"]:
                            cmd_path = plugin_dir / command
                            if not cmd_path.exists():
                                warnings.append(
                                    f"Plugin '{plugin['name']}': Command file not found: {cmd_path}"
                                )

                    if "skills" in plugin:
                        for skill in plugin["skills"]:
                            skill_path = plugin_dir / skill / "SKILL.md"
                            if not skill_path.exists():
                                warnings.append(
                                    f"Plugin '{plugin['name']}': Skill file not found: {skill_path}"
                                )

        # Report results
        if errors:
            print("❌ Validation failed with errors:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("✓ Validation passed with no errors")

        if warnings:
            print("\n⚠️  Warnings:")
            for warning in warnings:
                print(f"  - {warning}")

        return len(errors) == 0

    def _find_plugin(self, name: str) -> Optional[Dict[str, Any]]:
        """Find a plugin by name"""
        if "plugins" not in self.marketplace_data:
            return None

        for plugin in self.marketplace_data["plugins"]:
            if plugin.get("name") == name:
                return plugin

        return None


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Update marketplace.json")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new plugin")
    add_parser.add_argument("--name", required=True, help="Plugin name")
    add_parser.add_argument("--description", required=True, help="Plugin description")
    add_parser.add_argument("--version", required=True, help="Plugin version")
    add_parser.add_argument("--category", default="general", help="Plugin category")
    add_parser.add_argument("--agents", help="Comma-separated list of agent files")
    add_parser.add_argument("--commands", help="Comma-separated list of command files")
    add_parser.add_argument("--skills", help="Comma-separated list of skill directories")
    add_parser.add_argument("--keywords", help="Comma-separated list of keywords")
    add_parser.add_argument("--license", default="MIT", help="License type")
    add_parser.add_argument("--strict", action="store_true", help="Enable strict mode")
    add_parser.add_argument("--author-name", help="Author name")
    add_parser.add_argument("--author-url", help="Author URL")
    add_parser.add_argument(
        "--marketplace",
        default=".claude-plugin/marketplace.json",
        help="Path to marketplace.json",
    )

    # Update command
    update_parser = subparsers.add_parser("update", help="Update an existing plugin")
    update_parser.add_argument("--name", required=True, help="Plugin name")
    update_parser.add_argument("--description", help="Updated description")
    update_parser.add_argument("--version", help="Updated version")
    update_parser.add_argument("--category", help="Updated category")
    update_parser.add_argument("--keywords", help="Updated keywords (comma-separated)")
    update_parser.add_argument("--add-agent", help="Agent file to add")
    update_parser.add_argument("--remove-agent", help="Agent file to remove")
    update_parser.add_argument("--add-command", help="Command file to add")
    update_parser.add_argument("--remove-command", help="Command file to remove")
    update_parser.add_argument("--add-skill", help="Skill directory to add")
    update_parser.add_argument("--remove-skill", help="Skill directory to remove")
    update_parser.add_argument(
        "--marketplace",
        default=".claude-plugin/marketplace.json",
        help="Path to marketplace.json",
    )

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a plugin")
    remove_parser.add_argument("--name", required=True, help="Plugin name")
    remove_parser.add_argument(
        "--marketplace",
        default=".claude-plugin/marketplace.json",
        help="Path to marketplace.json",
    )

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate marketplace.json")
    validate_parser.add_argument(
        "--marketplace",
        default=".claude-plugin/marketplace.json",
        help="Path to marketplace.json",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        updater = MarketplaceUpdater(
            getattr(args, "marketplace", ".claude-plugin/marketplace.json")
        )

        if args.command == "add":
            updater.add_plugin(
                name=args.name,
                description=args.description,
                version=args.version,
                category=args.category,
                agents=args.agents.split(",") if args.agents else None,
                commands=args.commands.split(",") if args.commands else None,
                skills=args.skills.split(",") if args.skills else None,
                keywords=args.keywords.split(",") if args.keywords else None,
                license=args.license,
                strict=args.strict,
                author_name=args.author_name,
                author_url=args.author_url,
            )

        elif args.command == "update":
            updater.update_plugin(
                name=args.name,
                description=args.description,
                version=args.version,
                category=args.category,
                keywords=args.keywords.split(",") if args.keywords else None,
                add_agent=args.add_agent,
                remove_agent=args.remove_agent,
                add_command=args.add_command,
                remove_command=args.remove_command,
                add_skill=args.add_skill,
                remove_skill=args.remove_skill,
            )

        elif args.command == "remove":
            updater.remove_plugin(name=args.name)

        elif args.command == "validate":
            if not updater.validate():
                sys.exit(1)

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

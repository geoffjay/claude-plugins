#!/usr/bin/env python3
"""
Documentation Generator

Generates documentation files from marketplace data using Jinja2 templates.
"""

import json
import os
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import argparse


class SimpleTemplate:
    """Minimal Jinja2-like template engine"""

    def __init__(self, template_str: str):
        self.template = template_str

    def render(self, context: Dict[str, Any]) -> str:
        """Render template with context"""
        result = self.template

        # Replace simple variables: {{ variable }}
        for key, value in context.items():
            result = result.replace(f"{{{{ {key} }}}}", str(value))

        # Handle loops: {% for item in items %}...{% endfor %}
        for_pattern = r'{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%}(.*?){%\s*endfor\s*%}'

        def replace_for(match):
            var_name = match.group(1)
            list_name = match.group(2)
            loop_body = match.group(3)

            if list_name not in context:
                return ""

            items = context[list_name]
            if not isinstance(items, list):
                return ""

            output = []
            for item in items:
                # Create loop context
                loop_context = context.copy()
                loop_context[var_name] = item

                # Replace variables in loop body
                body_result = loop_body
                if isinstance(item, dict):
                    for k, v in item.items():
                        body_result = body_result.replace(
                            f"{{{{ {var_name}.{k} }}}}", str(v)
                        )
                else:
                    body_result = body_result.replace(
                        f"{{{{ {var_name} }}}}", str(item)
                    )

                output.append(body_result)

            return "".join(output)

        result = re.sub(for_pattern, replace_for, result, flags=re.DOTALL)

        # Handle conditionals: {% if condition %}...{% endif %}
        if_pattern = r'{%\s*if\s+(\w+)\s*%}(.*?){%\s*endif\s*%}'

        def replace_if(match):
            condition = match.group(1)
            body = match.group(2)

            if condition in context and context[condition]:
                return body
            return ""

        result = re.sub(if_pattern, replace_if, result, flags=re.DOTALL)

        # Clean up any remaining template syntax
        result = re.sub(r'{%.*?%}', '', result)
        result = re.sub(r'{{.*?}}', '', result)

        return result


class DocGenerator:
    """Generates documentation from marketplace data"""

    def __init__(
        self,
        marketplace_path: str = ".claude-plugins/marketplace.json",
        templates_dir: str = "plugins/claude-plugin/skills/documentation-update/assets",
        output_dir: str = "docs",
    ):
        self.marketplace_path = Path(marketplace_path)
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        self.marketplace_data: Dict[str, Any] = {}

    def load_marketplace(self) -> None:
        """Load marketplace.json"""
        if not self.marketplace_path.exists():
            raise FileNotFoundError(f"Marketplace not found: {self.marketplace_path}")

        with open(self.marketplace_path, 'r') as f:
            self.marketplace_data = json.load(f)

    def extract_frontmatter(self, file_path: Path) -> Dict[str, str]:
        """Extract YAML frontmatter from a markdown file"""
        if not file_path.exists():
            return {}

        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # Match frontmatter between --- delimiters
            match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if not match:
                return {}

            frontmatter_text = match.group(1)
            frontmatter = {}

            # Simple YAML parsing (key: value)
            for line in frontmatter_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip().strip('"\'')

            return frontmatter

        except Exception as e:
            print(f"Warning: Could not parse frontmatter in {file_path}: {e}")
            return {}

    def build_context(self) -> Dict[str, Any]:
        """Build template context from marketplace data"""
        context = {
            "marketplace": self.marketplace_data,
            "now": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "plugins_by_category": {},
            "all_agents": [],
            "all_skills": [],
            "all_commands": [],
            "stats": {
                "total_plugins": 0,
                "total_agents": 0,
                "total_commands": 0,
                "total_skills": 0,
            },
        }

        if "plugins" not in self.marketplace_data:
            return context

        plugins = self.marketplace_data["plugins"]
        context["stats"]["total_plugins"] = len(plugins)

        # Organize plugins by category
        for plugin in plugins:
            category = plugin.get("category", "general")
            if category not in context["plugins_by_category"]:
                context["plugins_by_category"][category] = []
            context["plugins_by_category"][category].append(plugin)

            plugin_name = plugin.get("name", "")
            plugin_dir = Path(f"plugins/{plugin_name}")

            # Extract agent information
            if "agents" in plugin:
                for agent_path in plugin["agents"]:
                    agent_file = agent_path.replace("./agents/", "")
                    full_path = plugin_dir / agent_path.lstrip('./')
                    frontmatter = self.extract_frontmatter(full_path)

                    context["all_agents"].append({
                        "plugin": plugin_name,
                        "name": frontmatter.get("name", agent_file.replace(".md", "")),
                        "file": agent_file,
                        "description": frontmatter.get("description", ""),
                        "model": frontmatter.get("model", ""),
                    })

                context["stats"]["total_agents"] += len(plugin["agents"])

            # Extract command information
            if "commands" in plugin:
                for cmd_path in plugin["commands"]:
                    cmd_file = cmd_path.replace("./commands/", "")
                    full_path = plugin_dir / cmd_path.lstrip('./')
                    frontmatter = self.extract_frontmatter(full_path)

                    context["all_commands"].append({
                        "plugin": plugin_name,
                        "name": frontmatter.get("name", cmd_file.replace(".md", "")),
                        "file": cmd_file,
                        "description": frontmatter.get("description", ""),
                    })

                context["stats"]["total_commands"] += len(plugin["commands"])

            # Extract skill information
            if "skills" in plugin:
                for skill_path in plugin["skills"]:
                    skill_name = skill_path.replace("./skills/", "")
                    full_path = plugin_dir / skill_path.lstrip('./') / "SKILL.md"
                    frontmatter = self.extract_frontmatter(full_path)

                    context["all_skills"].append({
                        "plugin": plugin_name,
                        "name": frontmatter.get("name", skill_name),
                        "path": skill_name,
                        "description": frontmatter.get("description", ""),
                    })

                context["stats"]["total_skills"] += len(plugin["skills"])

        return context

    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render a template with context"""
        template_path = self.templates_dir / f"{template_name}.j2"

        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        with open(template_path, 'r') as f:
            template_content = f.read()

        template = SimpleTemplate(template_content)
        return template.render(context)

    def generate_all(self, dry_run: bool = False, specific_file: Optional[str] = None) -> None:
        """Generate all documentation files"""
        self.load_marketplace()
        context = self.build_context()

        docs_to_generate = {
            "agents": "agents.md",
            "agent-skills": "agent-skills.md",
            "plugins": "plugins.md",
            "usage": "usage.md",
        }

        if specific_file:
            if specific_file not in docs_to_generate:
                raise ValueError(f"Unknown documentation file: {specific_file}")
            docs_to_generate = {specific_file: docs_to_generate[specific_file]}

        for template_name, output_file in docs_to_generate.items():
            try:
                print(f"Generating {output_file}...")
                content = self.render_template(template_name, context)

                if dry_run:
                    print(f"\n--- {output_file} ---")
                    print(content[:500] + "..." if len(content) > 500 else content)
                    print()
                else:
                    output_path = self.output_dir / output_file
                    output_path.parent.mkdir(parents=True, exist_ok=True)

                    with open(output_path, 'w') as f:
                        f.write(content)

                    print(f"✓ Generated {output_path}")

            except Exception as e:
                print(f"❌ Error generating {output_file}: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Generate documentation from marketplace")
    parser.add_argument(
        "--marketplace",
        default=".claude-plugins/marketplace.json",
        help="Path to marketplace.json",
    )
    parser.add_argument(
        "--templates",
        default="plugins/claude-plugin/skills/documentation-update/assets",
        help="Path to templates directory",
    )
    parser.add_argument(
        "--output",
        default="docs",
        help="Output directory for documentation",
    )
    parser.add_argument(
        "--file",
        choices=["agents", "agent-skills", "plugins", "usage"],
        help="Generate specific file only",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show output without writing files",
    )

    args = parser.parse_args()

    try:
        generator = DocGenerator(
            marketplace_path=args.marketplace,
            templates_dir=args.templates,
            output_dir=args.output,
        )

        generator.generate_all(dry_run=args.dry_run, specific_file=args.file)

        if not args.dry_run:
            print("\n✓ Documentation generation complete")

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

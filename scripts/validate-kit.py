#!/usr/bin/env python3
"""Read-only checks for kit-owned artifacts; accepts a relocated --root."""

import argparse
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

try:
    import yaml
except ImportError:
    raise SystemExit("Install requirements-dev.txt (PyYAML) before validating the kit.")


SKILL_NAMES = ("java-spring-bootstrap", "java-spring-change", "java-spring-review")
GUIDE_NAMES = (
    "architecture-java-style", "rest-api", "dto-validation-mapping", "entities-persistence",
    "security-errors", "integrations-background", "testing", "build-configuration", "operations", "delivery-gke",
    "spring-ai", "spring-ai-implementation", "spring-ai-runtime", "spring-ai-evaluations",
)
REQUIRED_FILES = (
    "AGENTS.md",
    ".editorconfig",
    "docs/java-spring-guidelines.md",
    "docs/agent-workflow.md",
    "docs/examples/partial-updates.md",
    "config/checkstyle.xml",
    "templates/README.md",
    "templates/maven/README.md",
    "templates/application/README.md",
    "templates/liquibase/README.md",
    "templates/delivery.md",
    "templates/maven/quality-plugins.xml",
    "templates/application/application.yml",
    "templates/application/application-local.yml",
    "templates/application/application-prod.yml",
    "templates/liquibase/db.changelog-master.xml",
    "templates/liquibase/changes/2026-10-30-01-create-example.xml",
) + tuple(f".agents/skills/{name}/SKILL.md" for name in SKILL_NAMES) + tuple(
    f"docs/guidelines/{name}.md" for name in GUIDE_NAMES
)

OPTIONAL_FILES = (
    "README.md", "docs/verification.md", "verification/pom.xml",
    "verification/skill-scenarios/README.md",
)


def without_fences(content):
    """Ignore fenced examples, while retaining inline Markdown references."""
    lines = []
    fence = None
    for line in content.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            if fence is None:
                fence = marker.group(1)[0]
            elif marker.group(1)[0] == fence:
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return "\n".join(lines)


def markdown_anchors(content):
    """Heading anchors for kit Markdown, including duplicate heading suffixes."""
    anchors = set()
    for heading in re.findall(r"(?m)^#{1,6}\s+(.+?)\s*#*\s*$", without_fences(content)):
        base = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        anchor = base
        suffix = 0
        while anchor in anchors:
            suffix += 1
            anchor = f"{base}-{suffix}"
        anchors.add(anchor)
    return anchors


def reference_errors(path, content, root):
    errors = []
    for match in re.finditer(r"!?\[[^\]\n]*\]\((<[^>]+>|[^)\s]+)(?:\s+\"[^\"]*\")?\)", without_fences(content)):
        reference = match.group(1).strip("<>")
        parsed = urlsplit(reference)
        if parsed.scheme or parsed.netloc:
            continue
        destination = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path.resolve()
        label = path.relative_to(root)
        if not destination.is_relative_to(root):
            errors.append(f"{label}: reference escapes kit: {reference}")
        elif destination.is_relative_to(root / "verification") and not (root / "verification").exists():
            # The executable fixture is optional in application-adoption copies.
            continue
        elif not destination.exists():
            errors.append(f"{label}: missing local reference: {reference}")
        elif parsed.fragment and destination.suffix == ".md" and destination.is_file():
            target = content if destination == path.resolve() else destination.read_text(encoding="utf-8")
            if unquote(parsed.fragment) not in markdown_anchors(target):
                errors.append(f"{label}: missing section: {reference}")
    return errors


def skill_errors(path, content, root):
    label = path.relative_to(root)
    if not content.startswith("---\n"):
        return [f"{label}: missing YAML frontmatter"]
    parts = content.split("\n---", 1)
    if len(parts) != 2:
        return [f"{label}: unclosed YAML frontmatter"]
    try:
        metadata = yaml.safe_load(parts[0][4:])
    except yaml.YAMLError as error:
        return [f"{label}: invalid YAML frontmatter: {error}"]
    if not isinstance(metadata, dict):
        return [f"{label}: frontmatter must be a mapping"]
    errors = []
    name = metadata.get("name")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or name != path.parent.name or len(name) > 64:
        errors.append(f"{label}: name must match its lowercase-hyphenated folder")
    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        errors.append(f"{label}: description must be nonempty text of at most 1024 characters")
    return errors


def validate(root):
    root = Path(root).resolve()
    errors = []
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"Missing required file: {relative}")

    paths = {root / relative for relative in REQUIRED_FILES + OPTIONAL_FILES}
    for directory in ("templates", "config", "docs/examples", "docs/guidelines"):
        paths.update(path for path in (root / directory).rglob("*") if path.is_file())

    for path in sorted(paths):
        if not path.is_file():
            continue
        if not path.resolve().is_relative_to(root):
            errors.append(f"{path.relative_to(root)}: artifact escapes kit via symlink")
            continue
        try:
            content = path.read_text(encoding="utf-8")
            if path.suffix == ".md":
                errors.extend(reference_errors(path, content, root))
                if path.name == "SKILL.md":
                    errors.extend(skill_errors(path, content, root))
            elif path.suffix == ".xml":
                ET.fromstring(content)
            elif path.suffix in (".yml", ".yaml"):
                list(yaml.safe_load_all(content))
        except (UnicodeError, OSError) as error:
            errors.append(f"{path.relative_to(root)}: cannot read UTF-8: {error}")
        except ET.ParseError as error:
            errors.append(f"{path.relative_to(root)}: invalid XML: {error}")
        except yaml.YAMLError as error:
            errors.append(f"{path.relative_to(root)}: invalid YAML: {error}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Kit validation passed (references, skill metadata, XML and YAML syntax).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

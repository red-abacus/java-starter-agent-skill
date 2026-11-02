"""Behavioral checks for read-only validation of a portable kit."""

import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate-kit.py"
SPEC = importlib.util.spec_from_file_location("validate_kit", SCRIPT)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ValidateKitTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="portable-kit-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "renamed project"
        self.root.mkdir()
        for relative in VALIDATOR.REQUIRED_FILES:
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.name == "SKILL.md":
                path.write_text(
                    f"---\nname: {path.parent.name}\n"
                    "description: Use when handling this focused Java task.\n---\n"
                    "# Workflow\n\nRead [guidance](../../../docs/java-spring-guidelines.md).\n",
                    encoding="utf-8",
                )
            elif path.suffix == ".xml":
                path.write_text("<configuration/>\n", encoding="utf-8")
            elif path.suffix in (".yaml", ".yml"):
                path.write_text("app:\n  timeout: 5s\n", encoding="utf-8")
            else:
                path.write_text("# Guide\n\nInstructions.\n", encoding="utf-8")

    def errors(self):
        return VALIDATOR.validate(self.root)

    def test_relocated_kit_is_valid(self):
        self.assertEqual([], self.errors())

    def test_cli_is_independent_of_working_directory_and_read_only(self):
        before = self.snapshot()
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root)],
            cwd=self.temp.name,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(before, self.snapshot())

    def test_missing_required_file_is_rejected(self):
        (self.root / "config/checkstyle.xml").unlink()
        self.assertTrue(any("config/checkstyle.xml" in error for error in self.errors()))

    def test_broken_local_reference_is_rejected(self):
        (self.root / "AGENTS.md").write_text("[Missing](docs/missing.md)\n")
        self.assertTrue(any("missing.md" in error for error in self.errors()))

    def test_missing_topic_guide_is_rejected(self):
        path = self.root / "docs/guidelines/rest-api.md"
        path.unlink(missing_ok=True)
        self.assertTrue(any("docs/guidelines/rest-api.md" in error for error in self.errors()))

    def test_links_inside_topic_guides_are_checked(self):
        path = self.root / "docs/guidelines/additional.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("[Missing](missing.md)\n")
        self.assertTrue(any("missing.md" in error for error in self.errors()))

    def test_missing_section_in_existing_file_is_rejected(self):
        (self.root / "AGENTS.md").write_text("[Guide](docs/java-spring-guidelines.md#missing-section)\n")
        self.assertTrue(any("missing section" in error for error in self.errors()))

    def test_missing_section_in_same_file_is_rejected(self):
        (self.root / "AGENTS.md").write_text("# Guide\n\n[Missing](#missing)\n")
        self.assertTrue(any("missing section" in error for error in self.errors()))

    def test_section_links_support_duplicate_headings_and_inline_code(self):
        (self.root / "AGENTS.md").write_text(
            "# Guide\n\n[One](#patch-dtos) [Two](#patch-dtos-1)\n\n"
            "## PATCH `DTOs`\n\nContent.\n\n## PATCH DTOs\n\nMore.\n"
        )
        self.assertEqual([], self.errors())

    def test_malformed_xml_is_rejected(self):
        (self.root / "config/checkstyle.xml").write_text("<module>")
        self.assertTrue(any("XML" in error for error in self.errors()))

    def test_malformed_yaml_is_rejected(self):
        (self.root / "templates/application/application.yml").write_text("key: [unclosed\n")
        self.assertTrue(any("YAML" in error for error in self.errors()))

    def test_invalid_skill_metadata_is_rejected(self):
        path = self.root / ".agents/skills/java-spring-bootstrap/SKILL.md"
        path.write_text("---\nname: unrelated\ndescription: ''\n---\n# Workflow\n")
        errors = self.errors()
        self.assertTrue(any("name" in error for error in errors))
        self.assertTrue(any("description" in error for error in errors))

    def test_reference_cannot_escape_kit(self):
        outside = self.root.parent / "private.md"
        outside.write_text("private\n")
        (self.root / "AGENTS.md").write_text("[Outside](../private.md)\n")
        self.assertTrue(any("escapes" in error for error in self.errors()))

    def test_reference_cannot_escape_via_symlink(self):
        outside = self.root.parent / "private.md"
        outside.write_text("private\n")
        (self.root / "linked.md").symlink_to(outside)
        (self.root / "AGENTS.md").write_text("[Outside](linked.md)\n")
        self.assertTrue(any("escapes" in error for error in self.errors()))

    def test_unrelated_project_documents_are_not_policed(self):
        (self.root / "unrelated.md").write_text("[missing](does-not-exist.md)\n")
        self.assertEqual([], self.errors())

    def test_optional_fixture_links_are_checked_when_fixture_is_present(self):
        guide = self.root / "docs/examples/partial-updates.md"
        guide.write_text("[Probe](../../verification/src/Missing.java)\n")
        self.assertEqual([], self.errors())
        (self.root / "verification").mkdir()
        self.assertTrue(any("Missing.java" in error for error in self.errors()))

    def test_code_fence_examples_are_not_treated_as_links(self):
        (self.root / "AGENTS.md").write_text("```text\n[example](missing.md)\n```\n")
        self.assertEqual([], self.errors())

    def test_runtime_copy_does_not_require_maintenance_files(self):
        copied = self.root.parent / "copy"
        shutil.copytree(self.root, copied)
        self.assertEqual([], VALIDATOR.validate(copied))

    def snapshot(self):
        return {str(path.relative_to(self.root)): path.read_bytes()
                for path in self.root.rglob("*") if path.is_file()}


if __name__ == "__main__":
    unittest.main()

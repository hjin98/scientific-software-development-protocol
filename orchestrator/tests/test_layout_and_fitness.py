"""O1 -- repository containment, namespace shape, and executable architecture fitness.

These are structural claims about the candidate as a whole, so they are checked
against the repository tree and the module ASTs rather than against behaviour.
"""

from __future__ import annotations

import ast
import subprocess
import tomllib
import unittest
from pathlib import Path

from ._support import REPO_ROOT

CORE_SRC = REPO_ROOT / "orchestrator/src/sdp_orchestrator/core"
PYPROJECT = REPO_ROOT / "orchestrator/pyproject.toml"

HIGHER_MODULES = ("sdp_orchestrator.tracker", "sdp_orchestrator.adapters", "sdp_orchestrator.scheduler")

#: Machinery WP-1 explicitly excludes from Core.
FORBIDDEN_IMPORTS = (
    "sqlite3", "httpx", "requests", "filelock", "aiohttp", "sqlalchemy", "asyncio",
)

#: Git subcommands that would mutate a target repository.
MUTATING_GIT = frozenset(
    {"fetch", "pull", "push", "checkout", "switch", "reset", "commit", "merge",
     "rebase", "add", "rm", "clean", "gc", "prune", "update-ref", "stash", "apply",
     "cherry-pick", "restore", "worktree", "clone", "init"}
)


def _tracked_files() -> list[str]:
    result = subprocess.run(  # noqa: S603
        ["git", "-C", str(REPO_ROOT), "ls-files", "--cached", "--others", "--exclude-standard"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.add(node.module)
    return names


def _core_modules() -> list[Path]:
    return sorted(CORE_SRC.rglob("*.py"))


class ContainmentTests(unittest.TestCase):
    def test_legacy_core_tree_and_private_module_paths_are_absent(self) -> None:
        self.assertFalse(
            (REPO_ROOT / "orchestrator" / "packages" / "core").exists(),
            "the retired multi-distribution Core tree must not remain",
        )
        private_modules = [
            path
            for path in CORE_SRC.rglob("*.py")
            if path.name.startswith("_") and path.name != "__init__.py"
        ]
        self.assertEqual(
            private_modules,
            [],
            "implementation modules must use their descriptive public-owner names",
        )

    def test_no_orchestrator_package_exists_outside_the_containment_root(self) -> None:
        stray = [
            path
            for path in _tracked_files()
            if "sdp_orchestrator" in path and not path.startswith("orchestrator/")
        ]
        self.assertEqual(stray, [])

    def test_sibling_repository_trees_do_not_import_orchestrator_code(self) -> None:
        for tree in ("source", "tests", "tools", "scripts"):
            root = REPO_ROOT / tree
            if not root.is_dir():
                continue
            for path in root.rglob("*.py"):
                self.assertNotIn(
                    "sdp_orchestrator",
                    path.read_text(encoding="utf-8"),
                    f"{path} must not host or import orchestrator implementation",
                )

    def test_every_orchestrator_python_file_lives_under_the_containment_root(self) -> None:
        for path in _tracked_files():
            if not path.endswith(".py"):
                continue
            if path.startswith(("orchestrator/", "source/", "tests/")):
                continue
            self.fail(f"unexpected top-level Python file outside the containment boundary: {path}")

    def test_repository_ci_only_invokes_orchestrator_commands(self) -> None:
        """CI may call into ``orchestrator/``; it must not host orchestrator logic."""

        workflow = REPO_ROOT / ".github/workflows/protocol-check.yml"
        text = workflow.read_text(encoding="utf-8")
        self.assertNotIn("import sdp_orchestrator", text)
        self.assertNotIn("def ", text)

    def test_protocol_workplans_remain_under_the_repository_convention(self) -> None:
        self.assertTrue(
            (REPO_ROOT / "workplans/active/PROTOCOL-ORCHESTRATOR-WP1-PROMPT-CORE.md").is_file()
        )


class NamespaceTests(unittest.TestCase):
    def test_no_distribution_owns_the_root_namespace_init(self) -> None:
        root_init = CORE_SRC.parent / "__init__.py"
        self.assertFalse(root_init.exists(), "PEP 420 native namespace must have no __init__.py")

    def test_packaging_declares_native_namespaces(self) -> None:
        config = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
        find = config["tool"]["setuptools"]["packages"]["find"]
        self.assertTrue(find["namespaces"])
        self.assertEqual(find["include"], ["sdp_orchestrator.core*"])

    def test_exactly_one_console_entry_point(self) -> None:
        config = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
        self.assertEqual(list(config["project"]["scripts"]), ["sdp"])

    def test_declared_runtime_dependencies_are_the_justified_set(self) -> None:
        config = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
        names = {
            dep.split(">")[0].split("[")[0].split("=")[0].strip()
            for dep in config["project"]["dependencies"]
        }
        self.assertEqual(
            names, {"platformdirs", "typer", "pydantic", "python-frontmatter", "packaging"}
        )

    def test_clipboard_is_an_optional_extra(self) -> None:
        config = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
        self.assertIn("clipboard", config["project"]["optional-dependencies"])

    def test_runtime_floor_is_python_311(self) -> None:
        config = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
        self.assertEqual(config["project"]["requires-python"], ">=3.11")


class ArchitectureFitnessTests(unittest.TestCase):
    def test_core_imports_no_higher_module(self) -> None:
        for path in _core_modules():
            for name in _imports(path):
                for higher in HIGHER_MODULES:
                    self.assertFalse(
                        name == higher or name.startswith(higher + "."),
                        f"{path.name} imports {name}",
                    )

    def test_core_imports_no_forbidden_machinery(self) -> None:
        for path in _core_modules():
            for name in _imports(path):
                root = name.split(".")[0]
                self.assertNotIn(root, FORBIDDEN_IMPORTS, f"{path.name} imports {name}")

    def test_public_surfaces_import_only_within_core(self) -> None:
        for path in (CORE_SRC / "api/v1.py", CORE_SRC / "spi/v1.py"):
            for name in _imports(path):
                self.assertFalse(
                    name.startswith("sdp_orchestrator.") and ".core" not in name,
                    f"{path.name} imports {name}",
                )

    def test_target_observer_uses_no_mutating_git_subcommand(self) -> None:
        """The single module that touches target repositories stays read-only."""

        tree = ast.parse((CORE_SRC / "git.py").read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                self.assertNotIn(
                    node.value,
                    MUTATING_GIT,
                    f"git.py mentions the mutating subcommand {node.value!r}",
                )

    def test_core_remote_source_reads_do_not_fetch_repository_mirrors(self) -> None:
        """Bounded archive reads avoid materializing an unrelated mirror."""

        offenders = [
            path.name
            for path in _core_modules()
            if '"fetch"' in path.read_text(encoding="utf-8")
        ]
        self.assertEqual(offenders, [])

    def test_core_defines_no_higher_module_command(self) -> None:
        cli = (CORE_SRC / "cli.py").read_text(encoding="utf-8")
        for command in ('"run"', '"status"', '"next"', '"ingest"', '"history"', '"graph"'):
            self.assertNotIn(f"@app.command({command}", cli)

    def test_core_declares_exactly_one_extension_entry_point_group(self) -> None:
        """One group constant, and one place that reads entry points from it."""

        tree = ast.parse((CORE_SRC / "application.py").read_text(encoding="utf-8"))
        assignments = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Assign)
            and isinstance(node.value, ast.Constant)
            and node.value.value == "sdp_orchestrator.extensions.v1"
        ]
        self.assertEqual(len(assignments), 1)
        self.assertEqual(
            [t.id for a in assignments for t in a.targets if isinstance(t, ast.Name)],
            ["ENTRY_POINT_GROUP"],
        )
        lookups = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "entry_points"
        ]
        self.assertEqual(len(lookups), 1, "entry points must be read in exactly one place")
        self.assertEqual(
            [kw.value.id for kw in lookups[0].keywords if isinstance(kw.value, ast.Name)],
            ["ENTRY_POINT_GROUP"],
        )

    def test_core_introduces_no_persistence(self) -> None:
        for path in _core_modules():
            source = path.read_text(encoding="utf-8")
            for token in ("CREATE TABLE", "INSERT INTO", "shelve", "pickle.dump"):
                self.assertNotIn(token, source, f"{path.name}")

    def test_no_higher_module_placeholders_remain(self) -> None:
        """Guard against speculative Adapter/Scheduler scaffolding inside Core."""

        for path in _core_modules():
            source = path.read_text(encoding="utf-8").lower()
            for token in ("class routepolicy", "class benchmark", "class resourceledger",
                          "class quotameter", "def schedule("):
                self.assertNotIn(token, source, f"{path.name}")


if __name__ == "__main__":
    unittest.main()

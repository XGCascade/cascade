"""
Core Contract Enforcement Tests.

These tests enforce architectural boundaries by inspecting
actual import statements, not documentation or comments.
"""

import ast
import inspect

import cascade.core.errors as core_errors
import cascade.core.types as core_types
import cascade.core.registry as core_registry
import cascade.core.coercion as core_coercion


FORBIDDEN_MODULE_PREFIXES = (
    "cascade.rules",
    "cascade.profiles",
    "cascade.dataclass",
    "cascade.jit",
)


def _has_forbidden_imports(module) -> bool:
    """
    Inspect the AST of a module and detect forbidden imports.

    This function only considers actual import statements.
    Docstrings, comments, and string literals are ignored.
    """
    source = inspect.getsource(module)
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith(FORBIDDEN_MODULE_PREFIXES):
                    return True

        if isinstance(node, ast.ImportFrom):
            if node.module and node.module.startswith(FORBIDDEN_MODULE_PREFIXES):
                return True

    return False


def test_core_errors_has_no_upward_dependencies():
    assert not _has_forbidden_imports(core_errors)


def test_core_types_has_no_upward_dependencies():
    assert not _has_forbidden_imports(core_types)


def test_core_registry_has_no_upward_dependencies():
    assert not _has_forbidden_imports(core_registry)


def test_core_coercion_has_no_upward_dependencies():
    assert not _has_forbidden_imports(core_coercion)

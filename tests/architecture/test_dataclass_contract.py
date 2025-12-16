import ast
import inspect

import cascade.dataclass.validated as validated


FORBIDDEN_PREFIXES = (
    "cascade.profiles",
)


def _has_forbidden_imports(module) -> bool:
    source = inspect.getsource(module)
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith(FORBIDDEN_PREFIXES):
                    return True

        if isinstance(node, ast.ImportFrom):
            if node.module and node.module.startswith(FORBIDDEN_PREFIXES):
                return True

    return False


def test_validated_dataclass_has_no_profile_dependency():
    assert not _has_forbidden_imports(validated)

"""
Field helpers for validated dataclasses.

Fields defined here are plain metadata containers.
They do not execute validation by themselves.
"""

from dataclasses import field as dc_field, MISSING
from typing import Any, Iterable, Optional

from cascade.rules.base import Rule


def field(
    *,
    rules: Optional[Iterable[Rule]] = None,
    default: Any = MISSING,
    default_factory: Any = MISSING,
):
    """
    Define a dataclass field with optional validation rules.

    Parameters
    ----------
    rules:
        Optional iterable of Rule instances to be applied explicitly.
    default:
        Default value for the field.
    default_factory:
        Factory for default value.

    Notes
    -----
    This function mirrors `dataclasses.field` behavior.
    It only forwards arguments that are explicitly provided.
    """
    metadata = {}

    if rules is not None:
        metadata["cascade_rules"] = list(rules)

    kwargs = {"metadata": metadata}

    if default is not MISSING:
        kwargs["default"] = default

    if default_factory is not MISSING:
        kwargs["default_factory"] = default_factory

    return dc_field(**kwargs)

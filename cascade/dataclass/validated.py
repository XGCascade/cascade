"""
Validated dataclass decorator for Cascade.

This decorator adds explicit validation methods to a dataclass.
Validation is never automatic unless explicitly requested.
"""

from dataclasses import dataclass, fields
from typing import Any, Callable, Type, TypeVar

from cascade.core.types import validate_type
from cascade.core.errors import ValidationError
from cascade.rules.base import Rule


T = TypeVar("T")


def validated_dataclass(cls: Type[T]) -> Type[T]:
    """
    Decorate a dataclass with explicit validation capabilities.

    The resulting class provides:
    - validate(): validate all fields
    - validate_field(name): validate a single field

    Validation is explicit and must be called by the user.
    """
    cls = dataclass(cls)

    def validate(self) -> None:
        """
        Validate all fields on the dataclass instance.

        Raises ValidationError on first failure.
        """
        for f in fields(self):
            _validate_field(self, f.name)

    def validate_field(self, name: str) -> None:
        """
        Validate a single field by name.

        Raises ValidationError if validation fails.
        """
        if not hasattr(self, name):
            raise AttributeError(f"Field '{name}' does not exist.")

        _validate_field(self, name)

    def is_valid(self) -> bool:
        """
        Check whether the dataclass instance is valid.

        Returns False instead of raising on validation error.
        """
        try:
            self.validate()
            return True
        except ValidationError:
            return False

    cls.validate = validate
    cls.validate_field = validate_field
    cls.is_valid = is_valid

    return cls


def _validate_field(instance: Any, name: str) -> None:
    """
    Internal helper to validate a single field.

    Validation steps:
    1. Type validation
    2. Rule validation (if any)
    """
    value = getattr(instance, name)
    annotation = instance.__annotations__.get(name)

    if annotation is not None:
        validate_type(value, annotation)

    field_info = next(f for f in fields(instance) if f.name == name)
    rules = field_info.metadata.get("cascade_rules", [])

    for rule in rules:
        if not isinstance(rule, Rule):
            raise TypeError("Field rules must be Rule instances.")
        rule(value)

"""
Core type registry for Cascade.

This module provides a passive registry for custom type validators.
It does not perform validation, coercion, or any runtime decision-making.

The registry exists purely as a lookup mechanism used by the core
type checking layer.
"""

from typing import Any, Callable, Dict, Optional, Type


Validator = Callable[[Any], None]


class TypeRegistry:
    """
    Passive registry for custom type validators.

    The registry maps a target type to a validation callable.
    Validators must raise TypeValidationError on failure.
    """

    def __init__(self) -> None:
        self._validators: Dict[Type[Any], Validator] = {}

    def register(self, target_type: Type[Any], validator: Validator) -> None:
        """
        Register a custom validator for a specific type.

        Parameters
        ----------
        target_type:
            The type that this validator applies to.
        validator:
            A callable that receives a value and raises an exception
            if validation fails.

        Notes
        -----
        This method does not perform validation at registration time.
        It simply stores the association.
        """
        if not callable(validator):
            raise TypeError("Validator must be a callable.")

        self._validators[target_type] = validator

    def unregister(self, target_type: Type[Any]) -> None:
        """
        Remove a registered validator for a given type.

        This operation is idempotent. If the type is not registered,
        the method does nothing.
        """
        self._validators.pop(target_type, None)

    def get(self, target_type: Type[Any]) -> Optional[Validator]:
        """
        Retrieve a validator for the given type, if available.
        """
        return self._validators.get(target_type)

    def clear(self) -> None:
        """
        Remove all registered validators.

        This is mainly intended for testing and controlled environments.
        """
        self._validators.clear()


# Global registry instance used by Cascade Core.
_registry = TypeRegistry()


def register_type(target_type: Type[Any], validator: Validator) -> None:
    """
    Register a custom type validator in the global registry.
    """
    _registry.register(target_type, validator)


def unregister_type(target_type: Type[Any]) -> None:
    """
    Unregister a custom type validator from the global registry.
    """
    _registry.unregister(target_type)


def get_registered_validator(target_type: Type[Any]) -> Optional[Validator]:
    """
    Retrieve a registered validator for a given type.

    This function performs no fallback logic and no inheritance resolution.
    """
    return _registry.get(target_type)


def clear_registry() -> None:
    """
    Clear the global registry.

    Intended for test isolation only.
    """
    _registry.clear()

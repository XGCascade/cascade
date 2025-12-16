"""
Public API for Cascade.

This module defines the officially supported public surface of Cascade.
Anything not exported here is considered internal and may change
without notice.

Design goals:
- Small and stable API surface
- Explicit over implicit behavior
- Clear separation between core and higher-level features
"""

# Core validation
from cascade.core.types import validate_type

# Core registry and coercion (explicit utilities)
from cascade.core.registry import (
    register_type,
    unregister_type,
)
from cascade.core.coercion import (
    register_coercer,
    unregister_coercer,
    can_coerce,
    coerce,
)

# Core errors
from cascade.core.errors import (
    CascadeError,
    ValidationError,
    TypeValidationError,
    RuleValidationError,
    CoercionError,
)

# Dataclass utilities (optional sugar)
from cascade.dataclass import (
    validated_dataclass,
    field,
)

__all__ = [
    # Core validation
    "validate_type",

    # Type registry
    "register_type",
    "unregister_type",

    # Coercion utilities
    "register_coercer",
    "unregister_coercer",
    "can_coerce",
    "coerce",

    # Errors
    "CascadeError",
    "ValidationError",
    "TypeValidationError",
    "RuleValidationError",
    "CoercionError",

    # Dataclass sugar
    "validated_dataclass",
    "field",
]

"""
Base rule definitions for Cascade.

A rule is a simple callable object that validates a value
and raises RuleValidationError on failure.
"""

from typing import Any

from cascade.core.errors import RuleValidationError


class Rule:
    """
    Base class for all validation rules.

    Subclasses must implement the `check` method.
    """

    name: str = "rule"

    def __call__(self, value: Any) -> None:
        self.check(value)

    def check(self, value: Any) -> None:
        """
        Validate a value.

        Must raise RuleValidationError on failure.
        """
        raise NotImplementedError("Rule.check must be implemented by subclasses.")

    def fail(self, value: Any, message: str) -> None:
        """
        Helper method to raise a standardized rule validation error.
        """
        raise RuleValidationError(
            value=value,
            rule_name=self.name,
            message=message,
        )

import pytest
from dataclasses import dataclass

from cascade import validated_dataclass, field
from cascade.core.errors import (
    TypeValidationError,
    RuleValidationError,
)


class GreaterThanZero:
    name = "greater_than_zero"

    def __call__(self, value):
        if value <= 0:
            raise RuleValidationError(
                value=value,
                rule_name=self.name,
                message="Value must be greater than zero.",
            )


def test_validated_dataclass_success():
    @validated_dataclass
    class User:
        id: int
        age: int = field(rules=[GreaterThanZero()])

    user = User(id=1, age=10)
    user.validate()


def test_type_validation_applied_first():
    @validated_dataclass
    class User:
        age: int

    user = User(age="not-int")

    with pytest.raises(TypeValidationError):
        user.validate()


def test_rule_validation_applied_after_type():
    @validated_dataclass
    class User:
        age: int = field(rules=[GreaterThanZero()])

    user = User(age=0)

    with pytest.raises(RuleValidationError):
        user.validate()


def test_validate_single_field():
    @validated_dataclass
    class User:
        age: int = field(rules=[GreaterThanZero()])
        name: str

    user = User(age=10, name="Alice")

    user.validate_field("age")
    user.validate_field("name")


def test_validate_field_invalid_name():
    @validated_dataclass
    class User:
        age: int

    user = User(age=10)

    with pytest.raises(AttributeError):
        user.validate_field("missing")


def test_is_valid_returns_false_on_error():
    @validated_dataclass
    class User:
        age: int = field(rules=[GreaterThanZero()])

    user = User(age=0)

    assert user.is_valid() is False


def test_no_validation_on_init():
    @validated_dataclass
    class User:
        age: int = field(rules=[GreaterThanZero()])

    user = User(age=0)
    assert user.age == 0

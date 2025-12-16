import pytest

from cascade import validated_dataclass, field
from cascade.rules import Min
from cascade.core.errors import RuleValidationError, TypeValidationError


def test_validated_dataclass_basic_success():
    @validated_dataclass
    class User:
        id: int
        age: int = field(rules=[Min(18)])

    user = User(id=1, age=20)
    user.validate()  # should not raise


def test_type_validation_applied():
    @validated_dataclass
    class User:
        age: int

    user = User(age="not-int")

    with pytest.raises(TypeValidationError):
        user.validate()


def test_rule_validation_applied_after_type():
    @validated_dataclass
    class User:
        age: int = field(rules=[Min(18)])

    user = User(age=10)

    with pytest.raises(RuleValidationError):
        user.validate()


def test_validate_single_field():
    @validated_dataclass
    class User:
        age: int = field(rules=[Min(18)])
        name: str

    user = User(age=20, name="A")

    user.validate_field("age")   # passes
    user.validate_field("name")  # passes


def test_validate_field_invalid_name():
    @validated_dataclass
    class User:
        age: int

    user = User(age=20)

    with pytest.raises(AttributeError):
        user.validate_field("missing")


def test_is_valid_returns_false_on_error():
    @validated_dataclass
    class User:
        age: int = field(rules=[Min(18)])

    user = User(age=10)

    assert user.is_valid() is False


def test_no_implicit_validation_on_init():
    @validated_dataclass
    class User:
        age: int = field(rules=[Min(18)])

    # This should NOT raise
    user = User(age=10)
    assert user.age == 10

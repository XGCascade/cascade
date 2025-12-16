import pytest
from dataclasses import dataclass

from cascade.dataclass import field
from cascade.rules import Min


def test_field_without_default():
    @dataclass
    class User:
        age: int = field(rules=[Min(18)])

    user = User(age=20)
    assert user.age == 20


def test_field_with_default_value():
    @dataclass
    class User:
        age: int = field(default=18)

    user = User()
    assert user.age == 18


def test_field_with_default_factory():
    @dataclass
    class User:
        tags: list[str] = field(default_factory=list)

    user = User()
    assert user.tags == []


def test_field_rules_stored_in_metadata():
    @dataclass
    class User:
        age: int = field(rules=[Min(18)])

    f = User.__dataclass_fields__["age"]
    assert "cascade_rules" in f.metadata
    assert len(f.metadata["cascade_rules"]) == 1


def test_field_rejects_invalid_rule_type_later():
    @dataclass
    class User:
        age: int = field(rules=["not-a-rule"])  # stored, not executed

    user = User(age=20)
    assert user.age == 20

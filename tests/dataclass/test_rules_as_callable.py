import pytest
from dataclasses import dataclass

from cascade import validated_dataclass, field
from cascade.core.errors import RuleValidationError


def test_lambda_rule_with_name_attribute():
    def positive(value):
        if value <= 0:
            raise RuleValidationError(
                value=value,
                rule_name=positive.name,
                message="Value must be positive.",
            )

    positive.name = "positive"

    @validated_dataclass
    class Item:
        quantity: int = field(rules=[positive])

    item = Item(quantity=1)
    item.validate()

    item.quantity = 0
    with pytest.raises(RuleValidationError):
        item.validate()


def test_invalid_rule_rejected_at_execution_time():
    bad_rule = lambda x: None  # no name attribute

    @validated_dataclass
    class Item:
        value: int = field(rules=[bad_rule])

    item = Item(value=10)

    with pytest.raises(TypeError):
        item.validate()

from cascade.core.errors import (
    CascadeError,
    ValidationError,
    TypeValidationError,
    RuleValidationError,
    CoercionError,
)


def test_error_hierarchy():
    assert issubclass(TypeValidationError, ValidationError)
    assert issubclass(RuleValidationError, ValidationError)
    assert issubclass(CoercionError, CascadeError)


def test_type_validation_error_message():
    err = TypeValidationError(value="x", expected_type=int)
    assert "Expected value of type" in str(err)


def test_rule_validation_error_contains_rule_name():
    err = RuleValidationError(value=10, rule_name="min")
    assert "min" in str(err)
    assert err.rule_name == "min"


def test_coercion_error_is_not_validation_error():
    err = CoercionError(value="1", target_type=int)
    assert not isinstance(err, ValidationError)

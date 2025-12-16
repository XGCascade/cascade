import pytest

from cascade.core.coercion import (
    register_coercer,
    unregister_coercer,
    coerce,
    can_coerce,
    clear_coercers,
)
from cascade.core.errors import CoercionError


def setup_function():
    clear_coercers()


def test_can_coerce_false_when_not_registered():
    assert can_coerce("123", int) is False


def test_successful_coercion():
    register_coercer(int, int)

    result = coerce("123", int)
    assert result == 123
    assert isinstance(result, int)


def test_coercion_without_coercer_raises():
    with pytest.raises(CoercionError):
        coerce("123", int)


def test_coercer_must_return_target_type():
    def bad_coercer(value):
        return "not-int"

    register_coercer(int, bad_coercer)

    with pytest.raises(CoercionError):
        coerce("123", int)


def test_unregister_coercer():
    register_coercer(int, int)
    unregister_coercer(int)

    assert can_coerce("123", int) is False

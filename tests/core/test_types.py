import pytest
from typing import Optional, List, Dict

from cascade.core.types import validate_type
from cascade.core.errors import TypeValidationError
from cascade.core.registry import register_type, clear_registry


def setup_function():
    clear_registry()


def test_builtin_type_success():
    assert validate_type(10, int) is True


def test_builtin_type_failure():
    with pytest.raises(TypeValidationError):
        validate_type("10", int)


def test_any_type_always_passes():
    assert validate_type("anything", object) is True


def test_optional_type():
    assert validate_type(None, Optional[int]) is True
    assert validate_type(5, Optional[int]) is True

    with pytest.raises(TypeValidationError):
        validate_type("x", Optional[int])


def test_list_generic():
    assert validate_type([1, 2, 3], List[int]) is True

    with pytest.raises(TypeValidationError):
        validate_type([1, "x"], List[int])


def test_dict_generic():
    assert validate_type({"a": 1}, Dict[str, int]) is True

    with pytest.raises(TypeValidationError):
        validate_type({"a": "x"}, Dict[str, int])


def test_custom_registered_type():
    class UserId(int):
        pass

    def validate_user_id(value):
        if not isinstance(value, UserId):
            raise TypeValidationError(value=value, expected_type=UserId)

    register_type(UserId, validate_user_id)

    assert validate_type(UserId(1), UserId) is True

    with pytest.raises(TypeValidationError):
        validate_type(1, UserId)

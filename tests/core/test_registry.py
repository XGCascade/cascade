from cascade.core.registry import (
    register_type,
    unregister_type,
    get_registered_validator,
    clear_registry,
)


def setup_function():
    clear_registry()


def test_register_and_get_validator():
    def validator(value):
        pass

    register_type(int, validator)
    assert get_registered_validator(int) is validator


def test_unregister_validator():
    def validator(value):
        pass

    register_type(int, validator)
    unregister_type(int)

    assert get_registered_validator(int) is None


def test_registry_is_global():
    def validator(value):
        pass

    register_type(str, validator)
    assert get_registered_validator(str) is validator

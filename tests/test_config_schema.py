import importlib


def test_config_schema_defined_and_accepts_empty_config() -> None:
    module = importlib.import_module("custom_components.willoughby_services")

    assert hasattr(module, "CONFIG_SCHEMA")

    config_schema = module.CONFIG_SCHEMA

    validated = config_schema({})
    assert isinstance(validated, dict)

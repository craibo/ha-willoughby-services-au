from __future__ import annotations


def config_entry_only_config_schema(domain: str):
    def _validate(config):
        return config

    return _validate

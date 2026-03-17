from __future__ import annotations

from enum import Enum
from typing import Any, Dict


class FlowResultType(str, Enum):
    CREATE_ENTRY = "create_entry"
    FORM = "form"


class ConfigEntry:
    def __init__(self, data: Dict[str, Any] | None = None) -> None:
        self.data = data or {}
        self.entry_id = "test-entry-id"


class ConfigFlow:
    def __init_subclass__(cls, **kwargs):
        return super().__init_subclass__()

    async def async_set_unique_id(self, unique_id: str) -> None:
        self._unique_id = unique_id

    def _abort_if_unique_id_configured(self) -> None:
        return

    def async_create_entry(self, *, title: str, data: Dict[str, Any]):
        return {
            "type": FlowResultType.CREATE_ENTRY,
            "title": title,
            "data": data,
        }

    def async_show_form(self, *, step_id: str, data_schema=None, errors=None, description_placeholders=None):
        return {
            "type": FlowResultType.FORM,
            "step_id": step_id,
            "errors": errors or {},
            "description_placeholders": description_placeholders or {},
        }


class OptionsFlow:
    def async_create_entry(self, *, title: str, data: Dict[str, Any]):
        return {
            "type": FlowResultType.CREATE_ENTRY,
            "title": title,
            "data": data,
        }

    def async_show_form(self, *, step_id: str, data_schema=None, errors=None, description_placeholders=None):
        return {
            "type": FlowResultType.FORM,
            "step_id": step_id,
            "errors": errors or {},
            "description_placeholders": description_placeholders or {},
        }


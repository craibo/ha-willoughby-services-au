from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN, CONF_ADDRESS, CONF_GEOLOCATION_ID


class WilloughbyServicesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        errors: dict[str, str] = {}

        if user_input is not None:
            address = user_input.get(CONF_ADDRESS, "").strip()
            geolocation_id = user_input.get(CONF_GEOLOCATION_ID, "").strip()

            if not address and not geolocation_id:
                errors["base"] = "address_or_geolocation_required"
            else:
                await self.async_set_unique_id(f"{geolocation_id or address}")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=address or geolocation_id,
                    data={
                        CONF_ADDRESS: address or None,
                        CONF_GEOLOCATION_ID: geolocation_id or None,
                    },
                )

        data_schema = vol.Schema(
            {
                vol.Optional(CONF_ADDRESS): str,
                vol.Optional(CONF_GEOLOCATION_ID): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return WilloughbyServicesOptionsFlow(config_entry)


class WilloughbyServicesOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_ADDRESS,
                    default=self._entry.data.get(CONF_ADDRESS, ""),
                ): str,
                vol.Optional(
                    CONF_GEOLOCATION_ID,
                    default=self._entry.data.get(CONF_GEOLOCATION_ID, ""),
                ): str,
            }
        )

        return self.async_show_form(step_id="init", data_schema=data_schema)


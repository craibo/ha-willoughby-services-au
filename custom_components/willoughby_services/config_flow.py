from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .address_search import AddressSearchResult, WilloughbyAddressSearchError, async_search_addresses
from .const import CONF_ADDRESS, CONF_GEOLOCATION_ID, DOMAIN


class WilloughbyServicesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self) -> None:
        self._search_results: list[AddressSearchResult] = []
        self._pending_address: str | None = None

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        errors: dict[str, str] = {}

        if user_input is not None:
            address = user_input.get(CONF_ADDRESS, "").strip()
            geolocation_id = user_input.get(CONF_GEOLOCATION_ID, "").strip()

            if not address and not geolocation_id:
                errors["base"] = "address_or_geolocation_required"
            elif geolocation_id:
                await self.async_set_unique_id(f"{geolocation_id or address}")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=address or geolocation_id,
                    data={
                        CONF_ADDRESS: address or None,
                        CONF_GEOLOCATION_ID: geolocation_id or None,
                    },
                )
            else:
                session = async_get_clientsession(self.hass)
                try:
                    results = await async_search_addresses(session, address)
                except WilloughbyAddressSearchError:
                    errors["base"] = "address_search_failed"
                else:
                    if not results:
                        errors["base"] = "address_not_found"
                    elif len(results) == 1:
                        result = results[0]
                        await self.async_set_unique_id(result.geolocation_id)
                        self._abort_if_unique_id_configured()
                        return self.async_create_entry(
                            title=result.address,
                            data={
                                CONF_ADDRESS: result.address,
                                CONF_GEOLOCATION_ID: result.geolocation_id,
                            },
                        )
                    else:
                        self._search_results = results
                        self._pending_address = address
                        return await self.async_step_select_address()

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

    async def async_step_select_address(
        self, user_input: dict[str, Any] | None = None
    ):
        errors: dict[str, str] = {}

        if not self._search_results:
            return await self.async_step_user({})

        if user_input is not None:
            try:
                index = int(user_input["selection"])
                result = self._search_results[index]
            except (KeyError, ValueError, IndexError):
                errors["base"] = "invalid_selection"
            else:
                await self.async_set_unique_id(result.geolocation_id)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=result.address,
                    data={
                        CONF_ADDRESS: result.address,
                        CONF_GEOLOCATION_ID: result.geolocation_id,
                    },
                )

        options = {
            str(idx): res.address for idx, res in enumerate(self._search_results)
        }

        data_schema = vol.Schema(
            {
                vol.Required("selection"): vol.In(options),
            }
        )

        return self.async_show_form(
            step_id="select_address",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={"query": self._pending_address or ""},
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return WilloughbyServicesOptionsFlow(config_entry)


class WilloughbyServicesOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._entry = config_entry
        self._search_results: list[AddressSearchResult] = []
        self._pending_address: str | None = None

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            address = user_input.get(CONF_ADDRESS, "").strip()
            geolocation_id = user_input.get(CONF_GEOLOCATION_ID, "").strip()

            if geolocation_id:
                return self.async_create_entry(
                    title="",
                    data={
                        CONF_ADDRESS: address,
                        CONF_GEOLOCATION_ID: geolocation_id,
                    },
                )

            if address:
                session = async_get_clientsession(self.hass)
                try:
                    results = await async_search_addresses(session, address)
                except WilloughbyAddressSearchError:
                    return self.async_show_form(
                        step_id="init",
                        data_schema=self._build_init_schema(user_input),
                        errors={"base": "address_search_failed"},
                    )

                if not results:
                    return self.async_show_form(
                        step_id="init",
                        data_schema=self._build_init_schema(user_input),
                        errors={"base": "address_not_found"},
                    )

                if len(results) == 1:
                    result = results[0]
                    return self.async_create_entry(
                        title="",
                        data={
                            CONF_ADDRESS: result.address,
                            CONF_GEOLOCATION_ID: result.geolocation_id,
                        },
                    )

                self._search_results = results
                self._pending_address = address
                return await self.async_step_select_address()

            return self.async_create_entry(
                title="",
                data={
                    CONF_ADDRESS: address,
                    CONF_GEOLOCATION_ID: None,
                },
            )

        return self.async_show_form(
            step_id="init", data_schema=self._build_init_schema()
        )

    async def async_step_select_address(
        self, user_input: dict[str, Any] | None = None
    ):
        errors: dict[str, str] = {}

        if not self._search_results:
            return await self.async_step_init({})

        if user_input is not None:
            try:
                index = int(user_input["selection"])
                result = self._search_results[index]
            except (KeyError, ValueError, IndexError):
                errors["base"] = "invalid_selection"
            else:
                return self.async_create_entry(
                    title="",
                    data={
                        CONF_ADDRESS: result.address,
                        CONF_GEOLOCATION_ID: result.geolocation_id,
                    },
                )

        options = {
            str(idx): res.address for idx, res in enumerate(self._search_results)
        }

        data_schema = vol.Schema(
            {
                vol.Required("selection"): vol.In(options),
            }
        )

        return self.async_show_form(
            step_id="select_address",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={"query": self._pending_address or ""},
        )

    def _build_init_schema(
        self, current: dict[str, Any] | None = None
    ) -> vol.Schema:
        data = current or self._entry.data
        return vol.Schema(
            {
                vol.Optional(
                    CONF_ADDRESS,
                    default=data.get(CONF_ADDRESS, ""),
                ): str,
                vol.Optional(
                    CONF_GEOLOCATION_ID,
                    default=data.get(CONF_GEOLOCATION_ID, ""),
                ): str,
            }
        )


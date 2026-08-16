from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    PLATFORMS,
    CONF_GEOLOCATION_ID,
    CONF_ADDRESS,
)
from .waste_client import WilloughbyWasteClient, WilloughbyWasteError

_LOGGER = logging.getLogger(__name__)


WilloughbyConfigEntry = ConfigEntry


CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    return True


async def async_setup_entry(hass: HomeAssistant, entry: WilloughbyConfigEntry) -> bool:
    session = async_get_clientsession(hass)

    client = WilloughbyWasteClient(
        session=session,
        geolocation_id=entry.options.get(CONF_GEOLOCATION_ID) or entry.data.get(CONF_GEOLOCATION_ID),
        address=entry.options.get(CONF_ADDRESS) or entry.data.get(CONF_ADDRESS),
    )

    async def async_update() -> dict:
        try:
            return await client.async_get_services()
        except WilloughbyWasteError as err:
            raise UpdateFailed(str(err)) from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update,
        update_interval=timedelta(days=1),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "client": client,
    }

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def _async_update_listener(hass: HomeAssistant, entry: WilloughbyConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: WilloughbyConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok and DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


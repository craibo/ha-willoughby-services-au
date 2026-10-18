from __future__ import annotations

import asyncio
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


INITIAL_REFRESH_RETRY_DELAYS = (60, 300, 900)

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

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "client": client,
    }

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_create_background_task(
        hass,
        _async_initial_refresh(coordinator),
        name=f"{DOMAIN}_initial_refresh_{entry.entry_id}",
    )
    return True


async def _async_initial_refresh(coordinator: DataUpdateCoordinator) -> None:
    """Fetch the first data set without blocking Home Assistant startup.

    The coordinator only polls daily, so retry a few times on failure rather
    than leaving sensors unavailable until the next scheduled refresh.
    """
    await coordinator.async_refresh()
    for delay in INITIAL_REFRESH_RETRY_DELAYS:
        if coordinator.last_update_success:
            return
        await asyncio.sleep(delay)
        await coordinator.async_refresh()


async def _async_update_listener(hass: HomeAssistant, entry: WilloughbyConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: WilloughbyConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok and DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


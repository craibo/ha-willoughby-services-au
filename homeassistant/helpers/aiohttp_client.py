from __future__ import annotations

from aiohttp import ClientSession


def async_get_clientsession(_hass) -> ClientSession:
    return ClientSession()


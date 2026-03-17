from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Awaitable, Callable


class UpdateFailed(Exception):
    pass


@dataclass
class DataUpdateCoordinator:
    hass: Any
    logger: Any
    name: str
    update_method: Callable[[], Awaitable[Any]]
    update_interval: timedelta

    async def async_config_entry_first_refresh(self) -> None:
        await self.update_method()


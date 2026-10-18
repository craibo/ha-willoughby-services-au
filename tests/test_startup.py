from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock

import pytest

from custom_components.willoughby_services import _async_initial_refresh
from custom_components.willoughby_services.sensor import WilloughbyWasteSensor


class DummyCoordinator:
    def __init__(self, data=None) -> None:
        self.config_entry = type("ConfigEntry", (), {"title": "Test Address"})()
        self.data = data


def test_sensor_value_is_none_before_first_refresh() -> None:
    sensor = WilloughbyWasteSensor(
        coordinator=DummyCoordinator(data=None),
        entry_id="entry-id",
        name="Test Address",
        sensor_key="next_red_bin_collection",
    )
    assert sensor.native_value is None


@pytest.mark.asyncio
async def test_initial_refresh_stops_after_success(monkeypatch) -> None:
    monkeypatch.setattr(asyncio, "sleep", AsyncMock())
    coordinator = type("C", (), {})()
    coordinator.last_update_success = True
    coordinator.async_refresh = AsyncMock()

    await _async_initial_refresh(coordinator)

    assert coordinator.async_refresh.await_count == 1


@pytest.mark.asyncio
async def test_initial_refresh_retries_on_failure(monkeypatch) -> None:
    monkeypatch.setattr(asyncio, "sleep", AsyncMock())
    coordinator = type("C", (), {})()
    coordinator.last_update_success = False
    coordinator.async_refresh = AsyncMock()

    await _async_initial_refresh(coordinator)

    assert coordinator.async_refresh.await_count == 4

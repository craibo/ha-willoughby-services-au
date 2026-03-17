from __future__ import annotations

from custom_components.willoughby_services.sensor import (
    SENSOR_ICONS,
    WilloughbyWasteSensor,
)


class DummyCoordinator:
    def __init__(self) -> None:
        self.config_entry = type("ConfigEntry", (), {"title": "Test Address"})()
        self.data = {}


def test_sensor_icons_mapping_complete() -> None:
    expected = {
        "next_red_bin_collection": "mdi:trash-can",
        "next_yellow_bin_collection": "mdi:trash-can",
        "next_green_bin_collection": "mdi:trash-can",
        "next_street_sweep_date": "mdi:broom",
        "next_autumn_bulky_collection": "mdi:dump-truck",
        "next_winter_bulky_collection": "mdi:dump-truck",
        "next_summer_bulky_collection": "mdi:dump-truck",
    }

    assert SENSOR_ICONS == expected


def test_sensor_uses_expected_icon() -> None:
    coordinator = DummyCoordinator()
    for key, icon in SENSOR_ICONS.items():
        sensor = WilloughbyWasteSensor(
            coordinator=coordinator,
            entry_id="entry-id",
            name="Test Address",
            sensor_key=key,
        )
        assert sensor.icon == icon


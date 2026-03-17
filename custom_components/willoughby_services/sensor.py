from __future__ import annotations

from datetime import datetime

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from homeassistant.util import dt as dt_util

from .const import DOMAIN, SENSOR_KEYS


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    entities: list[WilloughbyWasteSensor] = []
    for key in SENSOR_KEYS.values():
        entities.append(
            WilloughbyWasteSensor(
                coordinator=coordinator,
                entry_id=entry.entry_id,
                name=entry.title,
                sensor_key=key,
            )
        )

    async_add_entities(entities)


class WilloughbyWasteSensor(CoordinatorEntity, SensorEntity):
    _attr_device_class = "timestamp"

    def __init__(self, coordinator, entry_id: str, name: str, sensor_key: str) -> None:
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._sensor_key = sensor_key
        self._attr_unique_id = f"{entry_id}_{sensor_key}"
        self._attr_name = f"{name} {self._friendly_name_suffix(sensor_key)}"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry_id)},
            manufacturer="Willoughby City Council",
            name=self.coordinator.config_entry.title,
        )

    @property
    def native_value(self) -> datetime | None:
        value = self.coordinator.data.get(self._sensor_key)
        if isinstance(value, datetime):
            if value.tzinfo is not None:
                return value
            return value.replace(tzinfo=dt_util.DEFAULT_TIME_ZONE)
        return None

    def _friendly_name_suffix(self, sensor_key: str) -> str:
        if sensor_key.endswith("next_red_bin_collection"):
            return "Red Bin"
        if sensor_key.endswith("next_yellow_bin_collection"):
            return "Yellow Bin"
        if sensor_key.endswith("next_green_bin_collection"):
            return "Green Bin"
        if sensor_key.endswith("next_street_sweep_date"):
            return "Street Sweep"
        if sensor_key.endswith("next_autumn_bulky_collection"):
            return "Autumn Bulky Waste"
        if sensor_key.endswith("next_winter_bulky_collection"):
            return "Winter Bulky Waste"
        if sensor_key.endswith("next_summer_bulky_collection"):
            return "Summer Bulky Waste"
        return sensor_key


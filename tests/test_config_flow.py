from typing import Any

from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from custom_components.willoughby_services.const import CONF_ADDRESS, CONF_GEOLOCATION_ID
from custom_components.willoughby_services.config_flow import (
    WilloughbyServicesConfigFlow,
)


class _MockResult:
    def __init__(self, address: str, geolocation_id: str) -> None:
        self.address = address
        self.geolocation_id = geolocation_id


async def _init_flow(hass=None) -> WilloughbyServicesConfigFlow:
    flow = WilloughbyServicesConfigFlow()
    flow.hass = hass
    return flow


import pytest


@pytest.mark.asyncio
async def test_config_flow_single_match(monkeypatch: Any) -> None:
    async def _fake_search(_session, _keywords: str):
        return [
            _MockResult(
                address="2 Sunnyside Crescent, Castlecrag NSW 2068",
                geolocation_id="40e960ef-85bb-4c1f-9f69-a191bf7075f7",
            )
        ]

    monkeypatch.setattr(
        "custom_components.willoughby_services.config_flow.async_search_addresses",
        _fake_search,
    )

    flow = await _init_flow()

    result = await flow.async_step_user(
        {CONF_ADDRESS: "2 Sunnyside Crescent, Castlecrag"}
    )

    assert result["type"] == config_entries.FlowResultType.CREATE_ENTRY
    assert result["title"] == "2 Sunnyside Crescent, Castlecrag NSW 2068"
    assert result["data"][CONF_GEOLOCATION_ID] == "40e960ef-85bb-4c1f-9f69-a191bf7075f7"


@pytest.mark.asyncio
async def test_config_flow_multiple_matches(monkeypatch: Any) -> None:
    async def _fake_search(_session, _keywords: str):
        return [
            _MockResult(
                address="2 Sunnyside Crescent, Castlecrag NSW 2068",
                geolocation_id="40e960ef-85bb-4c1f-9f69-a191bf7075f7",
            ),
            _MockResult(
                address="26 Sunnyside Crescent, Castlecrag NSW 2068",
                geolocation_id="7c55cb94-955e-41d2-b930-7f7eb19ddb0f",
            ),
        ]

    monkeypatch.setattr(
        "custom_components.willoughby_services.config_flow.async_search_addresses",
        _fake_search,
    )

    flow = await _init_flow()

    result = await flow.async_step_user({CONF_ADDRESS: "Sunnyside Crescent"})
    assert result["type"] == config_entries.FlowResultType.FORM
    assert result["step_id"] == "select_address"

    result2 = await flow.async_step_select_address({"selection": "1"})
    assert result2["type"] == config_entries.FlowResultType.CREATE_ENTRY
    assert (
        result2["data"][CONF_GEOLOCATION_ID]
        == "7c55cb94-955e-41d2-b930-7f7eb19ddb0f"
    )


@pytest.mark.asyncio
async def test_config_flow_no_matches(monkeypatch: Any) -> None:
    async def _fake_search(_session, _keywords: str):
        return []

    monkeypatch.setattr(
        "custom_components.willoughby_services.config_flow.async_search_addresses",
        _fake_search,
    )

    flow = await _init_flow()

    result = await flow.async_step_user({CONF_ADDRESS: "Unknown Street"})
    assert result["type"] == config_entries.FlowResultType.FORM
    assert result["errors"]["base"] == "address_not_found"


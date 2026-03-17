from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest
from aiohttp import ClientSession

from custom_components.willoughby_services.waste_client import (
    WilloughbyWasteClient,
)


@pytest.mark.asyncio
async def test_waste_client_parses_all_expected_dates(aiohttp_client, aiohttp_unused_port):
    fixture_path = Path(__file__).parent / "fixtures_wasteservices_sample.json"
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))

    async def handler(request):
        return aiohttp.web.json_response(payload)

    from aiohttp import web

    app = web.Application()
    app.router.add_get("/ocapi/Public/myarea/wasteservices", handler)
    port = aiohttp_unused_port()
    server = await aiohttp_client(app, server_kwargs={"port": port})

    session: ClientSession = server.session

    client = WilloughbyWasteClient(
        session=session,
        geolocation_id="dummy-id",
        address=None,
    )
    # Override base URL to point to test server
    client._session = session  # type: ignore[attr-defined]

    results = await client.async_get_services()

    assert results["next_red_bin_collection"] == datetime(2026, 3, 23)
    assert results["next_yellow_bin_collection"] == datetime(2026, 3, 23)
    assert results["next_green_bin_collection"] == datetime(2026, 3, 23)
    assert results["next_autumn_bulky_collection"] == datetime(2025, 7, 20)
    assert results["next_summer_bulky_collection"] == datetime(2025, 11, 9)
    assert results["next_winter_bulky_collection"] == datetime(2026, 3, 15)
    assert results["next_street_sweep_date"] == datetime(2026, 3, 17)


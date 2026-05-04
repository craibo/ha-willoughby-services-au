# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run all tests
pytest tests/ -v

# Run a single test file
pytest tests/test_waste_client.py -v

# Run a specific test
pytest tests/test_config_flow.py::test_single_address_match -v
```

## Architecture

This is a Home Assistant custom integration for Willoughby City Council (NSW, Australia) waste collection services. Domain: `willoughby_services`.

### Integration flow

1. **Config entry setup** (`__init__.py`): Creates a `WilloughbyWasteClient` and a `DataUpdateCoordinator` (1-day poll interval). Both are stored in `hass.data[DOMAIN][entry.entry_id]`. All platforms are forwarded to `sensor`.

2. **Config flow** (`config_flow.py`): Two-step — user provides an address string or a raw `geolocationid`. If an address is given, `WilloughbyAddressSearchClient` resolves it to a geolocation ID via the council search API. If multiple results come back, a second step (`async_step_select_address`) lets the user pick. Unique ID is set from the resolved geolocation ID.

3. **API clients**:
   - `waste_client.py` — `WilloughbyWasteClient` fetches from the council's `wasteservices` endpoint. The response is HTML; it uses Python's `html.parser` (`HTMLParser`) to extract service dates by matching heading text keywords. Raises `WilloughbyWasteError` on failures.
   - `address_search.py` — `WilloughbyAddressSearchClient` calls the council's XML search API and manually parses the XML line-by-line. Returns a list of `AddressSearchResult` dataclasses. Raises `WilloughbyAddressSearchError` on failures.

4. **Sensors** (`sensor.py`): `WilloughbyWasteSensor` extends both `CoordinatorEntity` and `SensorEntity`. Device class is `timestamp`. Seven sensor keys are defined in `const.py` (red/yellow/green bins, street sweep, autumn/winter/summer bulk waste) with icons. All sensors for an entry share a single HA device.

### Key constants (`const.py`)

- `DOMAIN`, API endpoint URLs, sensor key definitions, icon map
- `CONF_ADDRESS`, `CONF_GEOLOCATION_ID` — config entry keys

### Parsing notes

HTML parsing in `waste_client.py` is keyword-based: headings are matched against known strings (e.g. "general waste", "recycling") to map them to sensor keys. Date parsing tries `%a %d/%m/%Y` then `%d/%m/%Y`. The XML parsing in `address_search.py` is manual (no lxml dependency).

### Tests

Tests use `pytest` with `pytest-asyncio`. API responses are mocked with `aiohttp_client` fixture and patched URLs. Fixtures (HTML/JSON/XML samples) live in `tests/`. Each file covers one module: waste client, address search, config flow, sensor icons.

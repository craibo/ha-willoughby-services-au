from custom_components.willoughby_services.address_search import (
    AddressSearchResult,
    _parse_search_response,
)


SAMPLE_JSON = {
    "Items": [
        {
            "Id": "40e960ef-85bb-4c1f-9f69-a191bf7075f7",
            "AddressSingleLine": "2 Sunnyside Crescent, Castlecrag NSW 2068",
            "MunicipalSubdivision": "Sailors Bay Ward",
            "Distance": 0,
            "Score": 7.6197715,
            "LatLon": None,
        },
        {
            "Id": "7c55cb94-955e-41d2-b930-7f7eb19ddb0f",
            "AddressSingleLine": "26 Sunnyside Crescent, Castlecrag NSW 2068",
            "MunicipalSubdivision": "Sailors Bay Ward",
            "Distance": 0,
            "Score": 7.1,
            "LatLon": None,
        },
    ],
    "Offset": 0,
    "Limit": 10,
    "Total": 2,
}


def test_parse_search_response_extracts_addresses_and_ids():
    results = _parse_search_response(SAMPLE_JSON)

    assert len(results) == 2

    first = results[0]
    assert isinstance(first, AddressSearchResult)
    assert first.address == "2 Sunnyside Crescent, Castlecrag NSW 2068"
    assert first.geolocation_id == "40e960ef-85bb-4c1f-9f69-a191bf7075f7"

    second = results[1]
    assert second.address == "26 Sunnyside Crescent, Castlecrag NSW 2068"
    assert second.geolocation_id == "7c55cb94-955e-41d2-b930-7f7eb19ddb0f"


def test_parse_search_response_handles_empty():
    results = _parse_search_response({"Items": [], "Offset": 0, "Limit": 10, "Total": 0})
    assert results == []


def test_parse_search_response_handles_missing_items():
    results = _parse_search_response({})
    assert results == []

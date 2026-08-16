from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from aiohttp import ClientError, ClientSession


SEARCH_API_URL = "https://www.willoughby.nsw.gov.au/api/v1/myarea/search"


class WilloughbyAddressSearchError(Exception):
    pass


@dataclass
class AddressSearchResult:
    address: str
    geolocation_id: str


async def async_search_addresses(
    session: ClientSession, keywords: str
) -> list[AddressSearchResult]:
    params = {"keywords": keywords}

    try:
        async with session.get(SEARCH_API_URL, params=params) as resp:
            resp.raise_for_status()
            data: Any = await resp.json(content_type=None)
    except ClientError as err:
        raise WilloughbyAddressSearchError(
            f"Error searching addresses: {err}"
        ) from err

    return _parse_search_response(data)


def _parse_search_response(data: Any) -> list[AddressSearchResult]:
    if not isinstance(data, dict):
        return []

    items = data.get("Items")
    if not isinstance(items, list):
        return []

    results: list[AddressSearchResult] = []

    for item in items:
        if not isinstance(item, dict):
            continue

        address = item.get("AddressSingleLine")
        geolocation_id = item.get("Id")

        if address and geolocation_id:
            results.append(
                AddressSearchResult(
                    address=address,
                    geolocation_id=geolocation_id,
                )
            )

    return results


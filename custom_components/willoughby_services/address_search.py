from __future__ import annotations

from dataclasses import dataclass

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
            text = await resp.text()
    except ClientError as err:
        raise WilloughbyAddressSearchError(
            f"Error searching addresses: {err}"
        ) from err

    return _parse_search_response(text)


def _parse_search_response(raw_xml: str) -> list[AddressSearchResult]:
    results: list[AddressSearchResult] = []

    in_result = False
    current_address: str | None = None
    current_id: str | None = None

    for line in raw_xml.splitlines():
        line = line.strip()
        if not line:
            continue

        if "<d2p1:PhysicalAddressSearchResult" in line:
            in_result = True
            current_address = None
            current_id = None
            continue

        if in_result and "</d2p1:PhysicalAddressSearchResult>" in line:
            if current_address and current_id:
                results.append(
                    AddressSearchResult(
                        address=current_address,
                        geolocation_id=current_id,
                    )
                )
            in_result = False
            current_address = None
            current_id = None
            continue

        if in_result and "<d2p1:AddressSingleLine>" in line:
            start = line.find(">") + 1
            end = line.rfind("<")
            current_address = line[start:end].strip()
            continue

        if in_result and "<d2p1:Id>" in line:
            start = line.find(">") + 1
            end = line.rfind("<")
            current_id = line[start:end].strip()
            continue

    return results


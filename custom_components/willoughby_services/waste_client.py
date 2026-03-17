from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from html.parser import HTMLParser
from typing import Any

from aiohttp import ClientSession, ClientError
from homeassistant.util import dt as dt_util

from .const import API_BASE_URL, API_LANG, API_PAGE_LINK, SENSOR_KEYS


class WilloughbyWasteError(Exception):
    pass


@dataclass
class _Tile:
    heading: str | None = None
    next_service_raw: str | None = None


class _WasteHtmlParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tiles: list[_Tile] = []
        self._in_heading = False
        self._in_next_service = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag == "h3":
            self.tiles.append(_Tile())
            self._in_heading = True
        elif tag == "div" and "class" in attrs_dict and "next-service" in (attrs_dict["class"] or ""):
            self._in_next_service = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "h3":
            self._in_heading = False
        elif tag == "div" and self._in_next_service:
            self._in_next_service = False

    def handle_data(self, data: str) -> None:
        if not self.tiles:
            return
        current = self.tiles[-1]
        text = data.strip()
        if not text:
            return
        if self._in_heading:
            current.heading = (current.heading or "") + text
        elif self._in_next_service:
            current.next_service_raw = (current.next_service_raw or "") + text


class WilloughbyWasteClient:
    def __init__(self, session: ClientSession, geolocation_id: str | None, address: str | None) -> None:
        if not geolocation_id and not address:
            raise WilloughbyWasteError("Either geolocation ID or address must be provided")
        self._session = session
        self._geolocation_id = geolocation_id
        self._address = address

    async def async_get_services(self) -> dict[str, datetime | None]:
        if not self._geolocation_id:
            raise WilloughbyWasteError("Geolocation ID resolution from address is not implemented")

        params = {
            "geolocationid": self._geolocation_id,
            "ocsvclang": API_LANG,
            "pageLink": API_PAGE_LINK,
        }

        try:
            async with self._session.get(API_BASE_URL, params=params) as resp:
                resp.raise_for_status()
                data: Any = await resp.json()
        except ClientError as err:
            raise WilloughbyWasteError(f"Error fetching waste services: {err}") from err

        content = data.get("responseContent")
        if not isinstance(content, str):
            raise WilloughbyWasteError("Unexpected response structure from waste services API")

        parser = _WasteHtmlParser()
        parser.feed(content)

        results: dict[str, datetime | None] = {key: None for key in SENSOR_KEYS.values()}

        for tile in parser.tiles:
            if not tile.heading or not tile.next_service_raw:
                continue

            key = self._map_heading_to_key(tile.heading)
            if not key:
                continue

            parsed_date = self._parse_date(tile.next_service_raw)
            if parsed_date is None:
                continue

            results[key] = parsed_date

        return results

    def _map_heading_to_key(self, heading: str) -> str | None:
        title = heading.lower()

        if "red-lidded garbage" in title or "red-lidded" in title:
            return SENSOR_KEYS["red_bin"]
        if "yellow-lidded recycling" in title or "yellow-lidded" in title:
            return SENSOR_KEYS["yellow_bin"]
        if "green-lidded vegetation" in title or "green-lidded" in title:
            return SENSOR_KEYS["green_bin"]
        if "street sweeping" in title:
            return SENSOR_KEYS["street_sweep"]
        if "mid-winter to spring" in title:
            return SENSOR_KEYS["autumn_bulky"]
        if "late summer to early winter" in title:
            return SENSOR_KEYS["winter_bulky"]
        if "spring" in title and "summer" in title:
            return SENSOR_KEYS["summer_bulky"]

        return None

    def _parse_date(self, raw: str) -> datetime | None:
        text = " ".join(raw.split())

        for fmt in ("%a %d/%m/%Y", "%d/%m/%Y"):
            try:
                parsed = datetime.strptime(text, fmt)
                return parsed.replace(tzinfo=dt_util.DEFAULT_TIME_ZONE)
            except ValueError:
                continue

        return None


from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Set, Tuple


@dataclass
class DeviceInfo:
    identifiers: Set[Tuple[str, str]]
    manufacturer: str | None = None
    name: str | None = None


class CoordinatorEntity:
    def __init__(self, coordinator: Any) -> None:
        self.coordinator = coordinator


from __future__ import annotations

from enum import Enum


class ExportDestinations(Enum):
    FILESYSTEM = "filesystem"
    CHROMA = "chroma"

from __future__ import annotations

from enum import Enum


class SearchTypes(Enum):
    VERSES = "bibledotdev.cli.verses.__main__"

    @staticmethod
    def check_argument(
        argument: str,
    ) -> bool:
        return argument in [search_type.value for search_type in SearchTypes]

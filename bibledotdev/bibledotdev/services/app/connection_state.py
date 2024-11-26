from __future__ import annotations

from enum import Enum

import httpx


class AppConnectionStateType(Enum):
    IS_ONLINE = True
    IS_OFFLINE = False

    @classmethod
    def from_ping(
        cls: type[AppConnectionStateType],
    ) -> AppConnectionStateType:
        try:
            httpx.get(
                "http://8.8.8.8",
                timeout=2,
            )

        except httpx.ConnectionError:
            return AppConnectionStateType.IS_OFFLINE

        else:
            return AppConnectionStateType.IS_ONLINE

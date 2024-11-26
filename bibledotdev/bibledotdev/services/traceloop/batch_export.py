from __future__ import annotations

from enum import Enum

from bibledotdev.services.app import AppConnectionStateType


class TraceloopDisableBatchType(Enum):
    ENABLE_BATCH = False
    DISABLE_BATCH = True

    @classmethod
    def from_app_connection_state(
        cls: type[TraceloopDisableBatchType],
        app_connection_state: AppConnectionStateType,
    ) -> TraceloopDisableBatchType:
        match app_connection_state:
            case AppConnectionStateType.IS_ONLINE:
                return TraceloopDisableBatchType.ENABLE_BATCH

            case AppConnectionStateType.IS_OFFLINE:
                return TraceloopDisableBatchType.DISABLE_BATCH

        raise ValueError

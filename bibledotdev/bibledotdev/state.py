from __future__ import annotations

from typing import TYPE_CHECKING

import reflex as rx
from traceloop.sdk import Traceloop

from bibledotdev.services.app import AppConnectionStateType
from bibledotdev.services.traceloop import TraceloopDisableBatchType
from bibledotdev.tokens import TOKENS

if TYPE_CHECKING:
    import chromadb


chroma_client: chromadb.api.async_api.AsyncClientAPI | None = None
app_connection_state: AppConnectionStateType = AppConnectionStateType.from_ping()
traceloop_disable_batch_type: TraceloopDisableBatchType = (
    TraceloopDisableBatchType.from_app_connection_state(
        app_connection_state=app_connection_state,
    )
)
Traceloop.init(
    disable_batch=traceloop_disable_batch_type.value,
    api_key=TOKENS.get("TRACELOOP_API_KEY"),
    app_name="bibledotdev",
)


class State(rx.State):

    @rx.var(
        cache=True,
    )
    def is_online(
        self,
    ) -> bool:
        return app_connection_state.value

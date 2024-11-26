# trunk-ignore-all(trunk/ignore-does-nothing)
from __future__ import annotations

from typing import TYPE_CHECKING

import chromadb

from bibledotdev.services.app.connection_state import AppConnectionStateType

from .client_type import ClientType

if TYPE_CHECKING:
    from chromadb.api import AsyncClientAPI, ClientAPI


async def set_up_client_from_tokens(
    tokens: dict[str, str | None],
    client_type: ClientType = ClientType.ASYNC,
) -> AsyncClientAPI | ClientAPI | None:
    required_tokens: list[str] = [
        "CHROMA_TENANT",
        "CHROMA_DATABASE",
        "CHROMA_API_KEY",
    ]
    missing_tokens = [token for token in required_tokens if not tokens.get(token)]
    if missing_tokens:
        return None

    match client_type:

        case ClientType.ASYNC:

            chroma_client: AsyncClientAPI = (
                await chromadb.AsyncHttpClient(  # trunk-ignore(pyright/reportReturnType)
                    ssl=True,
                    host="api.trychroma.com",
                    tenant=str(tokens.get("CHROMA_TENANT")),
                    database=str(tokens.get("CHROMA_DATABASE")),
                    headers={
                        "x-chroma-token": str(tokens.get("CHROMA_API_KEY")),
                    },
                )
            )
            return chroma_client

        case ClientType.SYNC:

            return chromadb.Client(
                    ssl=True,
                    host="api.trychroma.com",
                    tenant=str(tokens.get("CHROMA_TENANT")),
                    database=str(tokens.get("CHROMA_DATABASE")),
                    headers={
                        "x-chroma-token": str(tokens.get("CHROMA_API_KEY")),
                    },
                )


async def get_client_chroma(
    app_connection_state: AppConnectionStateType,
    tokens: dict[str, str | None] | None,
    client_type: ClientType = ClientType.ASYNC,
) -> AsyncClientAPI | ClientAPI:
    chroma_client: AsyncClientAPI | None
    match app_connection_state:

        case AppConnectionStateType.IS_ONLINE:
            if tokens is None:
                error_msg: str = "Tokens are required to set up a chroma client"
                raise AssertionError(error_msg)

            chroma_client = await set_up_client_from_tokens(
                tokens=tokens,
                client_type=client_type,
            )
            return chroma_client

        case AppConnectionStateType.IS_OFFLINE:

            match client_type:

                case ClientType.ASYNC:
                    chroma_client = await chromadb.AsyncHttpClient(
                        host="localhost",
                        port=8000,
                    )
                    return chroma_client

                case ClientType.SYNC:
                    return chromadb.HttpClient(
                        host="localhost",
                        port=8000,
                    )

    error_msg: str = "Invalid AppConnectionStateType"
    raise ValueError(error_msg)

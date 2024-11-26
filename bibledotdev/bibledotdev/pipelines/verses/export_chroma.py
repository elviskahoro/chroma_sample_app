from __future__ import annotations

from typing import TYPE_CHECKING

from traceloop.sdk.decorators import task

from bibledotdev.services.app.models.verse import Verse
from bibledotdev.services.chroma import ClientType as ClientTypeChroma

if TYPE_CHECKING:
    from chromadb.api import ClientAPI, Collection

from asyncio import run as aiorun
from typing import NamedTuple

from bibledotdev.services.app import AppConnectionStateType
from bibledotdev.services.chroma import get_client_chroma


class ChromaImport(NamedTuple):
    chroma_id: str
    chroma_document: str
    chroma_metadata: dict[str, str]


@task(
    name="get_client",
)
def _get_client(
    app_connection_state: AppConnectionStateType = AppConnectionStateType.IS_OFFLINE,
    tokens: dict[str, str | None] | None = None,
) -> ClientAPI:
    return aiorun(
        main=get_client_chroma(
            app_connection_state=app_connection_state,
            tokens=tokens,
            client_type=ClientTypeChroma.SYNC,
        ),
    )



@task(
    name="export_to_chroma",
)
def export_to_chroma(
    verses: list[Verse],
    count: int | None = None,
) -> None:
    if count is None:
        count = len(verses)

    chroma_client: ClientAPI = _get_client()
    chroma_collection: Collection = chroma_client.create_collection(
        name="verses",
    )
    chroma_imports: list[ChromaImport] = [
        ChromaImport(
            chroma_id=verse.get_id_for_chroma(),
            chroma_document=verse.get_document_for_chroma(),
            chroma_metadata=verse.get_metadata_for_chroma(
                get_metadata_keys_to_filter_with_for_chroma=Verse.get_metadata_keys_to_filter_with_for_chroma(),
            ),
        )
        for verse in verses[:count]
    ]
    chroma_collection.add(
        ids=[chroma_import.chroma_id for chroma_import in chroma_imports],
        metadatas=[chroma_import.chroma_metadata for chroma_import in chroma_imports],
        documents=[chroma_import.chroma_document for chroma_import in chroma_imports],
    )

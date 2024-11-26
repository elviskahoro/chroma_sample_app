# trunk-ignore-all(ruff/FBT002)
from __future__ import annotations

from asyncio import run as aiorun
from typing import TYPE_CHECKING, Annotated

import typer
from rich.console import Console
from rich.table import Table
from rich.text import Text

from bibledotdev.cli.search_types import SearchTypes
from bibledotdev.cli.utils import is_invalid_argument_exception, is_valid_argument
from bibledotdev.services.app import AppConnectionStateType
from bibledotdev.services.chroma import ClientType, get_client_chroma

if TYPE_CHECKING:
    from chromadb import ClientAPI, Collection, QueryResult

from bibledotdev.tokens import TOKENS

app = typer.Typer()
console = Console()


def highlight_matching_words(
    query_text: str,
    document: str,
) -> Text:
    rich_text = Text(document)
    query_words = set(query_text.lower().split())

    # Find and highlight all matching words
    for word in document.split():
        if word.lower() in query_words:
            start = 0
            while True:
                start = document.lower().find(word.lower(), start)
                if start == -1:
                    break

                rich_text.stylize(
                    "bold yellow",
                    start,
                    start + len(word),
                )
                start += len(word)

    return rich_text


@app.command()
def search(
    query_text: Annotated[str, typer.Argument()],
    count: Annotated[int, typer.Argument()] = 10,
    app_connection_state_raw: Annotated[bool, typer.Argument()] = False,
) -> None:
    argument_type_str: str = __name__
    if not is_valid_argument(
        argument_type_str=argument_type_str,
        argument_type_enum=SearchTypes,  #  trunk-ignore(pyright/reportArgumentType)
    ):
        raise is_invalid_argument_exception(
            argument_type_str=argument_type_str,
            argument_type_enum=SearchTypes,  # trunk-ignore(pyright/reportArgumentType)
        )

    app_connection_state: AppConnectionStateType = (
        AppConnectionStateType.IS_ONLINE
        if app_connection_state_raw
        else AppConnectionStateType.IS_OFFLINE
    )
    chroma_client: ClientAPI = aiorun(
        main=get_client_chroma(
            app_connection_state=app_connection_state,
            tokens=TOKENS,
            client_type=ClientType.SYNC,
        ),
    )

    collection_name: str = "verses"
    collection: Collection = chroma_client.get_collection(
        name=collection_name,
    )
    typer.echo(
        message=f"Collection: {collection_name} count: {collection.count()}",
    )
    query_result: QueryResult = collection.query(
        query_texts=[query_text],
        n_results=count,
    )
    table = Table(
        "distance",
        "document",
        "book_name",
        "chapter",
        "verse_number",
    )
    documents: list[str] | None = query_result.get("documents")[0]
    distances: list[float] | None = query_result.get("distances")[0]
    metadatas: list[str] | None = query_result.get("metadatas")[0]
    for i in range(len(documents)):
        highlighted_document = highlight_matching_words(
            query_text=query_text,
            document=documents[i],
        )
        table.add_row(
            str(distances[i]),
            highlighted_document,
            metadatas[i].get(
                "book_name",
                "unkown",
            ),
            metadatas[i].get(
                "chapter",
                "unknown",
            ),
            metadatas[i].get(
                "verse_number",
                "unknown",
            ),
        )

    console.print(table)


if __name__ == "__main__":
    app()

from __future__ import annotations

from pathlib import Path

import typer
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.semconv.resource import ResourceAttributes
from traceloop.sdk import Traceloop
from traceloop.sdk.decorators import task, workflow

from bibledotdev.pipelines.utils.export_types import ExportDestinations
from bibledotdev.services.app.models.bible_version import (
    FILE_PATH as BIBLE_VERSIONS_FILE_PATH,
    BibleVersion,
)
from bibledotdev.services.app.models.book import (
    FILE_PATH as BOOKS_FILE_PATH,
    Book,
)
from bibledotdev.services.app.models.verse import Verse
from bibledotdev.tokens import TOKENS

from .export_chroma import export_to_chroma
from .export_filesystem import export_to_filesystem

resource_attributes: dict = {
    ResourceAttributes.SERVICE_NAME: "etl-verses",
}
Traceloop.init(
    app_name="etl-verses",
    api_endpoint="https://api.traceloop.com",
    api_key=TOKENS.get("TRACEELOOP_API_KEY"),
    headers={},
    disable_batch=True,
    exporter=ConsoleSpanExporter(),
    metrics_exporter=None,
    metrics_headers=None,
    logging_exporter=ConsoleSpanExporter(),
    logging_headers=None,
    processor=None,
    propagator=None,
    traceloop_sync_enabled=False,
    should_enrich_metrics=True,
    resource_attributes=resource_attributes,
    instruments=None,
    block_instruments=None,
    image_uploader=None,
)


@task(
    name="get_bible_version_abbreviation_from_input_file_name",
)
def get_bible_version_abbreviation_from_input_file_name(
    input_file_name: str,
) -> str:
    input_file_path: Path = Path(input_file_name)
    return input_file_path.stem


@workflow(
    name="etl",
)
def etl(
    input_file_name: str,
    export_destination: ExportDestinations,
    output_folder: str | None = None,
    count: int | None = None,
) -> None:
    bible_versions: list[BibleVersion] = BibleVersion.load_bible_versions_from_file(
        bible_versions_file_path=Path.cwd() / BIBLE_VERSIONS_FILE_PATH,
    )
    books: list[Book] = Book.load_books_from_file(
        books_file_path=Path.cwd() / BOOKS_FILE_PATH,
    )
    current_bible_version: BibleVersion | None = (
        BibleVersion.filter_bible_version_with_abbreviation(
            bible_version_abbreviation=get_bible_version_abbreviation_from_input_file_name(
                input_file_name=input_file_name,
            ),
            bible_versions=bible_versions,
        )
    )
    error_msg: str = "Bible version should not be null"
    if current_bible_version is None:
        raise AssertionError(error_msg)

    verses: list[Verse] = Verse.load_verses_from_file(
        verses_file_path=Path.cwd() / input_file_name,
        bible_version=current_bible_version,
        books=books,
        count=count,
    )
    match export_destination:

        case ExportDestinations.FILESYSTEM:
            export_to_filesystem(
                output_folder=output_folder,
                verses=verses,
                books=books,
            )
            return

        case ExportDestinations.CHROMA:
            export_to_chroma(
                verses=verses,
            )
            return

    error_msg: str = f"Export destination is not valid: {export_destination}"
    raise ValueError(error_msg)


if __name__ == "__main__":
    typer.run(etl)

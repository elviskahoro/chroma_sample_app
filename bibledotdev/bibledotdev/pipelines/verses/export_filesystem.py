from __future__ import annotations

from pathlib import Path

from traceloop.sdk.decorators import task

from bibledotdev.services.app.models import Book, Verse


@task(
    name="get_verses_output_file_path",
)
def get_verses_output_file_path(
    verse: Verse,
    books: list[Book],
    output_folder: str,
    extension: str,
) -> Path:
    current_book: Book | None = Book.filter_book_with_number(
        number=verse.book_number,
        books=books,
    )
    if current_book is None:
        error_message: str = f"Book with number {verse.book_number} not found"
        raise ValueError(error_message)

    book_name: str = current_book.name.lower().replace(
        " ",
        "_",
    )
    output_file_path: Path = (
        Path.cwd()
        / output_folder
        / f"{verse.bible_version_abbreviation}"
        / f"{verse.book_number:03d}-{book_name}"
        / f"{verse.chapter:03d}-chapter"
        / f"{verse.verse_id}.{extension}"
    )
    output_file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    return output_file_path


@task(
    name="export_to_filesystem",
)
def export_to_filesystem(
    verses: list[Verse],
    books: list[Book],
    output_folder: str | None = None,
) -> None:
    if output_folder is None:
        error_msg: str = "output_folder is None"
        raise AssertionError(error_msg)

    for verse in verses:
        output_file: Path = get_verses_output_file_path(
            verse=verse,
            books=books,
            output_folder=output_folder,
            extension="jsonl",
        )
        output_file.write_text(
            data=verse.json(),
        )

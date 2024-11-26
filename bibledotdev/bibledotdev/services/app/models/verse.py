from __future__ import annotations

from typing import TYPE_CHECKING

import orjson
from uuid_extensions import uuid7

from bibledotdev.services.chroma.models.chroma_document_model import ChromaDocumentModel
from bibledotdev.services.etl.models.generic_file_parser import FileContainer

if TYPE_CHECKING:
    from pathlib import Path

    from bibledotdev.services.app.models.bible_version import BibleVersion
    from bibledotdev.services.app.models.book import Book


class Verse(  # trunk-ignore(pyright/reportGeneralTypeIssues)
    ChromaDocumentModel,
    table=True,  # trunk-ignore(pyright/reportCallIssue)
):
    verse_text: str
    bible_version_number: int
    bible_version_abbreviation: str
    book_number: int
    book_name: str
    book_testament: str
    chapter: int
    verse_number: int
    verse_id: int

    @staticmethod
    def get_metadata_keys_to_filter_with_for_chroma() -> list[str]:
        return [
            "bible_version_number",
            "bible_version_abbreviation",
            "book_number",
            "book_name",
            "book_testament",
            "chapter",
            "verse_number",
            "verse_id",
        ]

    @classmethod
    def from_field_array(
        cls: type[Verse],
        field_array: list[str | int],
        bible_version_abbreviation: str,
        bible_version_number: int,
        books: list[Book],
    ) -> Verse:
        book_number: int = int(field_array[1])
        current_book: Book | None = next(
            (book for book in books if book.number == book_number),
            None,
        )
        if current_book is None:
            error_message: str = f"Book with number {book_number} not found"
            raise ValueError(error_message)

        return cls(
            id=uuid7(
                as_type="int",
            ),
            verse_id=int(field_array[0]),
            book_number=book_number,
            chapter=int(field_array[2]),
            verse_number=int(field_array[3]),
            verse_text=str(field_array[4]),
            bible_version_abbreviation=bible_version_abbreviation,
            bible_version_number=bible_version_number,
            book_name=current_book.name,
            book_testament=current_book.testament,
        )

    @staticmethod
    def load_verses_from_file(
        verses_file_path: Path,
        bible_version: BibleVersion,
        books: list[Book],
        count: int | None = None,
    ) -> list[Verse]:
        verses_data: dict = orjson.loads(verses_file_path.read_text())
        file_container_verses: FileContainer = FileContainer.model_validate(
            obj=verses_data,
        )

        error_msg: str = "Bible version id is null"
        if bible_version.id is None:
            raise AssertionError(error_msg)

        if count is None:
            count = len(file_container_verses.resultset.row)

        return [
            Verse.from_field_array(
                field_array=row.field,
                bible_version_number=bible_version.id,
                bible_version_abbreviation=bible_version.abbreviation,
                books=books,
            )
            for row in file_container_verses.resultset.row[:count]
        ]

    def get_id_for_chroma(
        self,
    ) -> str:
        return super().get_id_for_chroma()

    def get_document_for_chroma(
        self,
    ) -> str:
        return self.verse_text

    def get_uri_for_chroma(
        self,
    ) -> str:
        return self.id

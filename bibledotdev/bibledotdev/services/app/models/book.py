from __future__ import annotations

from pathlib import Path

import orjson
import reflex as rx

from bibledotdev.services.etl.models.generic_file_parser import FileContainer

FILE_PATH: Path = Path("data/staging/verses/json/key_english.json")


class Book(  # trunk-ignore(pyright/reportGeneralTypeIssues)
    rx.Model,
    table=True,  # trunk-ignore(pyright/reportCallIssue)
):
    number: int
    name: str
    testament: str

    @staticmethod
    def filter_book_with_number(
        number: int,
        books: list[Book],
    ) -> Book | None:
        return next((book for book in books if book.number == number), None)

    @classmethod
    def from_keys_dict(
        cls: type[Book],
        keys_dict: dict[str, int | str],
    ) -> Book:
        book_number: int | None = None
        book_name: str | None = None
        book_testament: str | None = None

        error_message: str | None = None
        if temp_book_number := keys_dict.get("b"):
            book_number = int(temp_book_number)
        else:
            error_message = "Book number is not found"
            raise ValueError(error_message)

        if temp_book_name := keys_dict.get("n"):
            book_name = str(temp_book_name)
        else:
            error_message = "Book name is not found"
            raise ValueError(error_message)

        if temp_book_testament := keys_dict.get("t"):
            book_testament = str(temp_book_testament)
        else:
            error_message = "Book testament is not found"
            raise ValueError(error_message)

        return cls(
            number=int(book_number),
            name=str(book_name),
            testament=str(book_testament),
        )

    @staticmethod
    def load_books_from_file(
        books_file_path: Path,
    ) -> list[Book]:
        books_data: dict = orjson.loads(books_file_path.read_text())
        file_container_books: FileContainer = FileContainer.model_validate(
            obj=books_data,
        )
        return [
            Book.from_keys_dict(
                keys_dict=keys_dict,
            )
            for keys_dict in file_container_books.resultset.keys
        ]

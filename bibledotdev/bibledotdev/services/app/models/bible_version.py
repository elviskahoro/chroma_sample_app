from __future__ import annotations

from pathlib import Path

import orjson
import reflex as rx

from bibledotdev.services.etl.models.generic_file_parser import FileContainer

FILE_PATH: Path = Path("data/staging/verses/json/bible_version_key.json")


class BibleVersion(  # trunk-ignore(pyright/reportGeneralTypeIssues)
    rx.Model,
    table=True,  # trunk-ignore(pyright/reportCallIssue)
):
    abbreviation: str
    full_name: str
    url: str
    copyright: str

    @staticmethod
    def filter_bible_version_with_abbreviation(
        bible_version_abbreviation: str,
        bible_versions: list[BibleVersion],
    ) -> BibleVersion | None:
        return next(
            (
                bible_version
                for bible_version in bible_versions
                if bible_version.abbreviation == bible_version_abbreviation
            ),
            None,
        )

    @classmethod
    def from_field_array(
        cls: type[BibleVersion],
        field_array: list[str | int],
    ) -> BibleVersion:
        return cls(
            id=int(field_array[0]),
            abbreviation=str(field_array[1]),
            full_name=str(field_array[2]),
            url=str(field_array[3]),
            copyright=str(field_array[4]),
        )

    @staticmethod
    def load_bible_versions_from_file(
        bible_versions_file_path: Path,
    ) -> list[BibleVersion]:
        bible_versions_data: dict = orjson.loads(bible_versions_file_path.read_text())
        file_container_bible_versions: FileContainer = FileContainer.model_validate(
            obj=bible_versions_data,
        )
        return [
            BibleVersion.from_field_array(
                field_array=row.field,
            )
            for row in file_container_bible_versions.resultset.row
        ]

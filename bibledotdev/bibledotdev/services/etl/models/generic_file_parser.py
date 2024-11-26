from __future__ import annotations

from pydantic import BaseModel


class _FieldContainer(BaseModel):
    field: list[int | str]

class _ResultSetContainerRow(BaseModel):
    row: list[_FieldContainer]

class _ResultSetContainerKeys(BaseModel):
    keys: list[dict[str, int | str]]

class FileContainer(BaseModel):
    resultset: _ResultSetContainerRow | _ResultSetContainerKeys

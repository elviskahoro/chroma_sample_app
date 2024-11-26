from __future__ import annotations

import reflex as rx


class ChromaDocumentModel(
    rx.Model,
):

    def get_id_for_chroma(
        self,
    ) -> str:
        if self.id is None:
            error_msg: str = "CHROMA_ID is None"
            raise AttributeError(error_msg)

        return str(self.id)

    @staticmethod
    def get_metadata_keys_to_filter_with_for_chroma() -> list[str]:
        raise NotImplementedError

    def get_metadata_for_chroma(
        self,
        get_metadata_keys_to_filter_with_for_chroma: list[str] | None,
    ) -> dict[str, str]:
        if get_metadata_keys_to_filter_with_for_chroma is None:
            error_msg: str = "CHROMA_METADATA_KEYS is None"
            raise AttributeError(error_msg)

        item_dict: dict = self.dict()
        return {
            key: str(item_dict[key])
            for key in get_metadata_keys_to_filter_with_for_chroma
            if key in item_dict and item_dict[key] is not None
        }

    def get_document_for_chroma(
        self,
    ) -> str:
        raise NotImplementedError

    def get_uri_for_chroma(
        self,
    ) -> str:
        raise NotImplementedError

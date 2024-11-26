from __future__ import annotations

import reflex as rx

from bibledotdev.pages.index.page import index as page_index
from bibledotdev.pages.index.state import State as StatePageIndex

app = rx.App()
app.add_page(
    component=page_index,
    route=None,
    title="Bible.dev",
    description="Semantically search the Bible",
    on_load=StatePageIndex.on_load,
)

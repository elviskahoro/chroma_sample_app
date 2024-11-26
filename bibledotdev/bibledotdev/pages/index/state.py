from __future__ import annotations

import logging

import reflex as rx

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class State(rx.State):

    def on_load(self) -> None:
        logger.info("App loaded")

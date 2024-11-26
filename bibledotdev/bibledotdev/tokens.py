from __future__ import annotations

import os

import dotenv

dotenv.load_dotenv()

TOKENS: dict[str, str | None] = {
    "CHROMA_DATABASE": "devxhackathonprojecttracker",
    "CHROMA_API_KEY": os.getenv("CHROMA_API_KEY"),
    "CHROMA_TENANT": os.getenv("CHROMA_TENANT"),
    "OTEL_PROVIDER_TOKEN_NAME": os.getenv("OTEL_PROVIDER_TOKEN_NAME"),
    "OTEL_APP_NAME": os.getenv("OTEL_APP_NAME"),
    "TRACELOOP_BASE_URL": os.getenv("TRACELOOP_BASE_URL"),
    "TRACELOOP_HEADERS": os.getenv("TRACELOOP_HEADERS"),
    "TRACELOOP_API_KEY": os.getenv("TRACELOOP_API_KEY"),
}

if TOKENS["OTEL_PROVIDER_TOKEN_NAME"] is not None:
    TOKENS.update(
        {
            TOKENS["OTEL_PROVIDER_TOKEN_NAME"]: os.getenv(
                TOKENS["OTEL_PROVIDER_TOKEN_NAME"],
            ),
        },
    )

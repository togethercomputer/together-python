from __future__ import annotations

import os
import sys

# =============================================================================
# SDK 2.0 ANNOUNCEMENT
# =============================================================================
_ANNOUNCEMENT_MESSAGE = """
================================================================================
Together Python SDK 2.0 is now available!

Install: pip install together --upgrade
Install: uv sync --upgrade-package together
New SDK: https://github.com/togethercomputer/together-py
Migration guide: https://docs.together.ai/docs/pythonv2-migration-guide

Together V1 is now deprecated and will be maintained in maintanence mode.
All new features and development will occur in the 2.0 SDK.
================================================================================
"""

# Show info banner (unless suppressed)
if not os.environ.get("TOGETHER_NO_BANNER"):
    try:
        from rich.console import Console
        from rich.panel import Panel

        console = Console(stderr=True)
        console.print(
            Panel(
                "[bold cyan]Together Python SDK 2.0 is now available![/bold cyan]\n\n"
                "Upgrade to the latest version:\n"
                "[green]pip install together --upgrade[/green]  or  "
                "[green]uv sync --upgrade-package together[/green]\n\n"
                "New SDK: [link=https://github.com/togethercomputer/together-py]"
                "https://github.com/togethercomputer/together-py[/link]\n"
                "Migration guide: [link=https://docs.together.ai/docs/pythonv2-migration-guide]"
                "https://docs.together.ai/docs/pythonv2-migration-guide[/link]\n\n"
                "[dim]Together V1 is now deprecated and will be maintained in maintanence mode. All new features and development will occur in the 2.0 SDK.[/dim]\n",
                title="🚀 New SDK Available",
                border_style="cyan",
            )
        )
    except Exception:
        # Fallback for any error (ImportError, OSError in daemons, rich errors, etc.)
        # Banner display should never break module imports
        try:
            print(_ANNOUNCEMENT_MESSAGE, file=sys.stderr)
        except Exception:
            pass  # Silently ignore if even stderr is unavailable

# =============================================================================

from contextvars import ContextVar
from typing import TYPE_CHECKING, Callable

from together import (
    abstract,
    client,
    constants,
    error,
    filemanager,
    resources,
    together_response,
    types,
    utils,
)
from together.version import VERSION

from together.legacy.complete import AsyncComplete, Complete, Completion
from together.legacy.embeddings import Embeddings
from together.legacy.files import Files
from together.legacy.finetune import Finetune
from together.legacy.images import Image
from together.legacy.models import Models

version = VERSION

log: str | None = None  # Set to either 'debug' or 'info', controls console logging

if TYPE_CHECKING:
    import requests
    from aiohttp import ClientSession

requestssession: "requests.Session" | Callable[[], "requests.Session"] | None = None

aiosession: ContextVar["ClientSession" | None] = ContextVar(
    "aiohttp-session", default=None
)

from together.client import AsyncClient, AsyncTogether, Client, Together


api_key: str | None = None  # To be deprecated in the next major release

# Legacy functions


__all__ = [
    "aiosession",
    "constants",
    "version",
    "Together",
    "AsyncTogether",
    "Client",
    "AsyncClient",
    "resources",
    "types",
    "abstract",
    "filemanager",
    "error",
    "together_response",
    "client",
    "utils",
    "Complete",
    "AsyncComplete",
    "Completion",
    "Embeddings",
    "Files",
    "Finetune",
    "Image",
    "Models",
]

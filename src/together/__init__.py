from __future__ import annotations

import os
import sys
import warnings

# =============================================================================
# DEPRECATION NOTICE
# =============================================================================
_DEPRECATION_MESSAGE = """
================================================================================
DEPRECATION WARNING: The 'together' package is deprecated and will no longer
be maintained after January 2026.

Please migrate to the new SDK: https://github.com/togethercomputer/together-py

Migration guide: https://docs.together.ai/docs/pythonv2-migration-guide
================================================================================
"""

# Show deprecation warning (visible to developers with warnings enabled)
warnings.warn(
    "The 'together' package is deprecated and will no longer be maintained after "
    "January 2026. Please migrate to the new SDK: "
    "https://github.com/togethercomputer/together-py "
    "Migration guide: https://docs.together.ai/docs/pythonv2-migration-guide",
    DeprecationWarning,
    stacklevel=2,
)

# Also print a visible notice to stderr (unless suppressed)
if not os.environ.get("TOGETHER_SUPPRESS_DEPRECATION_WARNING"):
    try:
        from rich.console import Console
        from rich.panel import Panel

        console = Console(stderr=True)
        console.print(
            Panel(
                "[bold yellow]DEPRECATION WARNING[/bold yellow]\n\n"
                "The [cyan]together[/cyan] package is deprecated and will no longer "
                "be maintained after [bold]January 2026[/bold].\n\n"
                "Please migrate to the new SDK:\n"
                "[link=https://github.com/togethercomputer/together-py]"
                "https://github.com/togethercomputer/together-py[/link]\n\n"
                "Migration guide:\n"
                "[link=https://docs.together.ai/docs/pythonv2-migration-guide]"
                "https://docs.together.ai/docs/pythonv2-migration-guide[/link]\n\n"
                "[dim]Set TOGETHER_SUPPRESS_DEPRECATION_WARNING=1 to hide this message.[/dim]",
                title="⚠️  Deprecation Notice",
                border_style="yellow",
            )
        )
    except ImportError:
        # Fallback if rich is not available
        print(_DEPRECATION_MESSAGE, file=sys.stderr)

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

from __future__ import annotations

import asyncio
import logging
import sys

import rich.traceback
from rich.console import Console
from rich.logging import RichHandler

from .proxy_scraper_checker import ProxyScraperChecker


def install_uvloop() -> None:
    if sys.implementation.name == "cpython" and sys.platform in {
        "darwin",
        "linux",
    }:
        try:
            import uvloop
        except ImportError:
            pass
        else:
            uvloop.install()


def configure_logging(console: Console) -> None:
    rich.traceback.install(console=console)
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=(
            RichHandler(
                console=console, show_path=False, rich_tracebacks=True
            ),
        ),
    )


def main() -> None:
    install_uvloop()

    console = Console()
    configure_logging(console)

    psc = ProxyScraperChecker.from_ini("config.ini", console=console)
    asyncio.run(psc.run())


if __name__ == "__main__":
    main()
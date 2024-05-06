import asyncio
import logging
from argparse import ArgumentParser
from logging import getLogger

from . import __version__ as APP_VERSION
from .command.run import configure_subcommand_run

logger = getLogger(__name__)


async def main() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        "--version",
        action="version",
        version=APP_VERSION,
    )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s : %(message)s",
    )

    subparsers = parser.add_subparsers()

    subparser_run = subparsers.add_parser("run")
    await configure_subcommand_run(parser=subparser_run)

    args = parser.parse_args()
    if hasattr(args, "handler"):
        handler = args.handler
        if asyncio.iscoroutinefunction(handler):
            await handler(args)
        else:
            handler(args)
    else:
        parser.print_help()

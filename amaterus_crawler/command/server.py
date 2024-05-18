import os
from argparse import ArgumentParser, Namespace
from logging import getLogger

import uvicorn
from fastapi import FastAPI

from .. import __version__ as APP_VERSION
from ..graphql_client import Client
from ..routers import create_youtube_channel_router

logger = getLogger(__name__)


def execute_subcommand_server(
    args: Namespace,
) -> None:
    host: str = args.host
    port: int = args.port

    hasura_url: str | None = args.hasura_url or os.environ.get(
        "AMATERUS_CRAWLER_HASURA_GRAPHQL_ENDPOINT"
    )
    hasura_token: str | None = args.hasura_token or os.environ.get(
        "AMATERUS_CRAWLER_HASURA_GRAPHQL_TOKEN"
    )

    if hasura_url is None:
        raise Exception("hasura_url is None")

    if hasura_token is None:
        raise Exception("hasura_token is None")

    graphql_client = Client(
        url=hasura_url,
        headers={
            "Authorization": f"Bearer {hasura_token}",
        },
    )

    app = FastAPI(
        title="Amaterus Crawler API",
        version=APP_VERSION,
    )

    app.include_router(
        create_youtube_channel_router(
            graphql_client=graphql_client,
        ),
    )

    uvicorn.run(
        app=app,
        host=host,
        port=port,
    )


def configure_parser_subcommand_server(
    parser: ArgumentParser,
) -> None:
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
    )
    parser.add_argument(
        "--hasura_url",
        type=str,
    )
    parser.add_argument(
        "--hasura_token",
        type=str,
    )

    parser.set_defaults(handler=execute_subcommand_server)

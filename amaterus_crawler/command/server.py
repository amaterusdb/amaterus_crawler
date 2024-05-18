import os
from argparse import ArgumentParser, Namespace
from logging import getLogger
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from .. import __version__ as APP_VERSION
from ..config.config_parser import parse_amaterus_crawler_config_from_file
from ..graphql_client import Client
from ..server.routers import create_youtube_channel_router

logger = getLogger(__name__)


class SubcommandServerError(Exception):
    pass


async def execute_subcommand_server(
    args: Namespace,
) -> None:
    config_file: Path = args.config_file

    if not config_file.exists():
        raise SubcommandServerError(f"Config file not exists: {config_file}")

    config = parse_amaterus_crawler_config_from_file(
        config_file=config_file,
    )

    env_server_host = os.environ.get("AMATERUS_CRAWLER_SERVER_HOST") or None
    env_server_port_string = os.environ.get("AMATERUS_CRAWLER_SERVER_PORT") or None
    env_server_port = (
        int(env_server_port_string) if env_server_port_string is not None else None
    )
    env_hasura_url: str | None = os.environ.get("AMATERUS_CRAWLER_HASURA_URL") or None
    env_hasura_access_token: str | None = (
        os.environ.get("AMATERUS_CRAWLER_HASURA_ACCESS_TOKEN") or None
    )
    env_hasura_admin_secret: str | None = (
        os.environ.get("AMATERUS_CRAWLER_HASURA_ADMIN_SECRET") or None
    )
    env_hasura_role: str | None = os.environ.get("AMATERUS_CRAWLER_HASURA_ROLE") or None

    arg_server_host: str | None = args.host or None
    arg_server_port: int | None = args.port or None
    arg_hasura_url: str | None = args.hasura_url or None
    arg_hasura_access_token: str | None = args.hasura_access_token or None
    arg_hasura_admin_secret: str | None = args.hasura_admin_secret or None
    arg_hasura_role: str | None = args.hasura_role or None

    server_host = (
        env_server_host or arg_server_host or config.server_config.host or None
    )
    server_port = (
        env_server_port or arg_server_port or config.server_config.port or None
    )

    hasura_url = (
        env_hasura_url or arg_hasura_url or config.global_config.hasura_url or None
    )
    hasura_access_token = (
        env_hasura_access_token
        or arg_hasura_access_token
        or config.global_config.hasura_access_token
        or None
    )
    hasura_admin_secret = (
        env_hasura_admin_secret
        or arg_hasura_admin_secret
        or config.global_config.hasura_admin_secret
        or None
    )
    hasura_role = (
        env_hasura_role or arg_hasura_role or config.global_config.hasura_role or None
    )

    if server_host is None:
        raise SubcommandServerError("server_host is None")
    if server_port is None:
        raise SubcommandServerError("server_port is None")

    if hasura_url is None:
        raise SubcommandServerError("hasura_url is None")

    graphql_client_headers = {}
    if hasura_access_token is not None:
        graphql_client_headers["Authorization"] = f"Bearer {hasura_access_token}"
    elif hasura_admin_secret is not None:
        graphql_client_headers["X-Hasura-Admin-Secret"] = hasura_admin_secret

    if hasura_role is not None:
        graphql_client_headers["X-Hasura-Role"] = hasura_role

    graphql_client = Client(
        url=hasura_url,
        headers=graphql_client_headers,
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

    uvicorn_config = uvicorn.Config(
        app=app,
        host=server_host,
        port=server_port,
    )
    server = uvicorn.Server(config=uvicorn_config)
    await server.serve()


async def configure_subcommand_server(
    parser: ArgumentParser,
) -> None:
    parser.add_argument(
        "-c",
        "--config_file",
        type=Path,
        required=True,
    )
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
        "--hasura_access_token",
        type=str,
    )
    parser.add_argument(
        "--hasura_admin_secret",
        type=str,
    )
    parser.add_argument(
        "--hasura_role",
        type=str,
    )

    parser.set_defaults(handler=execute_subcommand_server)

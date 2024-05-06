import os
from argparse import ArgumentParser, Namespace
from logging import getLogger
from pathlib import Path

from ..config.config_parser import parse_amaterus_crawler_config_from_file
from ..runner import Runner
from ..runner.youtube_channel_update_runner import YoutubeChannelUpdateRunner
from ..runner.youtube_channel_update_runner.utility.remote_youtube_channel_fetcher import (
    RemoteYoutubeChannelFetcherYoutubeApi,
)
from ..runner.youtube_channel_update_runner.utility.updatable_youtube_channel_fetcher import (
    UpdatableYoutubeChannelFetcherHasura,
)
from ..runner.youtube_channel_update_runner.utility.youtube_channel_updater import (
    YoutubeChannelUpdaterHasura,
)

logger = getLogger(__name__)


class SubcommandRunError(Exception):
    pass


async def execute_subcommand_run(args: Namespace) -> None:
    config_file: Path = args.config_file

    if not config_file.exists():
        raise SubcommandRunError(f"Config file not exists: {config_file}")

    config = parse_amaterus_crawler_config_from_file(
        config_file=config_file,
    )

    env_hasura_url: str | None = os.environ.get("AMATERUS_CRAWLER_HASURA_URL") or None
    env_hasura_access_token: str | None = (
        os.environ.get("AMATERUS_CRAWLER_HASURA_ACCESS_TOKEN") or None
    )
    env_youtube_api_key: str | None = (
        os.environ.get("AMATERUS_CRAWLER_YOUTUBE_API_KEY") or None
    )

    arg_hasura_url: str | None = args.hasura_url or None
    arg_hasura_access_token: str | None = args.hasura_access_token or None
    arg_youtube_api_key: str | None = args.youtube_api_key or None

    hasura_url = env_hasura_url or arg_hasura_url or config.global_config.hasura_url
    hasura_access_token = (
        env_hasura_access_token
        or arg_hasura_access_token
        or config.global_config.hasura_access_token
    )
    youtube_api_key = (
        env_youtube_api_key
        or arg_youtube_api_key
        or config.global_config.youtube_api_key
    )

    runners: list[Runner] = []
    for runner_config in config.runner_configs:
        runner_type = runner_config.type
        if runner_type == "update_youtube_channel":
            if hasura_url is None:
                raise SubcommandRunError("hasura_url is None")
            if hasura_access_token is None:
                raise SubcommandRunError("hasura_access_token is None")
            if youtube_api_key is None:
                raise SubcommandRunError("youtube_api_key is None")

            runners.append(
                YoutubeChannelUpdateRunner(
                    updatable_youtube_channel_fetcher=UpdatableYoutubeChannelFetcherHasura(
                        hasura_url=hasura_url,
                        hasura_access_token=hasura_access_token,
                    ),
                    remote_youtube_channel_fetcher=RemoteYoutubeChannelFetcherYoutubeApi(
                        youtube_api_key=youtube_api_key,
                    ),
                    youtube_channel_updater=YoutubeChannelUpdaterHasura(
                        hasura_url=hasura_url,
                        hasura_access_token=hasura_access_token,
                    ),
                ),
            )

    for runner in runners:
        await runner.run()


async def configure_subcommand_run(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-c",
        "--config_file",
        type=Path,
        required=True,
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
        "--youtube_api_key",
        type=str,
    )

    parser.set_defaults(handler=execute_subcommand_run)

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
    env_hasura_admin_secret: str | None = (
        os.environ.get("AMATERUS_CRAWLER_HASURA_ADMIN_SECRET") or None
    )
    env_hasura_role: str | None = os.environ.get("AMATERUS_CRAWLER_HASURA_ROLE") or None
    env_youtube_api_key: str | None = (
        os.environ.get("AMATERUS_CRAWLER_YOUTUBE_API_KEY") or None
    )
    env_s3_endpoint_url: str | None = (
        os.environ.get("AMATERUS_CRAWLER_S3_ENDPOINT_URL") or None
    )
    env_s3_bucket: str | None = os.environ.get("AMATERUS_CRAWLER_S3_BUCKET") or None
    env_s3_access_key_id: str | None = (
        os.environ.get("AMATERUS_CRAWLER_S3_ACCESS_KEY_ID") or None
    )
    env_s3_secret_access_key: str | None = (
        os.environ.get("AMATERUS_CRAWLER_S3_SECRET_ACCESS_KEY") or None
    )

    arg_hasura_url: str | None = args.hasura_url or None
    arg_hasura_access_token: str | None = args.hasura_access_token or None
    arg_hasura_admin_secret: str | None = args.hasura_admin_secret or None
    arg_hasura_role: str | None = args.hasura_role or None
    arg_youtube_api_key: str | None = args.youtube_api_key or None
    arg_s3_endpoint_url: str | None = args.s3_endpoint_url or None
    arg_s3_bucket: str | None = args.s3_bucket or None
    arg_s3_access_key_id: str | None = args.s3_access_key_id or None
    arg_s3_secret_access_key: str | None = args.s3_secret_access_key or None

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
    youtube_api_key = (
        env_youtube_api_key
        or arg_youtube_api_key
        or config.global_config.youtube_api_key
        or None
    )
    s3_endpoint_url = (
        env_s3_endpoint_url
        or arg_s3_endpoint_url
        or config.global_config.s3_endpoint_url
        or None
    )
    s3_bucket = env_s3_bucket or arg_s3_bucket or config.global_config.s3_bucket or None
    s3_access_key_id = (
        env_s3_access_key_id
        or arg_s3_access_key_id
        or config.global_config.s3_access_key_id
        or None
    )
    s3_secret_access_key = (
        env_s3_secret_access_key
        or arg_s3_secret_access_key
        or config.global_config.s3_secret_access_key
        or None
    )

    runners: list[Runner] = []
    for runner_config in config.runner_configs:
        runner_type = runner_config.type
        if runner_type == "update_youtube_channel":
            if hasura_url is None:
                raise SubcommandRunError("hasura_url is None")
            if youtube_api_key is None:
                raise SubcommandRunError("youtube_api_key is None")

            runners.append(
                YoutubeChannelUpdateRunner(
                    updatable_youtube_channel_fetcher=UpdatableYoutubeChannelFetcherHasura(
                        hasura_url=hasura_url,
                        hasura_access_token=hasura_access_token,
                        hasura_admin_secret=hasura_admin_secret,
                        hasura_role=hasura_role,
                    ),
                    remote_youtube_channel_fetcher=RemoteYoutubeChannelFetcherYoutubeApi(
                        youtube_api_key=youtube_api_key,
                    ),
                    youtube_channel_updater=YoutubeChannelUpdaterHasura(
                        hasura_url=hasura_url,
                        hasura_access_token=hasura_access_token,
                        hasura_admin_secret=hasura_admin_secret,
                        hasura_role=hasura_role,
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
        "--hasura_admin_secret",
        type=str,
    )
    parser.add_argument(
        "--hasura_role",
        type=str,
    )
    parser.add_argument(
        "--youtube_api_key",
        type=str,
    )
    parser.add_argument(
        "--s3_endpoint_url",
        type=str,
    )
    parser.add_argument(
        "--s3_bucket",
        type=str,
    )
    parser.add_argument(
        "--s3_access_key_id",
        type=str,
    )
    parser.add_argument(
        "--s3_secret_access_key",
        type=str,
    )

    parser.set_defaults(handler=execute_subcommand_run)

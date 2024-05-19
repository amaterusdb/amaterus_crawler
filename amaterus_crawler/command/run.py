import os
from argparse import ArgumentParser, Namespace
from logging import getLogger
from pathlib import Path

from ..config.config_parser import parse_amaterus_crawler_config_from_file
from ..config.task_config import (
    DownloadYoutubeChannelThumbnailConfigOptions,
    UpdateYoutubeChannelConfigOptions,
)
from ..config.task_config.search_youtube_channel_video_config import (
    SearchYoutubeChannelVideoConfigOptions,
)
from ..graphql_client import Client
from ..task import AmaterusCrawlerTask
from ..task.youtube_channel_thumbnail_download_task import (
    DownloadableYoutubeChannelThumbnailFetcherHasura,
    YoutubeChannelThumbnailDownloaderYoutubeHttp,
    YoutubeChannelThumbnailDownloadTask,
    YoutubeChannelThumbnailObjectCreatorHasura,
    YoutubeChannelThumbnailUploaderS3,
)
from ..task.youtube_channel_update_task import YoutubeChannelUpdateTask
from ..task.youtube_channel_update_task.utility.remote_youtube_channel_fetcher import (
    RemoteYoutubeChannelFetcherYoutubeApi,
)
from ..task.youtube_channel_update_task.utility.updatable_youtube_channel_fetcher import (  # noqa: B950
    UpdatableYoutubeChannelFetcherHasura as UpdatableYoutubeChannelFetcherHasuraCU,
)
from ..task.youtube_channel_update_task.utility.youtube_channel_updater import (
    YoutubeChannelUpdaterHasura,
)
from ..task.youtube_channel_video_search_task import (
    RemoteYoutubeChannelVideoSearcherYoutubeApi,
)
from ..task.youtube_channel_video_search_task import (
    UpdatableYoutubeChannelFetcherHasura as UpdatableYoutubeChannelFetcherHasuraVS,
)
from ..task.youtube_channel_video_search_task import (
    YoutubeChannelVideoSearchTask,
    YoutubeVideoUpserterHasura,
)
from ..task.youtube_video_detail_update_task import (
    RemoteYoutubeVideoDetailFetcherYoutubeApi,
    UpdatableYoutubeVideoFetcherHasura,
    YoutubeVideoDetailCreatorHasura,
    YoutubeVideoDetailUpdateTask,
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

    graphql_client_headers: dict[str, str] = {}
    if hasura_access_token is not None:
        graphql_client_headers["Authorization"] = f"Bearer {hasura_access_token}"
    elif hasura_admin_secret is not None:
        graphql_client_headers["X-Hasura-Admin-Secret"] = hasura_admin_secret

    if hasura_role is not None:
        graphql_client_headers["X-Hasura-Role"] = hasura_role

    tasks: list[AmaterusCrawlerTask] = []
    for task_config in config.task_configs:
        task_type = task_config.type
        if task_type == "update_youtube_channel":
            options = task_config.options
            if options is not None:
                assert isinstance(options, UpdateYoutubeChannelConfigOptions)

                if options.override_hasura:
                    hasura_url = options.hasura_url
                    hasura_access_token = options.hasura_access_token
                    hasura_admin_secret = options.hasura_admin_secret
                    hasura_role = options.hasura_role

                if options.override_youtube_api_key:
                    youtube_api_key = options.youtube_api_key

            if hasura_url is None:
                raise SubcommandRunError("hasura_url is None")

            if youtube_api_key is None:
                raise SubcommandRunError("youtube_api_key is None")

            hasura_graphql_api_url = hasura_url
            if not hasura_graphql_api_url.endswith("/"):
                hasura_graphql_api_url += "/"
            hasura_graphql_api_url += "v1/graphql"

            graphql_client = Client(
                url=hasura_graphql_api_url,
                headers=graphql_client_headers,
            )

            tasks.append(
                YoutubeChannelUpdateTask(
                    updatable_youtube_channel_fetcher=UpdatableYoutubeChannelFetcherHasuraCU(
                        graphql_client=graphql_client,
                    ),
                    remote_youtube_channel_fetcher=RemoteYoutubeChannelFetcherYoutubeApi(
                        youtube_api_key=youtube_api_key,
                    ),
                    youtube_channel_updater=YoutubeChannelUpdaterHasura(
                        graphql_client=graphql_client,
                    ),
                ),
            )
        elif task_type == "download_youtube_channel_thumbnail":
            object_key_prefix: str | None = None

            options = task_config.options
            if options is not None:
                assert isinstance(options, DownloadYoutubeChannelThumbnailConfigOptions)

                if options.override_hasura:
                    hasura_url = options.hasura_url
                    hasura_access_token = options.hasura_access_token
                    hasura_admin_secret = options.hasura_admin_secret
                    hasura_role = options.hasura_role

                if options.override_s3:
                    s3_endpoint_url = options.s3_endpoint_url
                    s3_bucket = options.s3_bucket
                    s3_access_key_id = options.s3_access_key_id
                    s3_secret_access_key = options.s3_secret_access_key

                object_key_prefix = options.object_key_prefix

            if hasura_url is None:
                raise SubcommandRunError("hasura_url is None")

            if s3_endpoint_url is None:
                raise SubcommandRunError("s3_endpoint_url is None")
            if s3_bucket is None:
                raise SubcommandRunError("s3_bucket is None")
            if s3_access_key_id is None:
                raise SubcommandRunError("s3_access_key_id is None")
            if s3_secret_access_key is None:
                raise SubcommandRunError("s3_secret_access_key is None")

            hasura_graphql_api_url = hasura_url
            if not hasura_graphql_api_url.endswith("/"):
                hasura_graphql_api_url += "/"
            hasura_graphql_api_url += "v1/graphql"

            graphql_client = Client(
                url=hasura_graphql_api_url,
                headers=graphql_client_headers,
            )

            tasks.append(
                YoutubeChannelThumbnailDownloadTask(
                    downloadable_youtube_channel_thumbnail_fetcher=DownloadableYoutubeChannelThumbnailFetcherHasura(
                        graphql_client=graphql_client,
                    ),
                    youtube_channel_thumbnail_downloader=YoutubeChannelThumbnailDownloaderYoutubeHttp(),
                    youtube_channel_thumbnail_uploader=YoutubeChannelThumbnailUploaderS3(
                        s3_endpoint_url=s3_endpoint_url,
                        s3_bucket=s3_bucket,
                        s3_access_key_id=s3_access_key_id,
                        s3_secret_access_key=s3_secret_access_key,
                        object_key_prefix=object_key_prefix,
                    ),
                    youtube_channel_thumbnail_object_creator=YoutubeChannelThumbnailObjectCreatorHasura(
                        graphql_client=graphql_client,
                    ),
                ),
            )
        elif task_type == "search_youtube_channel_video":
            options = task_config.options
            if options is not None:
                assert isinstance(options, SearchYoutubeChannelVideoConfigOptions)

                if options.override_hasura:
                    hasura_url = options.hasura_url
                    hasura_access_token = options.hasura_access_token
                    hasura_admin_secret = options.hasura_admin_secret
                    hasura_role = options.hasura_role

                if options.override_youtube_api_key:
                    youtube_api_key = options.youtube_api_key

            if hasura_url is None:
                raise SubcommandRunError("hasura_url is None")

            if youtube_api_key is None:
                raise SubcommandRunError("youtube_api_key is None")

            hasura_graphql_api_url = hasura_url
            if not hasura_graphql_api_url.endswith("/"):
                hasura_graphql_api_url += "/"
            hasura_graphql_api_url += "v1/graphql"

            graphql_client = Client(
                url=hasura_graphql_api_url,
                headers=graphql_client_headers,
            )

            tasks.append(
                YoutubeChannelVideoSearchTask(
                    updatable_youtube_channel_fetcher=UpdatableYoutubeChannelFetcherHasuraVS(
                        graphql_client=graphql_client,
                    ),
                    remote_youtube_channel_video_searcher=RemoteYoutubeChannelVideoSearcherYoutubeApi(
                        youtube_api_key=youtube_api_key,
                    ),
                    youtube_video_upserter=YoutubeVideoUpserterHasura(
                        graphql_client=graphql_client,
                    ),
                ),
            )
        elif task_type == "update_youtube_video_detail":
            options = task_config.options
            if options is not None:
                assert isinstance(options, SearchYoutubeChannelVideoConfigOptions)

                if options.override_hasura:
                    hasura_url = options.hasura_url
                    hasura_access_token = options.hasura_access_token
                    hasura_admin_secret = options.hasura_admin_secret
                    hasura_role = options.hasura_role

                if options.override_youtube_api_key:
                    youtube_api_key = options.youtube_api_key

            if hasura_url is None:
                raise SubcommandRunError("hasura_url is None")

            if youtube_api_key is None:
                raise SubcommandRunError("youtube_api_key is None")

            hasura_graphql_api_url = hasura_url
            if not hasura_graphql_api_url.endswith("/"):
                hasura_graphql_api_url += "/"
            hasura_graphql_api_url += "v1/graphql"

            graphql_client = Client(
                url=hasura_graphql_api_url,
                headers=graphql_client_headers,
            )

            tasks.append(
                YoutubeVideoDetailUpdateTask(
                    updatable_youtube_video_fetcher=UpdatableYoutubeVideoFetcherHasura(
                        graphql_client=graphql_client,
                    ),
                    remote_youtube_video_detail_fetcher=RemoteYoutubeVideoDetailFetcherYoutubeApi(
                        youtube_api_key=youtube_api_key,
                    ),
                    youtube_video_detail_creator=YoutubeVideoDetailCreatorHasura(
                        graphql_client=graphql_client,
                    ),
                ),
            )

    for task in tasks:
        await task.run()


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

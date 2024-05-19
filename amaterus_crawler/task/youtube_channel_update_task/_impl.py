from datetime import datetime, timezone

from ..base import AmaterusCrawlerTask
from .utility.remote_youtube_channel_fetcher import RemoteYoutubeChannelFetcher
from .utility.updatable_youtube_channel_fetcher import UpdatableYoutubeChannelFetcher
from .utility.youtube_channel_updater import (
    YoutubeChannelUpdateQuery,
    YoutubeChannelUpdateQueryThumbnail,
    YoutubeChannelUpdater,
)


class YoutubeChannelUpdateTask(AmaterusCrawlerTask):
    def __init__(
        self,
        updatable_youtube_channel_fetcher: UpdatableYoutubeChannelFetcher,
        remote_youtube_channel_fetcher: RemoteYoutubeChannelFetcher,
        youtube_channel_updater: YoutubeChannelUpdater,
    ):
        self.updatable_youtube_channel_fetcher = updatable_youtube_channel_fetcher
        self.remote_youtube_channel_fetcher = remote_youtube_channel_fetcher
        self.youtube_channel_updater = youtube_channel_updater

    async def run(self) -> None:
        updatable_youtube_channel_fetcher = self.updatable_youtube_channel_fetcher
        remote_youtube_channel_fetcher = self.remote_youtube_channel_fetcher
        youtube_channel_updater = self.youtube_channel_updater

        youtube_channel_fetch_result = (
            await updatable_youtube_channel_fetcher.fetch_updatable_youtube_channels()
        )

        target_remote_youtube_channel_ids: list[str] = []
        for youtube_channel in youtube_channel_fetch_result.updatable_youtube_channels:
            target_remote_youtube_channel_ids.append(
                youtube_channel.remote_youtube_channel_id
            )

        # YouTube Data APIの1リクエスト当たりの最大取得数がチャンネル50個までのため、50個ずつ更新する
        for start_index in range(0, len(target_remote_youtube_channel_ids), 50):
            target_remote_youtube_channel_ids_chunk = target_remote_youtube_channel_ids[
                start_index : start_index + 50
            ]

            remote_youtube_channel_fetch_result = (
                await remote_youtube_channel_fetcher.fetch_remote_youtube_channels(
                    remote_youtube_channel_ids=target_remote_youtube_channel_ids_chunk,
                )
            )
            remote_youtube_channels = (
                remote_youtube_channel_fetch_result.remote_youtube_channels
            )

            now = datetime.now(tz=timezone.utc)
            update_queries: list[YoutubeChannelUpdateQuery] = []
            for remote_youtube_channel in remote_youtube_channels:
                update_query_thumbnails: list[YoutubeChannelUpdateQueryThumbnail] = []
                for thumbnail in remote_youtube_channel.thumbnails:
                    update_query_thumbnails.append(
                        YoutubeChannelUpdateQueryThumbnail(
                            key=thumbnail.key,
                            url=thumbnail.url,
                            width=thumbnail.width,
                            height=thumbnail.height,
                        ),
                    )

                update_queries.append(
                    YoutubeChannelUpdateQuery(
                        remote_youtube_channel_id=remote_youtube_channel.channel_id,
                        title=remote_youtube_channel.title,
                        description=remote_youtube_channel.description,
                        published_at=remote_youtube_channel.published_at,
                        custom_url=remote_youtube_channel.custom_url,
                        thumbnails=update_query_thumbnails,
                        fetched_at=now,
                    ),
                )

            await youtube_channel_updater.update_youtube_channels(
                update_queries=update_queries,
            )

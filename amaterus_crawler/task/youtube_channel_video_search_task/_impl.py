from datetime import datetime, timezone

from ..base import AmaterusCrawlerTask
from .utility.remote_youtube_channel_video_searcher import (
    RemoteYoutubeChannelVideoSearcher,
)
from .utility.updatable_youtube_channel_fetcher import UpdatableYoutubeChannelFetcher
from .utility.youtube_video_upserter import (
    YoutubeVideoUpserter,
    YoutubeVideoUpsertQuery,
)


class YoutubeChannelVideoSearchTask(AmaterusCrawlerTask):
    def __init__(
        self,
        updatable_youtube_channel_fetcher: UpdatableYoutubeChannelFetcher,
        remote_youtube_channel_video_searcher: RemoteYoutubeChannelVideoSearcher,
        youtube_video_upserter: YoutubeVideoUpserter,
    ):
        self.updatable_youtube_channel_fetcher = updatable_youtube_channel_fetcher
        self.remote_youtube_channel_video_searcher = (
            remote_youtube_channel_video_searcher
        )
        self.youtube_video_upserter = youtube_video_upserter

    async def run(self) -> None:
        updatable_youtube_channel_fetcher = self.updatable_youtube_channel_fetcher
        remote_youtube_channel_video_searcher = (
            self.remote_youtube_channel_video_searcher
        )
        youtube_video_upserter = self.youtube_video_upserter

        fetched_at_aware_string = datetime.now(tz=timezone.utc)

        youtube_channel_fetch_result = (
            await updatable_youtube_channel_fetcher.fetch_updatable_youtube_channels()
        )

        for youtube_channel in youtube_channel_fetch_result.updatable_youtube_channels:
            remote_youtube_channel_id = youtube_channel.remote_youtube_channel_id

            remote_youtube_channel_fetch_result = await remote_youtube_channel_video_searcher.fetch_remote_youtube_channel_videos(  # noqa: B950
                remote_youtube_channel_id=remote_youtube_channel_id,
            )
            remote_youtube_channel_videos = (
                remote_youtube_channel_fetch_result.remote_youtube_channel_videos
            )

            youtube_video_upsert_queries: list[YoutubeVideoUpsertQuery] = []
            for remote_youtube_channel_video in remote_youtube_channel_videos:
                youtube_video_upsert_queries.append(
                    YoutubeVideoUpsertQuery(
                        remote_youtube_video_id=remote_youtube_channel_video.remote_youtube_video_id,
                        fetched_at=fetched_at_aware_string,
                    )
                )

            await youtube_video_upserter.upsert_youtube_videos(
                upsert_queries=youtube_video_upsert_queries,
            )

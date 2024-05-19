from datetime import datetime, timezone

from ..base import AmaterusCrawlerTask
from .utility.remote_youtube_channel_video_detail_fetcher import (
    RemoteYoutubeChannelVideoDetailFetcher,
)
from .utility.remote_youtube_channel_video_searcher import (
    RemoteYoutubeChannelVideoSearcher,
)
from .utility.updatable_youtube_channel_fetcher import UpdatableYoutubeChannelFetcher
from .utility.youtube_channel_video_detail_creator import (
    YoutubeVideoDetailCreateQuery,
    YoutubeVideoDetailCreateQueryThumbnail,
    YoutubeVideoDetailCreator,
)


class YoutubeChannelVideoSearchTask(AmaterusCrawlerTask):
    def __init__(
        self,
        updatable_youtube_channel_fetcher: UpdatableYoutubeChannelFetcher,
        remote_youtube_channel_video_searcher: RemoteYoutubeChannelVideoSearcher,
        remote_youtube_channel_video_detail_fetcher: RemoteYoutubeChannelVideoDetailFetcher,
        youtube_video_detail_creator: YoutubeVideoDetailCreator,
    ):
        self.updatable_youtube_channel_fetcher = updatable_youtube_channel_fetcher
        self.remote_youtube_channel_video_searcher = (
            remote_youtube_channel_video_searcher
        )
        self.remote_youtube_channel_video_detail_fetcher = (
            remote_youtube_channel_video_detail_fetcher
        )
        self.youtube_video_detail_creator = youtube_video_detail_creator

    async def run(self) -> None:
        updatable_youtube_channel_fetcher = self.updatable_youtube_channel_fetcher
        remote_youtube_channel_video_searcher = (
            self.remote_youtube_channel_video_searcher
        )
        remote_youtube_channel_video_detail_fetcher = (
            self.remote_youtube_channel_video_detail_fetcher
        )
        youtube_video_detail_creator = self.youtube_video_detail_creator

        fetched_at_aware = datetime.now(tz=timezone.utc)

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

            remote_youtube_video_ids: list[str] = []
            for remote_youtube_channel_video in remote_youtube_channel_videos:
                remote_youtube_video_ids.append(
                    remote_youtube_channel_video.remote_youtube_video_id
                )

            remote_youtube_channel_video_detail_fetch_result = await remote_youtube_channel_video_detail_fetcher.fetch_remote_youtube_channel_video_details(  # noqa: B950
                remote_youtube_video_ids=remote_youtube_video_ids,
            )
            remote_youtube_channel_video_details = (
                remote_youtube_channel_video_detail_fetch_result.remote_youtube_channel_video_details
            )

            youtube_video_detail_create_queries: list[YoutubeVideoDetailCreateQuery] = (
                []
            )
            for (
                remote_youtube_channel_video_detail
            ) in remote_youtube_channel_video_details:
                thumbnails: list[YoutubeVideoDetailCreateQueryThumbnail] = []
                for thumbnail in remote_youtube_channel_video_detail.thumbnails:
                    thumbnails.append(
                        YoutubeVideoDetailCreateQueryThumbnail(
                            key=thumbnail.key,
                            url=thumbnail.url,
                            width=thumbnail.width,
                            height=thumbnail.height,
                        ),
                    )

                youtube_video_detail_create_queries.append(
                    YoutubeVideoDetailCreateQuery(
                        remote_youtube_channel_id=remote_youtube_channel_video_detail.remote_youtube_channel_id,
                        remote_youtube_video_id=remote_youtube_channel_video_detail.remote_youtube_video_id,
                        title=remote_youtube_channel_video_detail.title,
                        description=remote_youtube_channel_video_detail.description,
                        published_at=remote_youtube_channel_video_detail.published_at,
                        privacy_status=remote_youtube_channel_video_detail.privacy_status,
                        upload_status=remote_youtube_channel_video_detail.upload_status,
                        live_broadcast_content=remote_youtube_channel_video_detail.live_broadcast_content,
                        has_live_streaming_details=remote_youtube_channel_video_detail.has_live_streaming_details,
                        scheduled_start_time=remote_youtube_channel_video_detail.scheduled_start_time,
                        scheduled_end_time=remote_youtube_channel_video_detail.scheduled_end_time,
                        actual_start_time=remote_youtube_channel_video_detail.actual_start_time,
                        actual_end_time=remote_youtube_channel_video_detail.actual_end_time,
                        thumbnails=thumbnails,
                        fetched_at=fetched_at_aware,
                    )
                )

                await youtube_video_detail_creator.create_youtube_video_details(
                    create_queries=youtube_video_detail_create_queries,
                )

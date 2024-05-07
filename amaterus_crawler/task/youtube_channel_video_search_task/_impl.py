from ..base import AmaterusCrawlerTask
from .utility.remote_youtube_channel_video_searcher import (
    RemoteYoutubeChannelVideoSearcher,
)
from .utility.updatable_youtube_channel_fetcher import UpdatableYoutubeChannelFetcher


class YoutubeChannelVideoSearchTask(AmaterusCrawlerTask):
    def __init__(
        self,
        updatable_youtube_channel_fetcher: UpdatableYoutubeChannelFetcher,
        remote_youtube_channel_video_searcher: RemoteYoutubeChannelVideoSearcher,
    ):
        self.updatable_youtube_channel_fetcher = updatable_youtube_channel_fetcher
        self.remote_youtube_channel_video_searcher = (
            remote_youtube_channel_video_searcher
        )

    async def run(self) -> None:
        updatable_youtube_channel_fetcher = self.updatable_youtube_channel_fetcher
        remote_youtube_channel_video_searcher = (
            self.remote_youtube_channel_video_searcher
        )

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

            raise NotImplementedError(remote_youtube_channel_videos)

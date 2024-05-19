from logging import getLogger

from .....graphql_client import Client, GraphQLClientError
from .base import (
    DownloadableYoutubeVideo,
    DownloadableYoutubeVideoFetcher,
    DownloadableYoutubeVideoFetchError,
    DownloadableYoutubeVideoFetchResult,
)

logger = getLogger(__name__)


class DownloadableYoutubeVideoFetcherHasura(DownloadableYoutubeVideoFetcher):
    def __init__(
        self,
        graphql_client: Client,
    ):
        self.graphql_client = graphql_client

    async def fetch_downloadable_youtube_videos(
        self,
    ) -> DownloadableYoutubeVideoFetchResult:
        graphql_client = self.graphql_client

        try:
            result = await graphql_client.get_downloadable_youtube_videos()
        except GraphQLClientError:
            raise DownloadableYoutubeVideoFetchError(
                "Failed to fetch downloadable youtube videos."
            )

        downloadable_youtube_videos: list[DownloadableYoutubeVideo] = []

        youtube_videos = result.youtube_videos
        for youtube_video in youtube_videos:
            downloadable_youtube_videos.append(
                DownloadableYoutubeVideo(
                    remote_youtube_video_id=youtube_video.remote_youtube_video_id,
                ),
            )

        return DownloadableYoutubeVideoFetchResult(
            downloadable_youtube_videos=downloadable_youtube_videos,
        )

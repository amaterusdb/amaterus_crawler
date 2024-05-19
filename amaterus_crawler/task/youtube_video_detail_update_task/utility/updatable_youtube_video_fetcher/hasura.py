from logging import getLogger

from .....graphql_client import Client, GraphQLClientError
from .base import (
    UpdatableYoutubeVideo,
    UpdatableYoutubeVideoFetcher,
    UpdatableYoutubeVideoFetchError,
    UpdatableYoutubeVideoFetchResult,
)

logger = getLogger(__name__)


class UpdatableYoutubeVideoFetcherHasura(UpdatableYoutubeVideoFetcher):
    def __init__(
        self,
        graphql_client: Client,
    ):
        self.graphql_client = graphql_client

    async def fetch_updatable_youtube_videos(
        self,
    ) -> UpdatableYoutubeVideoFetchResult:
        graphql_client = self.graphql_client

        try:
            result = await graphql_client.get_updatable_youtube_videos()
        except GraphQLClientError:
            raise UpdatableYoutubeVideoFetchError(
                "Failed to fetch updatable youtube videos."
            )

        updatable_youtube_videos: list[UpdatableYoutubeVideo] = []

        youtube_videos = result.youtube_videos
        for youtube_video in youtube_videos:
            updatable_youtube_videos.append(
                UpdatableYoutubeVideo(
                    remote_youtube_video_id=youtube_video.remote_youtube_video_id,
                )
            )

        return UpdatableYoutubeVideoFetchResult(
            updatable_youtube_videos=updatable_youtube_videos,
        )

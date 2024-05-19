from logging import getLogger

from .....graphql_client import Client, GraphQLClientError
from .base import (
    DownloadableYoutubeVideoThumbnail,
    DownloadableYoutubeVideoThumbnailFetcher,
    DownloadableYoutubeVideoThumbnailFetchError,
    DownloadableYoutubeVideoThumbnailFetchResult,
)

logger = getLogger(__name__)


class DownloadableYoutubeVideoThumbnailFetcherHasura(
    DownloadableYoutubeVideoThumbnailFetcher
):
    def __init__(
        self,
        graphql_client: Client,
    ):
        self.graphql_client = graphql_client

    async def fetch_downloadable_youtube_video_thumbnails(
        self,
    ) -> DownloadableYoutubeVideoThumbnailFetchResult:
        graphql_client = self.graphql_client

        try:
            result = await graphql_client.get_downloadable_youtube_video_thumbnails()
        except GraphQLClientError:
            raise DownloadableYoutubeVideoThumbnailFetchError(
                "Failed to fetch downloadable youtube video thumbnails."
            )

        downloadable_youtube_video_thumbnails: list[
            DownloadableYoutubeVideoThumbnail
        ] = []

        youtube_video_thumbnails = result.youtube_video_thumbnails
        for youtube_video_thumbnail in youtube_video_thumbnails:
            downloadable_youtube_video_thumbnails.append(
                DownloadableYoutubeVideoThumbnail(
                    remote_youtube_video_id=youtube_video_thumbnail.youtube_video.remote_youtube_video_id,
                    url=youtube_video_thumbnail.url,
                    key=youtube_video_thumbnail.key,
                    width=youtube_video_thumbnail.width,
                    height=youtube_video_thumbnail.height,
                ),
            )

        return DownloadableYoutubeVideoThumbnailFetchResult(
            downloadable_youtube_video_thumbnails=downloadable_youtube_video_thumbnails,
        )

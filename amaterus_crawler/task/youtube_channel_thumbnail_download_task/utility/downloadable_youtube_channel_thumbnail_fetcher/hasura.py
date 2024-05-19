from logging import getLogger

from .....graphql_client import Client, GraphQLClientError
from .base import (
    DownloadableYoutubeChannelThumbnail,
    DownloadableYoutubeChannelThumbnailFetcher,
    DownloadableYoutubeChannelThumbnailFetchError,
    DownloadableYoutubeChannelThumbnailFetchResult,
)

logger = getLogger(__name__)


class DownloadableYoutubeChannelThumbnailFetcherHasura(
    DownloadableYoutubeChannelThumbnailFetcher
):
    def __init__(
        self,
        graphql_client: Client,
    ):
        self.graphql_client = graphql_client

    async def fetch_downloadable_youtube_channel_thumbnails(
        self,
    ) -> DownloadableYoutubeChannelThumbnailFetchResult:
        graphql_client = self.graphql_client

        try:
            result = await graphql_client.get_downloadable_youtube_channel_thumbnails()
        except GraphQLClientError:
            raise DownloadableYoutubeChannelThumbnailFetchError(
                "Failed to fetch downloadable youtube channel icons."
            )

        downloadable_youtube_channel_thumbnails: list[
            DownloadableYoutubeChannelThumbnail
        ] = []

        youtube_channel_thumbnails = result.youtube_channel_thumbnails
        for youtube_channel_thumbnail in youtube_channel_thumbnails:
            downloadable_youtube_channel_thumbnails.append(
                DownloadableYoutubeChannelThumbnail(
                    remote_youtube_channel_id=youtube_channel_thumbnail.youtube_channel.remote_youtube_channel_id,
                    url=youtube_channel_thumbnail.url,
                    key=youtube_channel_thumbnail.key,
                    width=youtube_channel_thumbnail.width,
                    height=youtube_channel_thumbnail.height,
                ),
            )

        return DownloadableYoutubeChannelThumbnailFetchResult(
            downloadable_youtube_channel_thumbnails=downloadable_youtube_channel_thumbnails,
        )

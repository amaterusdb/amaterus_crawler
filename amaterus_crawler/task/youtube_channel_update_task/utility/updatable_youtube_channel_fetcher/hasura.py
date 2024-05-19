from logging import getLogger

from .....graphql_client import Client, GraphQLClientError
from .base import (
    UpdatableYoutubeChannel,
    UpdatableYoutubeChannelFetcher,
    UpdatableYoutubeChannelFetchError,
    UpdatableYoutubeChannelFetchResult,
)

logger = getLogger(__name__)


class UpdatableYoutubeChannelFetcherHasura(UpdatableYoutubeChannelFetcher):
    def __init__(
        self,
        graphql_client: Client,
    ):
        self.graphql_client = graphql_client

    async def fetch_updatable_youtube_channels(
        self,
    ) -> UpdatableYoutubeChannelFetchResult:
        graphql_client = self.graphql_client

        try:
            result = await graphql_client.get_updatable_youtube_channels()
        except GraphQLClientError:
            raise UpdatableYoutubeChannelFetchError(
                "Failed to fetch updatable youtube channels."
            )

        updatable_youtube_channels: list[UpdatableYoutubeChannel] = []

        youtube_channels = result.youtube_channels
        for youtube_channel in youtube_channels:
            updatable_youtube_channels.append(
                UpdatableYoutubeChannel(
                    remote_youtube_channel_id=youtube_channel.remote_youtube_channel_id,
                )
            )

        return UpdatableYoutubeChannelFetchResult(
            updatable_youtube_channels=updatable_youtube_channels,
        )

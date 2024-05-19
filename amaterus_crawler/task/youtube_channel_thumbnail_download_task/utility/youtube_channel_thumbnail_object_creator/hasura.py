from datetime import datetime, timezone
from logging import getLogger

from .....graphql_client import Client, GraphQLClientError
from .base import (
    YoutubeChannelThumbnailObjectCreateError,
    YoutubeChannelThumbnailObjectCreator,
)

logger = getLogger(__name__)


class YoutubeChannelThumbnailObjectCreatorHasura(YoutubeChannelThumbnailObjectCreator):
    def __init__(
        self,
        graphql_client: Client,
    ):
        self.graphql_client = graphql_client

    async def create_youtube_channel_thumbnail_object(
        self,
        remote_youtube_channel_thumbnail_url: str,
        object_key: str,
        sha256_digest: str,
        object_size: int,
        content_type: str,
        fetched_at: datetime,
    ) -> None:
        graphql_client = self.graphql_client

        fetched_at_aware = fetched_at.astimezone(tz=timezone.utc)

        try:
            await graphql_client.create_youtube_channel_thumbnail_object(
                remote_youtube_channel_thumbnail_url=remote_youtube_channel_thumbnail_url,
                object_key=object_key,
                sha_256_digest=sha256_digest,
                object_size=object_size,
                content_type=content_type,
                fetched_at=fetched_at_aware.isoformat(),
            )
        except GraphQLClientError:
            raise YoutubeChannelThumbnailObjectCreateError(
                "Failed to create a youtube channel thumbnail object."
            )

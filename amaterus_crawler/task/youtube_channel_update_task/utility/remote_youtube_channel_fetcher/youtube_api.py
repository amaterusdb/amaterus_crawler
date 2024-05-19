from datetime import datetime, timezone

import httpx
from pydantic import BaseModel

from .base import (
    RemoteYoutubeChannel,
    RemoteYoutubeChannelFetcher,
    RemoteYoutubeChannelFetchError,
    RemoteYoutubeChannelFetchResult,
    RemoteYoutubeChannelThumbnail,
)


class YoutubeApiChannelListResultItemSnippetThumbnail(BaseModel):
    url: str
    width: int
    height: int


class YoutubeApiChannelListResultItemSnippetThumbnails(BaseModel):
    default: YoutubeApiChannelListResultItemSnippetThumbnail | None = None
    medium: YoutubeApiChannelListResultItemSnippetThumbnail | None = None
    high: YoutubeApiChannelListResultItemSnippetThumbnail | None = None


class YoutubeApiChannelListResultItemSnippet(BaseModel):
    title: str
    description: str
    publishedAt: datetime
    customUrl: str | None = None
    thumbnails: YoutubeApiChannelListResultItemSnippetThumbnails | None = None


class YoutubeApiChannelListResultItem(BaseModel):
    id: str
    snippet: YoutubeApiChannelListResultItemSnippet | None = None


class YoutubeApiChannelListResult(BaseModel):
    items: list[YoutubeApiChannelListResultItem] | None = None


class RemoteYoutubeChannelFetcherYoutubeApi(RemoteYoutubeChannelFetcher):
    def __init__(
        self,
        youtube_api_key: str,
    ) -> None:
        self.youtube_api_key = youtube_api_key

    async def fetch_remote_youtube_channels(
        self,
        remote_youtube_channel_ids: list[str],
    ) -> RemoteYoutubeChannelFetchResult:
        youtube_api_key = self.youtube_api_key

        if len(remote_youtube_channel_ids) == 0:
            raise RemoteYoutubeChannelFetchError("channel_ids is empty.")

        if len(remote_youtube_channel_ids) > 50:
            raise RemoteYoutubeChannelFetchError("len(channel_ids) > 50")

        try:
            async with httpx.AsyncClient() as client:
                channel_api_response = await client.get(
                    "https://www.googleapis.com/youtube/v3/channels",
                    params={
                        "key": youtube_api_key,
                        "part": "snippet",
                        "id": ",".join(remote_youtube_channel_ids),
                    },
                )

                channel_api_response.raise_for_status()
        except httpx.HTTPError:
            raise RemoteYoutubeChannelFetchError(
                "Failed to fetch YouTube channel data from YouTube Data API."
            )

        channel_api_dict = channel_api_response.json()
        channel_api_data = YoutubeApiChannelListResult.model_validate(channel_api_dict)

        channel_list_items = channel_api_data.items
        if channel_list_items is None:
            raise RemoteYoutubeChannelFetchError("channel_list_items is None.")
        if len(channel_list_items) == 0:
            raise RemoteYoutubeChannelFetchError("channel_list_items is empty.")

        remote_youtube_channels: list[RemoteYoutubeChannel] = []
        for channel in channel_list_items:
            channel_id = channel.id

            if channel.snippet is None:
                raise RemoteYoutubeChannelFetchError("channel.snippet is None.")

            title = channel.snippet.title
            description = channel.snippet.description
            published_at_aware = channel.snippet.publishedAt.astimezone(tz=timezone.utc)

            custom_url = channel.snippet.customUrl

            thumbnails = channel.snippet.thumbnails
            thumbnail_objects: list[RemoteYoutubeChannelThumbnail] = []

            if thumbnails is not None:
                if thumbnails.high is not None:
                    thumbnail_objects.append(
                        RemoteYoutubeChannelThumbnail(
                            key="high",
                            url=thumbnails.high.url,
                            width=thumbnails.high.width,
                            height=thumbnails.high.height,
                        ),
                    )

                if thumbnails.medium is not None:
                    thumbnail_objects.append(
                        RemoteYoutubeChannelThumbnail(
                            key="medium",
                            url=thumbnails.medium.url,
                            width=thumbnails.medium.width,
                            height=thumbnails.medium.height,
                        ),
                    )

                if thumbnails.default is not None:
                    thumbnail_objects.append(
                        RemoteYoutubeChannelThumbnail(
                            key="default",
                            url=thumbnails.default.url,
                            width=thumbnails.default.width,
                            height=thumbnails.default.height,
                        ),
                    )

            remote_youtube_channels.append(
                RemoteYoutubeChannel(
                    channel_id=channel_id,
                    title=title,
                    description=description,
                    published_at=published_at_aware,
                    custom_url=custom_url,
                    thumbnails=thumbnail_objects,
                ),
            )

        return RemoteYoutubeChannelFetchResult(
            remote_youtube_channels=remote_youtube_channels,
        )

import httpx
from pydantic import BaseModel

from .base import (
    RemoteYoutubeChannel,
    RemoteYoutubeChannelFetcher,
    RemoteYoutubeChannelFetchError,
    RemoteYoutubeChannelFetchResult,
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
        channel_ids: list[str],
    ) -> RemoteYoutubeChannelFetchResult:
        youtube_api_key = self.youtube_api_key

        if len(channel_ids) == 0:
            raise RemoteYoutubeChannelFetchError("channel_ids is empty.")

        if len(channel_ids) > 50:
            raise RemoteYoutubeChannelFetchError("len(channel_ids) > 50")

        try:
            async with httpx.AsyncClient() as client:
                channel_api_response = await client.get(
                    "https://www.googleapis.com/youtube/v3/channels",
                    params={
                        "key": youtube_api_key,
                        "part": "snippet",
                        "id": ",".join(channel_ids),
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
            custom_url = channel.snippet.customUrl
            thumbnails = channel.snippet.thumbnails
            if thumbnails is None:
                raise RemoteYoutubeChannelFetchError("channel.thumbnails is None.")

            icon_url: str | None = None
            if thumbnails.high is not None:
                icon_url = thumbnails.high.url
            elif thumbnails.medium is not None:
                icon_url = thumbnails.medium.url
            elif thumbnails.default is not None:
                icon_url = thumbnails.default.url
            else:
                raise RemoteYoutubeChannelFetchError(
                    "channel.thumbnails.high, medium and default is None."
                )

            remote_youtube_channels.append(
                RemoteYoutubeChannel(
                    channel_id=channel_id,
                    title=title,
                    icon_url=icon_url,
                    screen_name=custom_url,
                ),
            )

        return RemoteYoutubeChannelFetchResult(
            remote_youtube_channels=remote_youtube_channels,
        )

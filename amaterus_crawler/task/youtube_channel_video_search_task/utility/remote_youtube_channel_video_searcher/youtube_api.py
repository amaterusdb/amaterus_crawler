from datetime import datetime, timezone

import httpx
from pydantic import BaseModel

from .base import (
    RemoteYoutubeChannelVideo,
    RemoteYoutubeChannelVideoSearcher,
    RemoteYoutubeChannelVideoSearchError,
    RemoteYoutubeChannelVideoSearchResult,
)


class YoutubeSearchApiResultItemSnippet(BaseModel):
    channelId: str
    channelTitle: str
    title: str
    publishedAt: datetime


class YoutubeSearchApiResultItemId(BaseModel):
    videoId: str


class YoutubeSearchApiResultItem(BaseModel):
    id: YoutubeSearchApiResultItemId
    snippet: YoutubeSearchApiResultItemSnippet | None = None


class YoutubeSearchApiResult(BaseModel):
    items: list[YoutubeSearchApiResultItem] | None = None


class RemoteYoutubeChannelVideoSearcherYoutubeApi(RemoteYoutubeChannelVideoSearcher):
    def __init__(
        self,
        youtube_api_key: str,
    ) -> None:
        self.youtube_api_key = youtube_api_key

    async def fetch_remote_youtube_channel_videos(
        self,
        remote_youtube_channel_id: str,
    ) -> RemoteYoutubeChannelVideoSearchResult:
        youtube_api_key = self.youtube_api_key

        try:
            async with httpx.AsyncClient() as client:
                search_api_response = await client.get(
                    "https://www.googleapis.com/youtube/v3/search",
                    params={
                        "key": youtube_api_key,
                        "part": "id,snippet",
                        "channelId": remote_youtube_channel_id,
                        "type": "video",
                        "order": "date",  # createdAt desc
                        "maxResults": "10",
                    },
                )

                search_api_response.raise_for_status()
        except httpx.HTTPError:
            raise RemoteYoutubeChannelVideoSearchError(
                "Failed to fetch YouTube channel data from YouTube Data API."
            )

        search_api_dict = search_api_response.json()
        search_api_data = YoutubeSearchApiResult.model_validate(search_api_dict)

        channel_video_list_items = search_api_data.items
        if channel_video_list_items is None:
            raise RemoteYoutubeChannelVideoSearchError(
                "channel_video_list_items is None."
            )
        if len(channel_video_list_items) == 0:
            raise RemoteYoutubeChannelVideoSearchError(
                "channel_video_list_items is empty."
            )

        remote_youtube_channel_videos: list[RemoteYoutubeChannelVideo] = []
        for channel_video in channel_video_list_items:
            remote_youtube_video_id = channel_video.id.videoId

            if channel_video.snippet is None:
                raise RemoteYoutubeChannelVideoSearchError("channel.snippet is None.")

            remote_youtube_channel_videos.append(
                RemoteYoutubeChannelVideo(
                    remote_youtube_channel_id=channel_video.snippet.channelId,
                    channel_title=channel_video.snippet.channelTitle,
                    remote_youtube_video_id=remote_youtube_video_id,
                    title=channel_video.snippet.title,
                    published_at=channel_video.snippet.publishedAt.astimezone(
                        tz=timezone.utc
                    ),
                ),
            )

        return RemoteYoutubeChannelVideoSearchResult(
            remote_youtube_channel_videos=remote_youtube_channel_videos,
        )

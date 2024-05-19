from datetime import datetime, timezone
from typing import Literal

import httpx
from pydantic import BaseModel

from .base import (
    RemoteYoutubeVideoDetail,
    RemoteYoutubeVideoDetailFetcher,
    RemoteYoutubeVideoDetailFetchError,
    RemoteYoutubeVideoDetailFetchResult,
    RemoteYoutubeVideoDetailThumbnail,
)


class YoutubeVideoApiResultItemLiveStreamingDetails(BaseModel):
    scheduledStartTime: datetime | None = None
    scheduledEndTime: datetime | None = None
    actualStartTime: datetime | None = None
    actualEndTime: datetime | None = None


class YoutubeVideoApiResultItemSnippetThumbnail(BaseModel):
    url: str
    width: int
    height: int


class YoutubeVideoApiResultItemSnippetThumbnails(BaseModel):
    default: YoutubeVideoApiResultItemSnippetThumbnail | None = None
    medium: YoutubeVideoApiResultItemSnippetThumbnail | None = None
    high: YoutubeVideoApiResultItemSnippetThumbnail | None = None
    standard: YoutubeVideoApiResultItemSnippetThumbnail | None = None
    maxres: YoutubeVideoApiResultItemSnippetThumbnail | None = None


class YoutubeVideoApiResultItemSnippet(BaseModel):
    title: str
    description: str
    channelId: str
    channelTitle: str
    publishedAt: datetime
    liveBroadcastContent: str
    thumbnails: YoutubeVideoApiResultItemSnippetThumbnails


class YoutubeVideoApiResultItemStatus(BaseModel):
    privacyStatus: Literal["public", "private", "unlisted"]
    uploadStatus: Literal["deleted", "failed", "processed", "rejected", "uploaded"]


class YoutubeVideoApiResultItem(BaseModel):
    id: str
    status: YoutubeVideoApiResultItemStatus | None = None
    snippet: YoutubeVideoApiResultItemSnippet | None = None
    liveStreamingDetails: YoutubeVideoApiResultItemLiveStreamingDetails | None = None


class YoutubeVideoApiResult(BaseModel):
    items: list[YoutubeVideoApiResultItem]


class RemoteYoutubeVideoDetailFetcherYoutubeApi(RemoteYoutubeVideoDetailFetcher):
    def __init__(
        self,
        youtube_api_key: str,
    ) -> None:
        self.youtube_api_key = youtube_api_key

    async def fetch_remote_youtube_video_details(
        self,
        remote_youtube_video_ids: list[str],
    ) -> RemoteYoutubeVideoDetailFetchResult:
        youtube_api_key = self.youtube_api_key

        if len(remote_youtube_video_ids) == 0:
            raise RemoteYoutubeVideoDetailFetchError(
                "remote_youtube_video_ids is empty."
            )

        if len(remote_youtube_video_ids) > 50:
            raise RemoteYoutubeVideoDetailFetchError(
                "len(remote_youtube_video_ids) > 50"
            )

        try:
            async with httpx.AsyncClient() as client:
                video_api_response = await client.get(
                    "https://www.googleapis.com/youtube/v3/videos",
                    params={
                        "key": youtube_api_key,
                        "part": "snippet,status,liveStreamingDetails",
                        "id": ",".join(remote_youtube_video_ids),
                    },
                )

                video_api_response.raise_for_status()
        except httpx.HTTPError:
            raise RemoteYoutubeVideoDetailFetchError(
                "Failed to fetch YouTube video data from YouTube Data API."
            )

        video_api_dict = video_api_response.json()
        video_api_data = YoutubeVideoApiResult.model_validate(video_api_dict)

        video_list_items = video_api_data.items
        if len(video_list_items) == 0:
            raise RemoteYoutubeVideoDetailFetchError(
                "channel_video_list_items is empty."
            )

        remote_youtube_video_details: list[RemoteYoutubeVideoDetail] = []
        for channel_video in video_list_items:
            remote_youtube_video_id = channel_video.id

            if channel_video.snippet is None:
                raise RemoteYoutubeVideoDetailFetchError("channel.snippet is None.")

            if channel_video.status is None:
                raise RemoteYoutubeVideoDetailFetchError("channel.status is None.")

            privacy_status = channel_video.status.privacyStatus
            upload_status = channel_video.status.uploadStatus

            live_broadcast_content = channel_video.snippet.liveBroadcastContent

            thumbnails = channel_video.snippet.thumbnails
            thumbnail_objects: list[RemoteYoutubeVideoDetailThumbnail] = []

            if thumbnails.maxres is not None:
                thumbnail_objects.append(
                    RemoteYoutubeVideoDetailThumbnail(
                        key="maxres",
                        url=thumbnails.maxres.url,
                        width=thumbnails.maxres.width,
                        height=thumbnails.maxres.height,
                    ),
                )

            if thumbnails.standard is not None:
                thumbnail_objects.append(
                    RemoteYoutubeVideoDetailThumbnail(
                        key="standard",
                        url=thumbnails.standard.url,
                        width=thumbnails.standard.width,
                        height=thumbnails.standard.height,
                    ),
                )

            if thumbnails.high is not None:
                thumbnail_objects.append(
                    RemoteYoutubeVideoDetailThumbnail(
                        key="high",
                        url=thumbnails.high.url,
                        width=thumbnails.high.width,
                        height=thumbnails.high.height,
                    ),
                )

            if thumbnails.medium is not None:
                thumbnail_objects.append(
                    RemoteYoutubeVideoDetailThumbnail(
                        key="medium",
                        url=thumbnails.medium.url,
                        width=thumbnails.medium.width,
                        height=thumbnails.medium.height,
                    ),
                )

            if thumbnails.default is not None:
                thumbnail_objects.append(
                    RemoteYoutubeVideoDetailThumbnail(
                        key="default",
                        url=thumbnails.default.url,
                        width=thumbnails.default.width,
                        height=thumbnails.default.height,
                    ),
                )

            has_live_streaming_details: bool = False
            scheduled_start_time: datetime | None = None
            scheduled_end_time: datetime | None = None
            actual_start_time: datetime | None = None
            actual_end_time: datetime | None = None
            if channel_video.liveStreamingDetails is not None:
                has_live_streaming_details = True

                liveStreamingDetails = channel_video.liveStreamingDetails
                scheduled_start_time = liveStreamingDetails.scheduledStartTime
                scheduled_end_time = liveStreamingDetails.scheduledEndTime
                actual_start_time = liveStreamingDetails.actualStartTime
                actual_end_time = liveStreamingDetails.actualEndTime

            remote_youtube_video_details.append(
                RemoteYoutubeVideoDetail(
                    remote_youtube_channel_id=channel_video.snippet.channelId,
                    remote_youtube_video_id=remote_youtube_video_id,
                    title=channel_video.snippet.title,
                    description=channel_video.snippet.description,
                    published_at=channel_video.snippet.publishedAt.astimezone(
                        tz=timezone.utc
                    ),
                    privacy_status=privacy_status,
                    upload_status=upload_status,
                    live_broadcast_content=live_broadcast_content,
                    has_live_streaming_details=has_live_streaming_details,
                    scheduled_start_time=scheduled_start_time,
                    scheduled_end_time=scheduled_end_time,
                    actual_start_time=actual_start_time,
                    actual_end_time=actual_end_time,
                    thumbnails=thumbnail_objects,
                ),
            )

        return RemoteYoutubeVideoDetailFetchResult(
            remote_youtube_video_details=remote_youtube_video_details,
        )

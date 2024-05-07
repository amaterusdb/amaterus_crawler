from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RemoteYoutubeChannelVideoDetail:
    remote_youtube_channel_id: str
    """
    チャンネルID
    """
    channel_title: str
    """
    チャンネル名
    """
    remote_youtube_video_id: str
    """
    動画ID
    """
    title: str
    """
    タイトル
    """
    published_at: datetime
    """
    公開日時を表すタイムゾーン付き日時
    """
    thumbnail_url: str | None
    privacy_status: str
    upload_status: str
    live_broadcast_content: str

    has_live_streaming_details: bool
    scheduled_start_time: datetime | None = None
    scheduled_end_time: datetime | None = None
    actual_start_time: datetime | None = None
    actual_end_time: datetime | None = None


@dataclass
class RemoteYoutubeChannelVideoDetailFetchResult:
    remote_youtube_channel_videos: list[RemoteYoutubeChannelVideoDetail]


class RemoteYoutubeChannelVideoDetailFetchError(Exception):
    pass


class RemoteYoutubeChannelVideoDetailFetcher(ABC):
    @abstractmethod
    async def fetch_remote_youtube_channel_video_details(
        self,
        remote_youtube_video_ids: list[str],
    ) -> RemoteYoutubeChannelVideoDetailFetchResult: ...

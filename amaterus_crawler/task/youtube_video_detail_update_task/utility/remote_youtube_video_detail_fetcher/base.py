from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RemoteYoutubeVideoDetailThumbnail:
    key: str
    """
    サムネイルの種類
    """
    url: str
    """
    サムネイルのURL
    """
    width: int
    """
    サムネイルの幅
    """
    height: int
    """
    サムネイルの高さ
    """


@dataclass
class RemoteYoutubeVideoDetail:
    remote_youtube_channel_id: str
    """
    チャンネルID
    """
    remote_youtube_video_id: str
    """
    動画ID
    """
    title: str
    """
    動画のタイトル
    """
    description: str
    """
    動画の説明文
    """
    published_at: datetime
    """
    動画の公開日時を表すタイムゾーン付き日時
    """
    privacy_status: str
    """
    動画の公開設定
    """
    upload_status: str
    """
    動画のアップロード状態
    """
    live_broadcast_content: str
    """
    配信の状態
    """
    has_live_streaming_details: bool
    scheduled_start_time: datetime | None
    scheduled_end_time: datetime | None
    actual_start_time: datetime | None
    actual_end_time: datetime | None
    thumbnails: list[RemoteYoutubeVideoDetailThumbnail]
    """
    動画のサムネイル
    """


@dataclass
class RemoteYoutubeVideoDetailFetchResult:
    remote_youtube_video_details: list[RemoteYoutubeVideoDetail]


class RemoteYoutubeVideoDetailFetchError(Exception):
    pass


class RemoteYoutubeVideoDetailFetcher(ABC):
    @abstractmethod
    async def fetch_remote_youtube_video_details(
        self,
        remote_youtube_video_ids: list[str],
    ) -> RemoteYoutubeVideoDetailFetchResult: ...

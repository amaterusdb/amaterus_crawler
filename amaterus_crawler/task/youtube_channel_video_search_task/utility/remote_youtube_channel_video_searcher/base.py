from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RemoteYoutubeChannelVideo:
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


@dataclass
class RemoteYoutubeChannelVideoSearchResult:
    remote_youtube_channel_videos: list[RemoteYoutubeChannelVideo]


class RemoteYoutubeChannelVideoSearchError(Exception):
    pass


class RemoteYoutubeChannelVideoSearcher(ABC):
    @abstractmethod
    async def fetch_remote_youtube_channel_videos(
        self,
        remote_youtube_channel_id: str,
    ) -> RemoteYoutubeChannelVideoSearchResult: ...

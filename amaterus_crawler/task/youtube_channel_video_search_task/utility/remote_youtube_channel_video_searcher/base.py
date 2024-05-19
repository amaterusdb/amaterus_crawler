from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class RemoteYoutubeChannelVideo:
    remote_youtube_channel_id: str
    """
    チャンネルID
    """
    remote_youtube_video_id: str
    """
    動画ID
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

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class RemoteYoutubeChannel:
    channel_id: str
    """
    チャンネルID
    """
    title: str
    """
    チャンネル名
    """
    icon_url: str
    """
    アイコンURL
    """
    custom_url: str | None
    """
    @ を含むハンドル名
    """


@dataclass
class RemoteYoutubeChannelFetchResult:
    remote_youtube_channels: list[RemoteYoutubeChannel]


class RemoteYoutubeChannelFetchError(Exception):
    pass


class RemoteYoutubeChannelFetcher(ABC):
    @abstractmethod
    async def fetch_remote_youtube_channels(
        self,
        remote_youtube_channel_ids: list[str],
    ) -> RemoteYoutubeChannelFetchResult: ...

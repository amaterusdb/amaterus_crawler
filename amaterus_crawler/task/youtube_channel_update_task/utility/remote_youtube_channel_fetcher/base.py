from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RemoteYoutubeChannelThumbnail:
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
class RemoteYoutubeChannel:
    channel_id: str
    """
    チャンネルID
    """
    title: str
    """
    チャンネルの名前
    """
    description: str
    """
    チャンネルの説明文
    """
    published_at: datetime
    """
    チャンネルの公開日時
    """
    custom_url: str | None
    """
    チャンネルのカスタムURL（@ を含むハンドル名）
    """
    thumbnails: list[RemoteYoutubeChannelThumbnail]
    """
    チャンネルのアイコン
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

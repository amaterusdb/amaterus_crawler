from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class YoutubeChannelUpdateQueryThumbnail:
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
class YoutubeChannelUpdateQuery:
    remote_youtube_channel_id: str
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
    thumbnails: list[YoutubeChannelUpdateQueryThumbnail]
    """
    チャンネルのアイコン
    """
    fetched_at: datetime
    """
    クローラによる自動的な情報取得の日時を表すタイムゾーン付き日時
    """


class YoutubeChannelUpdateError(Exception):
    pass


class YoutubeChannelUpdater(ABC):
    @abstractmethod
    async def update_youtube_channels(
        self,
        update_queries: list[YoutubeChannelUpdateQuery],
    ) -> None: ...

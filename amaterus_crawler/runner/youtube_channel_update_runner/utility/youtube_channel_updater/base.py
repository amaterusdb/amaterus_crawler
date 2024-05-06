from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class YoutubeChannelUpdateQuery:
    remote_youtube_channel_id: str
    """
    チャンネルID
    """
    name: str
    """
    チャンネル名
    """
    icon_url: str
    """
    アイコンURL
    """
    youtube_channel_handle: str | None
    """
    @ を含まないハンドル名
    """
    auto_updated_at: datetime
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

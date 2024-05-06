from abc import ABC, abstractmethod
from dataclasses import dataclass


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


class YoutubeChannelUpdateError(Exception):
    pass


class YoutubeChannelUpdater(ABC):
    @abstractmethod
    async def update_youtube_channels(
        self,
        update_queries: list[YoutubeChannelUpdateQuery],
    ) -> None: ...

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class UpdatableYoutubeChannel:
    remote_youtube_channel_id: str
    name: str | None
    """
    None の場合、未取得のチャンネル
    """


@dataclass
class UpdatableYoutubeChannelFetchResult:
    updatable_youtube_channels: list[UpdatableYoutubeChannel]


class UpdatableYoutubeChannelFetchError(Exception):
    pass


class UpdatableYoutubeChannelFetcher(ABC):
    @abstractmethod
    async def fetch_updatable_youtube_channels(
        self,
    ) -> UpdatableYoutubeChannelFetchResult: ...
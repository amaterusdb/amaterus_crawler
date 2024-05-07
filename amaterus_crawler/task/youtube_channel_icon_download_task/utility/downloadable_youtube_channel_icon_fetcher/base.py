from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class DownloadableYoutubeChannelIcon:
    remote_youtube_channel_id: str
    remote_icon_url: str
    youtube_channel_name: str | None
    """
    None の場合、未取得のチャンネル
    """


@dataclass
class DownloadableYoutubeChannelIconFetchResult:
    downloadable_youtube_channel_icons: list[DownloadableYoutubeChannelIcon]


class DownloadableYoutubeChannelIconFetchError(Exception):
    pass


class DownloadableYoutubeChannelIconFetcher(ABC):
    @abstractmethod
    async def fetch_downloadable_youtube_channel_icons(
        self,
    ) -> DownloadableYoutubeChannelIconFetchResult: ...

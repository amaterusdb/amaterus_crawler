from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class DownloadableYoutubeChannelThumbnail:
    remote_youtube_channel_id: str
    url: str
    key: str
    width: int
    height: int


@dataclass
class DownloadableYoutubeChannelThumbnailFetchResult:
    downloadable_youtube_channel_thumbnails: list[DownloadableYoutubeChannelThumbnail]


class DownloadableYoutubeChannelThumbnailFetchError(Exception):
    pass


class DownloadableYoutubeChannelThumbnailFetcher(ABC):
    @abstractmethod
    async def fetch_downloadable_youtube_channel_thumbnails(
        self,
    ) -> DownloadableYoutubeChannelThumbnailFetchResult: ...

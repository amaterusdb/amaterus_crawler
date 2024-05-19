from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class DownloadableYoutubeVideoThumbnail:
    remote_youtube_video_id: str
    url: str
    key: str
    width: int
    height: int


@dataclass
class DownloadableYoutubeVideoThumbnailFetchResult:
    downloadable_youtube_video_thumbnails: list[DownloadableYoutubeVideoThumbnail]


class DownloadableYoutubeVideoThumbnailFetchError(Exception):
    pass


class DownloadableYoutubeVideoThumbnailFetcher(ABC):
    @abstractmethod
    async def fetch_downloadable_youtube_video_thumbnails(
        self,
    ) -> DownloadableYoutubeVideoThumbnailFetchResult: ...

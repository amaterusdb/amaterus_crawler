from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class DownloadableYoutubeVideo:
    remote_youtube_video_id: str


@dataclass
class DownloadableYoutubeVideoFetchResult:
    downloadable_youtube_videos: list[DownloadableYoutubeVideo]


class DownloadableYoutubeVideoFetchError(Exception):
    pass


class DownloadableYoutubeVideoFetcher(ABC):
    @abstractmethod
    async def fetch_downloadable_youtube_videos(
        self,
    ) -> DownloadableYoutubeVideoFetchResult: ...

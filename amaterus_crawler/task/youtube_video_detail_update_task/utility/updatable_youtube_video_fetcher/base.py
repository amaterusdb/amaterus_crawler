from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class UpdatableYoutubeVideo:
    remote_youtube_video_id: str


@dataclass
class UpdatableYoutubeVideoFetchResult:
    updatable_youtube_videos: list[UpdatableYoutubeVideo]


class UpdatableYoutubeVideoFetchError(Exception):
    pass


class UpdatableYoutubeVideoFetcher(ABC):
    @abstractmethod
    async def fetch_updatable_youtube_videos(
        self,
    ) -> UpdatableYoutubeVideoFetchResult: ...

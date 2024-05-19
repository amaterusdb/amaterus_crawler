from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncContextManager, BinaryIO


@dataclass
class YoutubeVideoDownloadResult:
    remote_youtube_video_id: str
    content_type: str
    sha256_digest: str
    size: int
    binaryio: BinaryIO


class YoutubeVideoDownloadError(Exception):
    pass


class YoutubeVideoDownloader(ABC):
    @abstractmethod
    def download_youtube_video(
        self,
        remote_youtube_video_id: str,
    ) -> AsyncContextManager[YoutubeVideoDownloadResult]: ...

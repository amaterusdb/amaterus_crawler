from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncContextManager, BinaryIO


@dataclass
class YoutubeVideoThumbnailDownloadResult:
    youtube_video_thumbnail_url: str
    content_type: str
    sha256_digest: str
    size: int
    binaryio: BinaryIO


class YoutubeVideoThumbnailDownloadError(Exception):
    pass


class YoutubeVideoThumbnailDownloader(ABC):
    @abstractmethod
    def download_youtube_video_thumbnail(
        self,
        youtube_video_thumbnail_url: str,
    ) -> AsyncContextManager[YoutubeVideoThumbnailDownloadResult]: ...

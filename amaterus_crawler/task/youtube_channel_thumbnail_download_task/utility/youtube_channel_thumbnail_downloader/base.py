from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncContextManager, BinaryIO


@dataclass
class YoutubeChannelThumbnailDownloadResult:
    youtube_channel_thumbnail_url: str
    content_type: str
    sha256_digest: str
    size: int
    binaryio: BinaryIO


class YoutubeChannelThumbnailDownloadError(Exception):
    pass


class YoutubeChannelThumbnailDownloader(ABC):
    @abstractmethod
    def download_youtube_channel_thumbnail(
        self,
        youtube_channel_thumbnail_url: str,
    ) -> AsyncContextManager[YoutubeChannelThumbnailDownloadResult]: ...

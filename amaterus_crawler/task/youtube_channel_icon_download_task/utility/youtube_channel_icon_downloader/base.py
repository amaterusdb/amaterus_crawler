from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncContextManager, BinaryIO


@dataclass
class YoutubeChannelIconDownloadResult:
    youtube_channel_icon_url: str
    content_type: str
    sha256_digest: str
    binaryio: BinaryIO


class YoutubeChannelIconDownloadError(Exception):
    pass


class YoutubeChannelIconDownloader(ABC):
    @abstractmethod
    def download_youtube_channel_icon(
        self,
        youtube_channel_icon_url: str,
    ) -> AsyncContextManager[YoutubeChannelIconDownloadResult]: ...

from abc import ABC, abstractmethod
from typing import BinaryIO


class YoutubeChannelThumbnailUploadError(Exception):
    pass


class YoutubeChannelThumbnailUploader(ABC):
    @abstractmethod
    async def upload_youtube_channel_thumbnail(
        self,
        object_key: str,
        content_type: str,
        binaryio: BinaryIO,
    ) -> None: ...

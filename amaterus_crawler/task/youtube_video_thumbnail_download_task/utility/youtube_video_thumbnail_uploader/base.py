from abc import ABC, abstractmethod
from typing import BinaryIO


class YoutubeVideoThumbnailUploadError(Exception):
    pass


class YoutubeVideoThumbnailUploader(ABC):
    @abstractmethod
    async def upload_youtube_video_thumbnail(
        self,
        object_key: str,
        content_type: str,
        binaryio: BinaryIO,
    ) -> None: ...

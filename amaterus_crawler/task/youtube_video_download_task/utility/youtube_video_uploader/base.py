from abc import ABC, abstractmethod
from typing import BinaryIO


class YoutubeVideoUploadError(Exception):
    pass


class YoutubeVideoUploader(ABC):
    @abstractmethod
    async def upload_youtube_video(
        self,
        object_key: str,
        content_type: str,
        binaryio: BinaryIO,
    ) -> None: ...

from abc import ABC, abstractmethod
from typing import BinaryIO


class YoutubeChannelIconUploadError(Exception):
    pass


class YoutubeChannelIconUploader(ABC):
    @abstractmethod
    async def upload_youtube_channel_icon(
        self,
        object_key: str,
        content_type: str,
        binaryio: BinaryIO,
    ) -> None: ...

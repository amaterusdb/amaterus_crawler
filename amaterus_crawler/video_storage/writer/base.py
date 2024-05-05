from abc import ABC, abstractmethod


class VideoStorageWriteError(Exception):
    pass


class VideoStorageWriter(ABC):
    @abstractmethod
    async def upload_video(self) -> None: ...

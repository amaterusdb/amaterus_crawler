from abc import ABC, abstractmethod


class DownloadVideoFailedError(Exception):
    pass


class VideoDownloader(ABC):
    @abstractmethod
    async def download_video(self) -> None: ...

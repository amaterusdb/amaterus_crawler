from abc import ABC, abstractmethod
from dataclasses import dataclass


class DownloadVideoFailedError(Exception):
    pass


class VideoDownloader(ABC):
    @abstractmethod
    async def download_video(self) -> None: ...

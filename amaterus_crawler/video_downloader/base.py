from abc import ABC


class DownloadVideoFailedError(Exception):
    pass


class VideoDownloader(ABC):
    async def download_video(self) -> None: ...

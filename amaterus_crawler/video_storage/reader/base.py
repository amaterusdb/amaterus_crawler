from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import BinaryIO


@dataclass
class VideoStorageReadResult:
    content_type: str
    content_length: int
    binaryio: BinaryIO


class VideoStorageReadError(Exception):
    pass


class VideoStorageReader(ABC):
    @abstractmethod
    async def download_video(self) -> VideoStorageReadResult: ...

from abc import ABC, abstractmethod

from ..model import VideoInspection


class VideoInspectionReadError(Exception):
    pass


class VideoInspectionReader(ABC):
    @abstractmethod
    async def read_video_inspection(self) -> VideoInspection: ...

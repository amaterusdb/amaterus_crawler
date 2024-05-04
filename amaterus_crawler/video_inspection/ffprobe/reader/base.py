from abc import ABC, abstractmethod

from ..model import FfprobeResult


class FfprobeReadError(Exception):
    pass


class FfprobeReader(ABC):
    @abstractmethod
    async def read_ffprobe(self) -> FfprobeResult: ...

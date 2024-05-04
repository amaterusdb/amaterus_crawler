from abc import ABC

from ..model import FfprobeResult


class FfprobeReadError(Exception):
    pass


class FfprobeReader(ABC):
    async def read_ffprobe(self) -> FfprobeResult: ...

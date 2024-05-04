from abc import ABC, abstractmethod

from ..model import MimetypeResult


class MimetypeReadError(Exception):
    pass


class MimetypeReader(ABC):
    @abstractmethod
    async def read_mimetype(self) -> MimetypeResult: ...

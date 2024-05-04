from logging import getLogger
from typing import BinaryIO

import magic

from ..model import MimetypeResult
from .base import MimetypeReader

logger = getLogger(__name__)


class MimetypeBinaryIOReader(MimetypeReader):
    def __init__(
        self,
        fileobj: BinaryIO,
    ):
        self.fileobj = fileobj

    async def read_mimetype(self) -> MimetypeResult:
        fileobj = self.fileobj

        head_bytes = fileobj.read(1024)
        content_type = magic.from_buffer(head_bytes, mime=True)

        return MimetypeResult(
            content_type=content_type,
        )

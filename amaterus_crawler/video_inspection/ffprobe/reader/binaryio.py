import asyncio
from logging import getLogger
from typing import BinaryIO

from ..model import FfprobeResult
from .base import FfprobeReader, FfprobeReadError

logger = getLogger(__name__)


class FfprobeBinaryIOReader(FfprobeReader):
    def __init__(
        self,
        fileobj: BinaryIO,
    ):
        self.fileobj = fileobj

    async def read_ffprobe(self) -> FfprobeResult:
        fileobj = self.fileobj

        args = [
            "-show_format",
            "-show_streams",
            "-of",
            "json",
            "pipe:0",
        ]

        proc = await asyncio.create_subprocess_exec(
            program="ffprobe",
            *args,
            stdin=fileobj,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await proc.communicate()

        exit_code = proc.returncode
        if exit_code != 0:
            stderr_string = stderr.decode(encoding="utf-8")
            logger.error(f"FFprobe stderr: {stderr_string}")
            raise FfprobeReadError(f"Failed to inspect a video. FFprobe {exit_code=}")

        stdout_string = stdout.decode(encoding="utf-8")
        result = FfprobeResult.model_validate_json(json_data=stdout_string)

        return result

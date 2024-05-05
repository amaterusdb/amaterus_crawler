from typing import BinaryIO

from ..ffprobe.model import FfprobeResultVideoStream
from ..ffprobe.reader import FfprobeBinaryIOReader, FfprobeReadError
from ..model import VideoInspection
from .base import VideoInspectionReader, VideoInspectionReadError


class VideoInspectionBinaryIOReader(VideoInspectionReader):
    def __init__(
        self,
        binaryio: BinaryIO,
    ):
        self.binaryio = binaryio

    async def read_video_inspection(self) -> VideoInspection:
        binaryio = self.binaryio

        reader = FfprobeBinaryIOReader(fileobj=binaryio)
        try:
            result = await reader.read_ffprobe()
        except FfprobeReadError:
            raise VideoInspectionReadError("FFprobe errored.")

        first_video_stream: FfprobeResultVideoStream | None = None
        for stream in result.streams:
            if stream.codec_type == "video" and isinstance(
                stream, FfprobeResultVideoStream
            ):
                first_video_stream = stream

        if first_video_stream is None:
            raise VideoInspectionReadError("No video stream found.")

        return VideoInspection(
            duration=result.duration,
            width=first_video_stream.width,
            height=first_video_stream.height,
            num_frames=first_video_stream.nb_frames,
            frame_rate=first_video_stream.r_frame_rate,
        )

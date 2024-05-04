from typing import Literal

from pydantic import BaseModel


class FfprobeResultVideoStream(BaseModel):
    codec_type: Literal["video"]
    width: int
    height: int
    nb_frames: int
    r_frame_rate: float


class FfprobeResultUnknownStream(BaseModel):
    codec_type: str


class FfprobeResult(BaseModel):
    streams: list[FfprobeResultVideoStream | FfprobeResultUnknownStream]
    duration: float

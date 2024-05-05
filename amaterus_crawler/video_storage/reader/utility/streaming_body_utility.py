from io import BufferedReader, RawIOBase
from typing import BinaryIO

from botocore.response import StreamingBody


class ConvertStreamingBodyToBinaryIoError(Exception):
    pass


def convert_streamingbody_to_binaryio(streaming_body: StreamingBody) -> BinaryIO:
    if not hasattr(streaming_body, "_raw_stream"):
        raise ConvertStreamingBodyToBinaryIoError(
            "StreamingBody._raw_stream not defined"
        )

    raw_stream = streaming_body._raw_stream
    if not isinstance(raw_stream, RawIOBase):
        raise ConvertStreamingBodyToBinaryIoError(
            "StreamingBody._raw_stream is not subclass of RawIOBase"
        )

    buffered_reader = BufferedReader(raw=raw_stream)
    return buffered_reader

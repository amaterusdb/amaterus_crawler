import boto3
import botocore.exceptions

from .base import VideoStorageReader, VideoStorageReadError, VideoStorageReadResult
from .utility.streaming_body_utility import (
    ConvertStreamingBodyToBinaryIoError,
    convert_streamingbody_to_binaryio,
)


class VideoStorageS3Reader(VideoStorageReader):
    def __init__(
        self,
        s3_access_key_id: str,
        s3_secret_access_key: str,
        s3_endpoint_url: str,
        s3_bucket_name: str,
        s3_object_key: str,
    ):
        self.s3_access_key_id = s3_access_key_id
        self.s3_secret_access_key = s3_secret_access_key
        self.s3_endpoint_url = s3_endpoint_url
        self.s3_bucket_name = s3_bucket_name
        self.s3_object_key = s3_object_key

    async def download_video(self) -> VideoStorageReadResult:
        s3_access_key_id = self.s3_access_key_id
        s3_secret_access_key = self.s3_secret_access_key
        s3_endpoint_url = self.s3_endpoint_url
        s3_bucket_name = self.s3_bucket_name
        s3_object_key = self.s3_object_key

        s3 = boto3.resource(
            service_name="s3",
            endpoint_url=s3_endpoint_url,
            aws_access_key_id=s3_access_key_id,
            aws_secret_access_key=s3_secret_access_key,
        )

        bucket = s3.Bucket(name=s3_bucket_name)
        obj = bucket.Object(key=s3_object_key)
        try:
            obj.load()
        except botocore.exceptions.ClientError as err:
            if err.response["Error"]["Code"] == "404":
                raise VideoStorageReadError("S3 errored: No such key.")

            raise VideoStorageReadError("S3 errored: Unknown reason.")

        content_length = obj.content_length

        # S3上のメタデータに設定されたContent-Type
        # S3 CLIのguess機能を使わなかったり、手動設定をしなかったりした場合、
        # binary/octet-stream になる点に注意
        content_type = obj.content_type

        response = obj.get()
        streaming_body = response["Body"]
        try:
            binaryio = convert_streamingbody_to_binaryio(
                streaming_body=streaming_body,
            )
        except ConvertStreamingBodyToBinaryIoError:
            raise VideoStorageReadError(
                "Failed to convert from StreamingBody to BinaryIO."
            )

        return VideoStorageReadResult(
            content_type=content_type,
            content_length=content_length,
            binaryio=binaryio,
        )

from typing import BinaryIO

import boto3
import botocore.exceptions

from .base import VideoStorageWriteError, VideoStorageWriter


class VideoStorageS3Writer(VideoStorageWriter):
    def __init__(
        self,
        s3_access_key_id: str,
        s3_secret_access_key: str,
        s3_endpoint_url: str,
        s3_bucket_name: str,
        s3_object_key: str,
        content_type: str,
        binaryio: BinaryIO,
    ):
        self.s3_access_key_id = s3_access_key_id
        self.s3_secret_access_key = s3_secret_access_key
        self.s3_endpoint_url = s3_endpoint_url
        self.s3_bucket_name = s3_bucket_name
        self.s3_object_key = s3_object_key
        self.content_type = content_type
        self.binaryio = binaryio

    async def upload_video(self) -> None:
        s3_access_key_id = self.s3_access_key_id
        s3_secret_access_key = self.s3_secret_access_key
        s3_endpoint_url = self.s3_endpoint_url
        s3_bucket_name = self.s3_bucket_name
        s3_object_key = self.s3_object_key
        content_type = self.content_type
        binaryio = self.binaryio

        s3 = boto3.resource(
            service_name="s3",
            endpoint_url=s3_endpoint_url,
            aws_access_key_id=s3_access_key_id,
            aws_secret_access_key=s3_secret_access_key,
        )

        bucket = s3.Bucket(name=s3_bucket_name)
        obj = bucket.Object(key=s3_object_key)
        try:
            obj.upload_fileobj(
                Fileobj=binaryio,
                ExtraArgs={
                    "ContentType": content_type,
                },
            )
        except botocore.exceptions.ClientError:
            raise VideoStorageWriteError("S3 errored.")

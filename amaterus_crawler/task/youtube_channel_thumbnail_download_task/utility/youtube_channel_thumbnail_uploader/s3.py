from typing import BinaryIO

import boto3
import botocore.exceptions

from .base import YoutubeChannelThumbnailUploader, YoutubeChannelThumbnailUploadError


class YoutubeChannelThumbnailUploaderS3(YoutubeChannelThumbnailUploader):
    def __init__(
        self,
        s3_endpoint_url: str,
        s3_bucket: str,
        s3_access_key_id: str,
        s3_secret_access_key: str,
        object_key_prefix: str | None = None,
    ):
        self.s3_endpoint_url = s3_endpoint_url
        self.s3_bucket = s3_bucket
        self.s3_access_key_id = s3_access_key_id
        self.s3_secret_access_key = s3_secret_access_key
        self.object_key_prefix = object_key_prefix

    async def upload_youtube_channel_thumbnail(
        self,
        object_key: str,
        content_type: str,
        binaryio: BinaryIO,
    ) -> None:
        s3_endpoint_url = self.s3_endpoint_url
        s3_bucket = self.s3_bucket
        s3_access_key_id = self.s3_access_key_id
        s3_secret_access_key = self.s3_secret_access_key
        object_key_prefix = self.object_key_prefix

        s3 = boto3.resource(
            service_name="s3",
            endpoint_url=s3_endpoint_url,
            aws_access_key_id=s3_access_key_id,
            aws_secret_access_key=s3_secret_access_key,
        )

        bucket = s3.Bucket(name=s3_bucket)

        full_object_key = ""
        if object_key_prefix is not None:
            full_object_key += object_key_prefix
        full_object_key += object_key

        obj = bucket.Object(key=full_object_key)
        try:
            obj.upload_fileobj(
                Fileobj=binaryio,
                ExtraArgs={
                    "ContentType": content_type,
                },
            )
        except botocore.exceptions.ClientError:
            raise YoutubeChannelThumbnailUploadError("S3 errored.")

import tempfile
from pathlib import Path
from uuid import uuid4

import boto3
from yt_dlp import YoutubeDL
from yt_dlp.utils import YoutubeDLError

from .base import DownloadVideoFailedError, VideoDownloader


class VideoDownloaderYoutubeS3(VideoDownloader):
    def __init__(
        self,
        youtube_video_url: str,
        s3_access_key_id: str,
        s3_secret_access_key: str,
        s3_endpoint_url: str,
        s3_bucket_name: str,
        s3_object_key: str,
    ):
        self.youtube_video_url = youtube_video_url
        self.s3_access_key_id = s3_access_key_id
        self.s3_secret_access_key = s3_secret_access_key
        self.s3_endpoint_url = s3_endpoint_url
        self.s3_bucket_name = s3_bucket_name
        self.s3_object_key = s3_object_key

    async def download_video(self) -> None:
        youtube_video_url = self.youtube_video_url
        s3_access_key_id = self.s3_access_key_id
        s3_secret_access_key = self.s3_secret_access_key
        s3_endpoint_url = self.s3_endpoint_url
        s3_bucket_name = self.s3_bucket_name
        s3_object_key = self.s3_object_key

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            tmp_id = str(uuid4())

            try:
                with YoutubeDL(
                    params={
                        "paths": {
                            "home": tmpdir,
                        },
                        "outtmpl": f"{tmp_id}.%(ext)s",
                    },
                ) as ydl:
                    error_code = ydl.download(url_list=[youtube_video_url])
                    if error_code != 0:
                        raise DownloadVideoFailedError(
                            f"Failed to download. {error_code=}"
                        )
            except YoutubeDLError:
                raise DownloadVideoFailedError(
                    "Failed to download. YouTubeDLError occured."
                )

        video_file: Path | None = None
        for tmp_file in tmpdir_path.iterdir():
            if tmp_file.stem == tmp_id:
                video_file = tmp_file
                break

        if video_file is None:
            raise DownloadVideoFailedError(
                f"Failed to download. No file downloaded in temp dir: {tmpdir_path}"
            )

        s3 = boto3.resource(
            service_name="s3",
            endpoint_url=s3_endpoint_url,
            aws_access_key_id=s3_access_key_id,
            aws_secret_access_key=s3_secret_access_key,
        )
        bucket = s3.Bucket(name=s3_bucket_name)
        bucket.upload_file(
            Filename=str(tmpdir_path),
            Key=s3_object_key,
        )

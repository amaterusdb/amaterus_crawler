import tempfile
from pathlib import Path
from uuid import uuid4

from mypy_boto3_s3.service_resource import Bucket
from yt_dlp import YoutubeDL
from yt_dlp.utils import YoutubeDLError

from .base import DownloadVideoFailedError, VideoDownloader


class VideoDownloaderYoutubeS3(VideoDownloader):
    def __init__(
        self,
        youtube_video_url: str,
        output_bucket: Bucket,
        output_object_key: str,
    ):
        self.youtube_video_url = youtube_video_url
        self.output_bucket = output_bucket
        self.output_object_key = output_object_key

    async def download_video(self) -> None:
        youtube_video_url = self.youtube_video_url
        output_bucket = self.output_bucket
        output_object_key = self.output_object_key

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
                    f"Failed to download. YouTubeDLError occured."
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

        output_bucket.upload_file(
            Filename=tmpdir_path,
            Key=output_object_key,
        )

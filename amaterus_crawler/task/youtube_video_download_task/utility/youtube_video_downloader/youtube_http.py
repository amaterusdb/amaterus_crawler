import asyncio
import hashlib
import mimetypes
import tempfile
from contextlib import asynccontextmanager
from logging import getLogger
from pathlib import Path
from typing import AsyncIterator

from yt_dlp import YoutubeDL
from yt_dlp.utils import YoutubeDLError

from .base import (
    YoutubeVideoDownloader,
    YoutubeVideoDownloadError,
    YoutubeVideoDownloadResult,
)

logger = getLogger(__name__)


class YoutubeVideoDownloaderYoutubeHttp(YoutubeVideoDownloader):
    @asynccontextmanager
    async def download_youtube_video(
        self,
        remote_youtube_video_id: str,
    ) -> AsyncIterator[YoutubeVideoDownloadResult]:
        youtube_video_url = f"https://www.youtube.com/watch?v={remote_youtube_video_id}"

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            try:
                with YoutubeDL(
                    params={
                        "paths": {
                            "home": tmpdir,
                        },
                    },
                ) as ydl:
                    return_code = await asyncio.to_thread(
                        ydl.download,
                        url_list=[youtube_video_url],
                    )
                    if return_code != 0:
                        raise YoutubeVideoDownloadError(
                            f"yt-dlp errored (return code: {return_code})."
                        )
            except YoutubeDLError:
                raise YoutubeVideoDownloadError(
                    "yt-dlp errored. YouTubeDLError occured."
                )

            video_files = sorted(list(tmpdir_path.iterdir()))
            first_video_file: Path | None = None
            content_type: str | None = None
            for video_file in video_files:
                content_type = mimetypes.guess_type(video_file)[0]
                if content_type is None:
                    continue
                if content_type.startswith("video/"):
                    first_video_file = video_file
                    break

            if first_video_file is None or content_type is None:
                raise YoutubeVideoDownloadError(
                    "No video file downloaded.",
                )

            size = first_video_file.stat().st_size

            with first_video_file.open(mode="rb") as fileobj:
                sha256_hash = hashlib.file_digest(fileobj, hashlib.sha256)
            sha256_digest = sha256_hash.hexdigest()

            with first_video_file.open(mode="rb") as fileobj:
                yield YoutubeVideoDownloadResult(
                    remote_youtube_video_id=remote_youtube_video_id,
                    content_type=content_type,
                    sha256_digest=sha256_digest,
                    size=size,
                    binaryio=fileobj,
                )

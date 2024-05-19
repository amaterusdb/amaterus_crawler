import hashlib
import tempfile
from contextlib import AsyncExitStack, asynccontextmanager
from logging import getLogger
from typing import AsyncIterator

import httpx

from .base import (
    YoutubeVideoThumbnailDownloader,
    YoutubeVideoThumbnailDownloadError,
    YoutubeVideoThumbnailDownloadResult,
)

logger = getLogger(__name__)


class YoutubeVideoThumbnailDownloaderYoutubeHttp(YoutubeVideoThumbnailDownloader):
    @asynccontextmanager
    async def download_youtube_video_thumbnail(
        self,
        youtube_video_thumbnail_url: str,
    ) -> AsyncIterator[YoutubeVideoThumbnailDownloadResult]:
        async with AsyncExitStack() as exit_stack:
            temp_icon_fileobj = exit_stack.enter_context(tempfile.TemporaryFile())
            sha256_hash = hashlib.sha256()
            size = 0

            async with httpx.AsyncClient() as client:
                try:
                    async with client.stream(
                        method="GET", url=youtube_video_thumbnail_url
                    ) as response:
                        if "Content-Type" not in response.headers:
                            raise YoutubeVideoThumbnailDownloadError(
                                "No Content-Type response header."
                            )

                        content_type = response.headers["Content-Type"]
                        if not content_type.startswith("image/"):
                            raise YoutubeVideoThumbnailDownloadError(
                                "Content-Type is not image/*."
                            )

                        async for chunk in response.aiter_bytes():
                            temp_icon_fileobj.write(chunk)
                            sha256_hash.update(chunk)
                            size += len(chunk)
                except httpx.HTTPError as err:
                    logger.error(err)
                    raise YoutubeVideoThumbnailDownloadError("httpx error occured.")

            sha256_digest = sha256_hash.hexdigest()

            temp_icon_fileobj.flush()
            temp_icon_fileobj.seek(0)

            yield YoutubeVideoThumbnailDownloadResult(
                youtube_video_thumbnail_url=youtube_video_thumbnail_url,
                content_type=content_type,
                sha256_digest=sha256_digest,
                size=size,
                binaryio=temp_icon_fileobj,
            )
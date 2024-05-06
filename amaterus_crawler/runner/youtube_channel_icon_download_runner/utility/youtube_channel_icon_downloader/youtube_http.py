import hashlib
import tempfile
from contextlib import AsyncExitStack, asynccontextmanager
from logging import getLogger
from typing import AsyncIterator

import httpx

from .base import (
    YoutubeChannelIconDownloader,
    YoutubeChannelIconDownloadError,
    YoutubeChannelIconDownloadResult,
)

logger = getLogger(__name__)


class YoutubeChannelIconDownloaderYoutubeHttp(YoutubeChannelIconDownloader):
    @asynccontextmanager
    async def download_youtube_channel_icon(
        self,
        youtube_channel_icon_url: str,
    ) -> AsyncIterator[YoutubeChannelIconDownloadResult]:
        async with AsyncExitStack() as exit_stack:
            temp_icon_fileobj = exit_stack.enter_context(tempfile.TemporaryFile())
            sha256_hash = hashlib.sha256()

            async with httpx.AsyncClient() as client:
                try:
                    async with client.stream(
                        method="GET", url=youtube_channel_icon_url
                    ) as response:
                        if "Content-Type" not in response.headers:
                            raise YoutubeChannelIconDownloadError(
                                "No Content-Type response header."
                            )

                        content_type = response.headers["Content-Type"]

                        async for chunk in response.aiter_bytes():
                            temp_icon_fileobj.write(chunk)
                            sha256_hash.update(chunk)
                except httpx.HTTPError as err:
                    logger.error(err)
                    raise YoutubeChannelIconDownloadError("httpx error occured.")

            sha256_digest = sha256_hash.hexdigest()

            temp_icon_fileobj.flush()
            temp_icon_fileobj.seek(0)

            yield YoutubeChannelIconDownloadResult(
                youtube_channel_icon_url=youtube_channel_icon_url,
                content_type=content_type,
                sha256_digest=sha256_digest,
                binaryio=temp_icon_fileobj,
            )

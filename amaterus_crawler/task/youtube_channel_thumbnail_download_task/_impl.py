from datetime import datetime, timezone
from uuid import uuid4

from ..base import AmaterusCrawlerTask
from .utility.downloadable_youtube_channel_thumbnail_fetcher import (
    DownloadableYoutubeChannelThumbnailFetcher,
)
from .utility.youtube_channel_thumbnail_downloader import (
    YoutubeChannelThumbnailDownloader,
    YoutubeChannelThumbnailDownloadError,
)
from .utility.youtube_channel_thumbnail_object_creator import (
    YoutubeChannelThumbnailObjectCreateError,
    YoutubeChannelThumbnailObjectCreator,
)
from .utility.youtube_channel_thumbnail_uploader import (
    YoutubeChannelThumbnailUploader,
    YoutubeChannelThumbnailUploadError,
)


class YoutubeChannelThumbnailDownloadTask(AmaterusCrawlerTask):
    def __init__(
        self,
        downloadable_youtube_channel_thumbnail_fetcher: DownloadableYoutubeChannelThumbnailFetcher,  # noqa: B950
        youtube_channel_thumbnail_downloader: YoutubeChannelThumbnailDownloader,
        youtube_channel_thumbnail_uploader: YoutubeChannelThumbnailUploader,
        youtube_channel_thumbnail_object_creator: YoutubeChannelThumbnailObjectCreator,
    ):
        self.downloadable_youtube_channel_thumbnail_fetcher = (
            downloadable_youtube_channel_thumbnail_fetcher
        )
        self.youtube_channel_thumbnail_downloader = youtube_channel_thumbnail_downloader
        self.youtube_channel_thumbnail_uploader = youtube_channel_thumbnail_uploader
        self.youtube_channel_thumbnail_object_creator = (
            youtube_channel_thumbnail_object_creator
        )

    async def run(self) -> None:
        downloadable_youtube_channel_thumbnail_fetcher = (
            self.downloadable_youtube_channel_thumbnail_fetcher
        )
        youtube_channel_thumbnail_downloader = self.youtube_channel_thumbnail_downloader
        youtube_channel_thumbnail_uploader = self.youtube_channel_thumbnail_uploader
        youtube_channel_thumbnail_object_creator = (
            self.youtube_channel_thumbnail_object_creator
        )

        fetched_at_aware = datetime.now(tz=timezone.utc)

        youtube_channel_thumbnail_fetch_result = (
            await downloadable_youtube_channel_thumbnail_fetcher.fetch_downloadable_youtube_channel_thumbnails()  # noqa: B950
        )

        downloadable_youtube_channel_thumbnails = (
            youtube_channel_thumbnail_fetch_result.downloadable_youtube_channel_thumbnails
        )

        exceptions: list[
            YoutubeChannelThumbnailDownloadError
            | YoutubeChannelThumbnailUploadError
            | YoutubeChannelThumbnailObjectCreateError
        ] = []
        for (
            downloadable_youtube_channel_thumbnail
        ) in downloadable_youtube_channel_thumbnails:
            thumbnail_url = downloadable_youtube_channel_thumbnail.url

            try:
                async with youtube_channel_thumbnail_downloader.download_youtube_channel_thumbnail(  # noqa: B950
                    youtube_channel_thumbnail_url=thumbnail_url,
                ) as download_result:
                    content_type = download_result.content_type
                    object_size = download_result.size
                    object_key = str(uuid4())

                    await youtube_channel_thumbnail_uploader.upload_youtube_channel_thumbnail(
                        object_key=object_key,
                        content_type=content_type,
                        binaryio=download_result.binaryio,
                    )

                    await youtube_channel_thumbnail_object_creator.create_youtube_channel_thumbnail_object(  # noqa: B950
                        remote_youtube_channel_thumbnail_url=thumbnail_url,
                        object_key=object_key,
                        sha256_digest=download_result.sha256_digest,
                        object_size=object_size,
                        content_type=content_type,
                        fetched_at=fetched_at_aware,
                    )
            except (
                YoutubeChannelThumbnailDownloadError,
                YoutubeChannelThumbnailUploadError,
                YoutubeChannelThumbnailObjectCreateError,
            ) as err:
                exceptions.append(err)

        if len(exceptions) > 0:
            raise ExceptionGroup(
                "Some errors occured.",
                exceptions,
            )

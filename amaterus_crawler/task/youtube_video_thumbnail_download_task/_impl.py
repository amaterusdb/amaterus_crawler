from datetime import datetime, timezone
from uuid import uuid4

from ..base import AmaterusCrawlerTask
from .utility.downloadable_youtube_video_thumbnail_fetcher import (
    DownloadableYoutubeVideoThumbnailFetcher,
)
from .utility.youtube_video_thumbnail_downloader import (
    YoutubeVideoThumbnailDownloader,
    YoutubeVideoThumbnailDownloadError,
)
from .utility.youtube_video_thumbnail_object_creator import (
    YoutubeVideoThumbnailObjectCreateError,
    YoutubeVideoThumbnailObjectCreator,
)
from .utility.youtube_video_thumbnail_uploader import (
    YoutubeVideoThumbnailUploader,
    YoutubeVideoThumbnailUploadError,
)


class YoutubeVideoThumbnailDownloadTask(AmaterusCrawlerTask):
    def __init__(
        self,
        downloadable_youtube_video_thumbnail_fetcher: DownloadableYoutubeVideoThumbnailFetcher,  # noqa: B950
        youtube_video_thumbnail_downloader: YoutubeVideoThumbnailDownloader,
        youtube_video_thumbnail_uploader: YoutubeVideoThumbnailUploader,
        youtube_video_thumbnail_object_creator: YoutubeVideoThumbnailObjectCreator,
    ):
        self.downloadable_youtube_video_thumbnail_fetcher = (
            downloadable_youtube_video_thumbnail_fetcher
        )
        self.youtube_video_thumbnail_downloader = youtube_video_thumbnail_downloader
        self.youtube_video_thumbnail_uploader = youtube_video_thumbnail_uploader
        self.youtube_video_thumbnail_object_creator = (
            youtube_video_thumbnail_object_creator
        )

    async def run(self) -> None:
        downloadable_youtube_video_thumbnail_fetcher = (
            self.downloadable_youtube_video_thumbnail_fetcher
        )
        youtube_video_thumbnail_downloader = self.youtube_video_thumbnail_downloader
        youtube_video_thumbnail_uploader = self.youtube_video_thumbnail_uploader
        youtube_video_thumbnail_object_creator = (
            self.youtube_video_thumbnail_object_creator
        )

        fetched_at_aware = datetime.now(tz=timezone.utc)

        youtube_video_thumbnail_fetch_result = (
            await downloadable_youtube_video_thumbnail_fetcher.fetch_downloadable_youtube_video_thumbnails()  # noqa: B950
        )

        downloadable_youtube_video_thumbnails = (
            youtube_video_thumbnail_fetch_result.downloadable_youtube_video_thumbnails
        )

        exceptions: list[
            YoutubeVideoThumbnailDownloadError
            | YoutubeVideoThumbnailUploadError
            | YoutubeVideoThumbnailObjectCreateError
        ] = []
        for (
            downloadable_youtube_video_thumbnail
        ) in downloadable_youtube_video_thumbnails:
            thumbnail_url = downloadable_youtube_video_thumbnail.url

            try:
                async with youtube_video_thumbnail_downloader.download_youtube_video_thumbnail(  # noqa: B950
                    youtube_video_thumbnail_url=thumbnail_url,
                ) as download_result:
                    content_type = download_result.content_type
                    object_size = download_result.size
                    object_key = str(uuid4())

                    await youtube_video_thumbnail_uploader.upload_youtube_video_thumbnail(
                        object_key=object_key,
                        content_type=content_type,
                        binaryio=download_result.binaryio,
                    )

                    await youtube_video_thumbnail_object_creator.create_youtube_video_thumbnail_object(  # noqa: B950
                        remote_youtube_video_thumbnail_url=thumbnail_url,
                        object_key=object_key,
                        sha256_digest=download_result.sha256_digest,
                        object_size=object_size,
                        content_type=content_type,
                        fetched_at=fetched_at_aware,
                    )
            except (
                YoutubeVideoThumbnailDownloadError,
                YoutubeVideoThumbnailUploadError,
                YoutubeVideoThumbnailObjectCreateError,
            ) as err:
                exceptions.append(err)

        if len(exceptions) > 0:
            raise ExceptionGroup(
                "Some errors occured.",
                exceptions,
            )

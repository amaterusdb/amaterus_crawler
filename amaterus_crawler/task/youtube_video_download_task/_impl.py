from datetime import datetime, timezone
from uuid import uuid4

from ..base import AmaterusCrawlerTask
from .utility.downloadable_youtube_video_fetcher import DownloadableYoutubeVideoFetcher
from .utility.youtube_video_downloader import (
    YoutubeVideoDownloader,
    YoutubeVideoDownloadError,
)
from .utility.youtube_video_object_creator import (
    YoutubeVideoObjectCreateError,
    YoutubeVideoObjectCreator,
)
from .utility.youtube_video_uploader import (
    YoutubeVideoUploader,
    YoutubeVideoUploadError,
)


class YoutubeVideoDownloadTask(AmaterusCrawlerTask):
    def __init__(
        self,
        downloadable_youtube_video_fetcher: DownloadableYoutubeVideoFetcher,
        youtube_video_downloader: YoutubeVideoDownloader,
        youtube_video_uploader: YoutubeVideoUploader,
        youtube_video_object_creator: YoutubeVideoObjectCreator,
    ):
        self.downloadable_youtube_video_fetcher = downloadable_youtube_video_fetcher
        self.youtube_video_downloader = youtube_video_downloader
        self.youtube_video_uploader = youtube_video_uploader
        self.youtube_video_object_creator = youtube_video_object_creator

    async def run(self) -> None:
        downloadable_youtube_video_fetcher = self.downloadable_youtube_video_fetcher
        youtube_video_downloader = self.youtube_video_downloader
        youtube_video_uploader = self.youtube_video_uploader
        youtube_video_object_creator = self.youtube_video_object_creator

        fetched_at_aware = datetime.now(tz=timezone.utc)

        youtube_video_fetch_result = (
            await downloadable_youtube_video_fetcher.fetch_downloadable_youtube_videos()
        )

        downloadable_youtube_videos = (
            youtube_video_fetch_result.downloadable_youtube_videos
        )

        exceptions: list[
            YoutubeVideoDownloadError
            | YoutubeVideoUploadError
            | YoutubeVideoObjectCreateError
        ] = []
        for downloadable_youtube_video in downloadable_youtube_videos:
            remote_youtube_video_id = downloadable_youtube_video.remote_youtube_video_id

            try:
                async with youtube_video_downloader.download_youtube_video(
                    remote_youtube_video_id=remote_youtube_video_id,
                ) as download_result:
                    content_type = download_result.content_type
                    object_size = download_result.size
                    object_key = str(uuid4())

                    await youtube_video_uploader.upload_youtube_video(
                        object_key=object_key,
                        content_type=content_type,
                        binaryio=download_result.binaryio,
                    )

                    await youtube_video_object_creator.create_youtube_video_object(
                        remote_youtube_video_id=remote_youtube_video_id,
                        object_key=object_key,
                        sha256_digest=download_result.sha256_digest,
                        object_size=object_size,
                        content_type=content_type,
                        fetched_at=fetched_at_aware,
                    )
            except (
                YoutubeVideoDownloadError,
                YoutubeVideoUploadError,
                YoutubeVideoObjectCreateError,
            ) as err:
                exceptions.append(err)

        if len(exceptions) > 0:
            raise ExceptionGroup(
                "Some errors occured.",
                exceptions,
            )

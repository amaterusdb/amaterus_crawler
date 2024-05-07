from datetime import datetime, timezone
from uuid import uuid4

from ..base import AmaterusCrawlerTask
from .utility.downloadable_youtube_channel_icon_fetcher import (
    DownloadableYoutubeChannelIconFetcher,
)
from .utility.youtube_channel_icon_downloader import (
    YoutubeChannelIconDownloader,
    YoutubeChannelIconDownloadError,
)
from .utility.youtube_channel_icon_updater import (
    YoutubeChannelIconUpdateError,
    YoutubeChannelIconUpdateQuery,
    YoutubeChannelIconUpdater,
)
from .utility.youtube_channel_icon_uploader import (
    YoutubeChannelIconUploader,
    YoutubeChannelIconUploadError,
)


class YoutubeChannelIconDownloadTask(AmaterusCrawlerTask):
    def __init__(
        self,
        downloadable_youtube_channel_icon_fetcher: DownloadableYoutubeChannelIconFetcher,
        youtube_channel_icon_downloader: YoutubeChannelIconDownloader,
        youtube_channel_icon_uploader: YoutubeChannelIconUploader,
        youtube_channel_icon_updater: YoutubeChannelIconUpdater,
    ):
        self.downloadable_youtube_channel_icon_fetcher = (
            downloadable_youtube_channel_icon_fetcher
        )
        self.youtube_channel_icon_downloader = youtube_channel_icon_downloader
        self.youtube_channel_icon_uploader = youtube_channel_icon_uploader
        self.youtube_channel_icon_updater = youtube_channel_icon_updater

    async def run(self) -> None:
        downloadable_youtube_channel_icon_fetcher = (
            self.downloadable_youtube_channel_icon_fetcher
        )
        youtube_channel_icon_downloader = self.youtube_channel_icon_downloader
        youtube_channel_icon_uploader = self.youtube_channel_icon_uploader
        youtube_channel_icon_updater = self.youtube_channel_icon_updater

        now = datetime.now(tz=timezone.utc)

        youtube_channel_icon_fetch_result = (
            await downloadable_youtube_channel_icon_fetcher.fetch_downloadable_youtube_channel_icons()  # noqa: B950
        )

        downloadable_youtube_channel_icons = (
            youtube_channel_icon_fetch_result.downloadable_youtube_channel_icons
        )

        # storage__youtube_channel_icons のレコードを事前作成
        pre_update_queries: list[YoutubeChannelIconUpdateQuery] = []
        for downloadable_youtube_channel_icon in downloadable_youtube_channel_icons:
            remote_youtube_channel_id = (
                downloadable_youtube_channel_icon.remote_youtube_channel_id
            )
            remote_icon_url = downloadable_youtube_channel_icon.remote_icon_url

            pre_update_queries.append(
                YoutubeChannelIconUpdateQuery(
                    remote_youtube_channel_id=remote_youtube_channel_id,
                    remote_icon_url=remote_icon_url,
                )
            )
        await youtube_channel_icon_updater.update_youtube_channel_icons(
            update_queries=pre_update_queries,
        )

        exceptions: list[
            YoutubeChannelIconDownloadError
            | YoutubeChannelIconUploadError
            | YoutubeChannelIconUpdateError
        ] = []
        for downloadable_youtube_channel_icon in downloadable_youtube_channel_icons:
            remote_youtube_channel_id = (
                downloadable_youtube_channel_icon.remote_youtube_channel_id
            )
            remote_icon_url = downloadable_youtube_channel_icon.remote_icon_url

            try:
                async with (
                    youtube_channel_icon_downloader.download_youtube_channel_icon(
                        youtube_channel_icon_url=remote_icon_url,
                    ) as download_result
                ):
                    content_type = download_result.content_type
                    object_key = str(uuid4())

                    await youtube_channel_icon_uploader.upload_youtube_channel_icon(
                        object_key=object_key,
                        content_type=content_type,
                        binaryio=download_result.binaryio,
                    )

                    remote_youtube_channel_id = (
                        downloadable_youtube_channel_icon.remote_youtube_channel_id
                    )

                    await youtube_channel_icon_updater.update_youtube_channel_icons(
                        update_queries=[
                            YoutubeChannelIconUpdateQuery(
                                remote_youtube_channel_id=remote_youtube_channel_id,
                                remote_icon_url=remote_icon_url,
                                is_downloaded=True,
                                downloaded_at=now,
                                object_key=object_key,
                                object_sha256_digest=download_result.sha256_digest,
                            ),
                        ],
                    )
            except (
                YoutubeChannelIconDownloadError,
                YoutubeChannelIconUploadError,
                YoutubeChannelIconUpdateError,
            ) as err:
                exceptions.append(err)

        if len(exceptions) > 0:
            raise ExceptionGroup(
                "Some errors occured.",
                exceptions,
            )

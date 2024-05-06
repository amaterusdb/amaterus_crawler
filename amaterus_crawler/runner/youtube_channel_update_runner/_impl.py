from ..base import Runner
from .utility.remote_youtube_channel_fetcher import RemoteYoutubeChannelFetcher
from .utility.youtube_channel_fetcher import UpdatableYoutubeChannelFetcher
from .utility.youtube_channel_updater import (
    YoutubeChannelUpdateQuery,
    YoutubeChannelUpdater,
)


class YoutubeChannelUpdateRunner(Runner):
    def __init__(
        self,
        updatable_youtube_channel_fetcher: UpdatableYoutubeChannelFetcher,
        remote_youtube_channel_fetcher: RemoteYoutubeChannelFetcher,
        youtube_channel_updater: YoutubeChannelUpdater,
    ):
        self.updatable_youtube_channel_fetcher = updatable_youtube_channel_fetcher
        self.remote_youtube_channel_fetcher = remote_youtube_channel_fetcher
        self.youtube_channel_updater = youtube_channel_updater

    async def run(self) -> None:
        updatable_youtube_channel_fetcher = self.updatable_youtube_channel_fetcher
        remote_youtube_channel_fetcher = self.remote_youtube_channel_fetcher
        youtube_channel_updater = self.youtube_channel_updater

        youtube_channel_fetch_result = (
            await updatable_youtube_channel_fetcher.fetch_updatable_youtube_channels()
        )

        target_remote_youtube_channel_ids: list[str] = []
        for youtube_channel in youtube_channel_fetch_result.updatable_youtube_channels:
            target_remote_youtube_channel_ids.append(
                youtube_channel.remote_youtube_channel_id
            )

        remote_youtube_channel_fetch_result = (
            await remote_youtube_channel_fetcher.fetch_remote_youtube_channels(
                remote_youtube_channel_ids=target_remote_youtube_channel_ids,
            )
        )
        remote_youtube_channels = (
            remote_youtube_channel_fetch_result.remote_youtube_channels
        )

        update_queries: list[YoutubeChannelUpdateQuery] = []
        for remote_youtube_channel in remote_youtube_channels:
            update_queries.append(
                YoutubeChannelUpdateQuery(
                    remote_youtube_channel_id=remote_youtube_channel.channel_id,
                    name=remote_youtube_channel.title,
                    icon_url=remote_youtube_channel.icon_url,
                    youtube_channel_handle=remote_youtube_channel.screen_name,
                ),
            )

        await youtube_channel_updater.update_youtube_channels(
            update_queries=update_queries,
        )

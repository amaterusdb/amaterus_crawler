from datetime import timezone
from logging import getLogger

from .....graphql_client import Client, GraphQLClientError, youtube_videos_insert_input
from .base import YoutubeVideoUpserter, YoutubeVideoUpsertError, YoutubeVideoUpsertQuery

logger = getLogger(__name__)


class YoutubeVideoUpserterHasura(YoutubeVideoUpserter):
    def __init__(
        self,
        graphql_client: Client,
    ):
        self.graphql_client = graphql_client

    async def upsert_youtube_videos(
        self,
        upsert_queries: list[YoutubeVideoUpsertQuery],
    ) -> None:
        graphql_client = self.graphql_client

        objects: list[youtube_videos_insert_input] = []
        for upsert_query in upsert_queries:
            # 送信時点でタイムゾーン付きであることを保証する
            fetched_at_aware_string = upsert_query.fetched_at.astimezone(
                tz=timezone.utc
            ).isoformat()

            objects.append(
                youtube_videos_insert_input(
                    remote_youtube_video_id=upsert_query.remote_youtube_video_id,
                    last_fetched_at=fetched_at_aware_string,
                ),
            )

        try:
            await graphql_client.upsert_youtube_videos(
                objects=objects,
            )
        except GraphQLClientError:
            raise YoutubeVideoUpsertError("Failed to upsert youtube channel videos.")

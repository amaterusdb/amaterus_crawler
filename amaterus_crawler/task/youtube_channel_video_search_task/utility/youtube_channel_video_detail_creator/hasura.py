from datetime import timezone
from logging import getLogger

from .....graphql_client import (
    Client,
    GraphQLClientError,
    youtube_channels_constraint,
    youtube_channels_insert_input,
    youtube_channels_obj_rel_insert_input,
    youtube_channels_on_conflict,
    youtube_channels_update_column,
    youtube_video_detail_logs_arr_rel_insert_input,
    youtube_video_detail_logs_insert_input,
    youtube_video_details_insert_input,
    youtube_videos_constraint,
    youtube_videos_insert_input,
    youtube_videos_obj_rel_insert_input,
    youtube_videos_on_conflict,
    youtube_videos_update_column,
)
from .base import (
    YoutubeVideoDetailCreateError,
    YoutubeVideoDetailCreateQuery,
    YoutubeVideoDetailCreator,
)

logger = getLogger(__name__)


class YoutubeVideoDetailCreatorHasura(YoutubeVideoDetailCreator):
    def __init__(
        self,
        graphql_client: Client,
    ):
        self.graphql_client = graphql_client

    async def create_youtube_video_details(
        self,
        create_queries: list[YoutubeVideoDetailCreateQuery],
    ) -> None:
        graphql_client = self.graphql_client

        objects: list[youtube_video_details_insert_input] = []
        for create_query in create_queries:
            # 送信時点でタイムゾーン付きであることを保証する
            scheduled_start_time = create_query.scheduled_start_time
            scheduled_end_time = create_query.scheduled_end_time
            actual_start_time = create_query.actual_start_time
            actual_end_time = create_query.actual_end_time

            scheduled_start_time_aware_string = (
                scheduled_start_time.astimezone(tz=timezone.utc).isoformat()
                if scheduled_start_time is not None
                else None
            )
            scheduled_end_time_aware_string = (
                scheduled_end_time.astimezone(tz=timezone.utc).isoformat()
                if scheduled_end_time is not None
                else None
            )
            actual_start_time_aware_string = (
                actual_start_time.astimezone(tz=timezone.utc).isoformat()
                if actual_start_time is not None
                else None
            )
            actual_end_time_aware_string = (
                actual_end_time.astimezone(tz=timezone.utc).isoformat()
                if actual_end_time is not None
                else None
            )

            fetched_at_aware_string = create_query.fetched_at.astimezone(
                tz=timezone.utc
            ).isoformat()

            objects.append(
                youtube_video_details_insert_input(
                    youtube_channel=youtube_channels_obj_rel_insert_input(
                        data=youtube_channels_insert_input(
                            remote_youtube_channel_id=create_query.remote_youtube_channel_id,
                            last_fetched_at=fetched_at_aware_string,
                        ),
                        on_conflict=youtube_channels_on_conflict(
                            constraint=youtube_channels_constraint.youtube_channels_remote_youtube_channel_id_key,
                            update_columns=[
                                youtube_channels_update_column.last_fetched_at,
                            ],
                        ),
                    ),
                    youtube_video=youtube_videos_obj_rel_insert_input(
                        data=youtube_videos_insert_input(
                            remote_youtube_video_id=create_query.remote_youtube_video_id,
                            last_fetched_at=fetched_at_aware_string,
                        ),
                        on_conflict=youtube_videos_on_conflict(
                            constraint=youtube_videos_constraint.youtube_videos_remote_youtube_video_id_key,
                            update_columns=[
                                youtube_videos_update_column.last_fetched_at,
                            ],
                        ),
                    ),
                    title=create_query.title,
                    description=create_query.description,
                    published_at=create_query.published_at,
                    privacy_status=create_query.privacy_status,
                    upload_status=create_query.upload_status,
                    live_broadcast_content=create_query.live_broadcast_content,
                    has_live_streaming_details=create_query.has_live_streaming_details,
                    scheduled_start_time=scheduled_start_time_aware_string,
                    scheduled_end_time=scheduled_end_time_aware_string,
                    actual_start_time=actual_start_time_aware_string,
                    actual_end_time=actual_end_time_aware_string,
                    last_fetched_at=fetched_at_aware_string,
                    youtube_video_detail_logs=youtube_video_detail_logs_arr_rel_insert_input(
                        data=[
                            youtube_video_detail_logs_insert_input(
                                fetched_at=fetched_at_aware_string,
                            ),
                        ],
                    ),
                ),
            )

        try:
            await graphql_client.create_youtube_video_details(
                objects=objects,
            )
        except GraphQLClientError:
            raise YoutubeVideoDetailCreateError(
                "Failed to create a youtube channel detail."
            )

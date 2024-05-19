from datetime import timezone
from logging import getLogger

from pydantic import BaseModel, Field

from .....graphql_client import (
    Client,
    GraphQLClientError,
    youtube_channel_detail_logs_arr_rel_insert_input,
    youtube_channel_detail_logs_insert_input,
    youtube_channel_detail_thumbnails_arr_rel_insert_input,
    youtube_channel_detail_thumbnails_constraint,
    youtube_channel_detail_thumbnails_insert_input,
    youtube_channel_detail_thumbnails_on_conflict,
    youtube_channel_detail_thumbnails_update_column,
    youtube_channel_details_arr_rel_insert_input,
    youtube_channel_details_constraint,
    youtube_channel_details_insert_input,
    youtube_channel_details_on_conflict,
    youtube_channel_details_update_column,
    youtube_channel_thumbnails_constraint,
    youtube_channel_thumbnails_insert_input,
    youtube_channel_thumbnails_obj_rel_insert_input,
    youtube_channel_thumbnails_on_conflict,
    youtube_channel_thumbnails_update_column,
    youtube_channels_constraint,
    youtube_channels_insert_input,
    youtube_channels_obj_rel_insert_input,
    youtube_channels_on_conflict,
    youtube_channels_update_column,
)
from .base import (
    YoutubeChannelUpdateError,
    YoutubeChannelUpdateQuery,
    YoutubeChannelUpdater,
)

logger = getLogger(__name__)


class CrawlerYoutubeChannelConfigInsertInput(BaseModel):
    auto_updated_at: str | None


class CrawlerYoutubeChannelConfigObjRelInsertInputOnConflict(BaseModel):
    constraint: str = "crawler__youtube_channel_configs_remote_youtube_channel_id_key"
    update_columns: list[str] = Field(default_factory=lambda: ["auto_updated_at"])


class CrawlerYoutubeChannelConfigObjRelInsertInput(BaseModel):
    data: CrawlerYoutubeChannelConfigInsertInput
    on_conflict: CrawlerYoutubeChannelConfigObjRelInsertInputOnConflict = Field(
        default_factory=(
            lambda: CrawlerYoutubeChannelConfigObjRelInsertInputOnConflict()
        )
    )


class YoutubeChannelsInsertInput(BaseModel):
    remote_youtube_channel_id: str
    name: str
    icon_url: str | None
    youtube_channel_handle: str | None
    crawler__youtube_channel_config: CrawlerYoutubeChannelConfigObjRelInsertInput


class UpsertYouTubeChannelsResponseBodyDataInsertYoutubeChannels(BaseModel):
    affected_rows: int


class UpsertYouTubeChannelsResponseBodyData(BaseModel):
    insert_youtube_channels: UpsertYouTubeChannelsResponseBodyDataInsertYoutubeChannels


class UpsertYouTubeChannelsResponseBodyError(BaseModel):
    message: str


class UpsertYouTubeChannelsResponseBody(BaseModel):
    data: UpsertYouTubeChannelsResponseBodyData | None = None
    errors: list[UpsertYouTubeChannelsResponseBodyError] | None = None


class YoutubeChannelUpdaterHasura(YoutubeChannelUpdater):
    def __init__(
        self,
        graphql_client: Client,
    ):
        self.graphql_client = graphql_client

    async def update_youtube_channels(
        self,
        update_queries: list[YoutubeChannelUpdateQuery],
    ) -> None:
        graphql_client = self.graphql_client

        objects: list[youtube_channels_insert_input] = []
        for update_query in update_queries:
            # 送信時点でタイムゾーン付きであることを保証する
            fetched_at_aware = update_query.fetched_at.astimezone(tz=timezone.utc)
            published_at_aware = update_query.published_at.astimezone(tz=timezone.utc)

            detail_thumbnail_objects: list[
                youtube_channel_detail_thumbnails_insert_input
            ] = []
            for thumbnail in update_query.thumbnails:
                detail_thumbnail_objects.append(
                    youtube_channel_detail_thumbnails_insert_input(
                        youtube_channel_thumbnail=youtube_channel_thumbnails_obj_rel_insert_input(
                            data=youtube_channel_thumbnails_insert_input(
                                last_fetched_at=fetched_at_aware.isoformat(),
                                youtube_channel=youtube_channels_obj_rel_insert_input(
                                    data=youtube_channels_insert_input(
                                        remote_youtube_channel_id=update_query.remote_youtube_channel_id,
                                        last_fetched_at=fetched_at_aware.isoformat(),
                                    ),
                                    on_conflict=youtube_channels_on_conflict(
                                        constraint=youtube_channels_constraint.youtube_channels_remote_youtube_channel_id_key,
                                        update_columns=[
                                            youtube_channels_update_column.last_fetched_at,
                                        ],
                                    ),
                                ),
                                key=thumbnail.key,
                                url=thumbnail.url,
                                width=thumbnail.width,
                                height=thumbnail.height,
                            ),
                            on_conflict=youtube_channel_thumbnails_on_conflict(
                                constraint=youtube_channel_thumbnails_constraint.youtube_channel_thumbnails_key_url_width_height_youtube_channel,
                                update_columns=[
                                    youtube_channel_thumbnails_update_column.last_fetched_at,
                                ],
                            ),
                        ),
                    ),
                )

            objects.append(
                youtube_channels_insert_input(
                    remote_youtube_channel_id=update_query.remote_youtube_channel_id,
                    last_fetched_at=fetched_at_aware.isoformat(),
                    youtube_channel_details=youtube_channel_details_arr_rel_insert_input(
                        data=[
                            youtube_channel_details_insert_input(
                                last_fetched_at=fetched_at_aware.isoformat(),
                                title=update_query.title,
                                description=update_query.description,
                                published_at=published_at_aware.isoformat(),
                                custom_url=update_query.custom_url,
                                youtube_channel_detail_logs=youtube_channel_detail_logs_arr_rel_insert_input(
                                    data=[
                                        youtube_channel_detail_logs_insert_input(
                                            fetched_at=fetched_at_aware.isoformat(),
                                        ),
                                    ],
                                ),
                                youtube_channel_detail_thumbnails=youtube_channel_detail_thumbnails_arr_rel_insert_input(
                                    data=detail_thumbnail_objects,
                                    on_conflict=youtube_channel_detail_thumbnails_on_conflict(
                                        constraint=youtube_channel_detail_thumbnails_constraint.youtube_channel_detail_thumbnails_youtube_channel_detail_id_you,
                                        update_columns=[],
                                    ),
                                ),
                            ),
                        ],
                        on_conflict=youtube_channel_details_on_conflict(
                            constraint=youtube_channel_details_constraint.youtube_channel_details_title_description_published_at_custom_u,
                            update_columns=[
                                youtube_channel_details_update_column.last_fetched_at,
                            ],
                        ),
                    ),
                ),
            )

        try:
            await graphql_client.create_youtube_channel_details(
                objects=objects,
            )
        except GraphQLClientError:
            raise YoutubeChannelUpdateError("Failed to update youtube channel.")

# Generated by ariadne-codegen
# Source: schema.graphql

from enum import Enum


class cursor_ordering(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class order_by(str, Enum):
    asc = "asc"
    asc_nulls_first = "asc_nulls_first"
    asc_nulls_last = "asc_nulls_last"
    desc = "desc"
    desc_nulls_first = "desc_nulls_first"
    desc_nulls_last = "desc_nulls_last"


class youtube_channel_detail_logs_constraint(str, Enum):
    youtube_channel_detail_logs_pkey = "youtube_channel_detail_logs_pkey"


class youtube_channel_detail_logs_select_column(str, Enum):
    created_at = "created_at"
    fetched_at = "fetched_at"
    id = "id"
    updated_at = "updated_at"
    youtube_channel_detail_id = "youtube_channel_detail_id"


class youtube_channel_detail_logs_update_column(str, Enum):
    _PLACEHOLDER = "_PLACEHOLDER"


class youtube_channel_detail_thumbnails_constraint(str, Enum):
    youtube_channel_detail_thumbnails_pkey = "youtube_channel_detail_thumbnails_pkey"
    youtube_channel_detail_thumbnails_youtube_channel_detail_id_you = (
        "youtube_channel_detail_thumbnails_youtube_channel_detail_id_you"
    )


class youtube_channel_detail_thumbnails_select_column(str, Enum):
    created_at = "created_at"
    id = "id"
    updated_at = "updated_at"
    youtube_channel_detail_id = "youtube_channel_detail_id"
    youtube_channel_thumbnail_id = "youtube_channel_thumbnail_id"


class youtube_channel_detail_thumbnails_update_column(str, Enum):
    _PLACEHOLDER = "_PLACEHOLDER"


class youtube_channel_details_constraint(str, Enum):
    youtube_channel_details_pkey = "youtube_channel_details_pkey"
    youtube_channel_details_remote_youtube_channel_id_title_descrip = (
        "youtube_channel_details_remote_youtube_channel_id_title_descrip"
    )


class youtube_channel_details_select_column(str, Enum):
    created_at = "created_at"
    custom_url = "custom_url"
    description = "description"
    id = "id"
    last_fetched_at = "last_fetched_at"
    published_at = "published_at"
    remote_youtube_channel_id = "remote_youtube_channel_id"
    title = "title"
    updated_at = "updated_at"


class youtube_channel_details_update_column(str, Enum):
    last_fetched_at = "last_fetched_at"


class youtube_channel_thumbnail_objects_constraint(str, Enum):
    youtube_channel_thumbnail_objects_pkey = "youtube_channel_thumbnail_objects_pkey"
    youtube_channel_thumbnail_objects_remote_youtube_channel_thumbn = (
        "youtube_channel_thumbnail_objects_remote_youtube_channel_thumbn"
    )


class youtube_channel_thumbnail_objects_select_column(str, Enum):
    content_type = "content_type"
    created_at = "created_at"
    fetched_at = "fetched_at"
    id = "id"
    object_key = "object_key"
    object_size = "object_size"
    remote_youtube_channel_thumbnail_url = "remote_youtube_channel_thumbnail_url"
    sha256_digest = "sha256_digest"
    updated_at = "updated_at"


class youtube_channel_thumbnail_objects_update_column(str, Enum):
    _PLACEHOLDER = "_PLACEHOLDER"


class youtube_channel_thumbnails_constraint(str, Enum):
    youtube_channel_thumbnails_pkey = "youtube_channel_thumbnails_pkey"
    youtube_channel_thumbnails_remote_youtube_channel_id_key_url_wi = (
        "youtube_channel_thumbnails_remote_youtube_channel_id_key_url_wi"
    )


class youtube_channel_thumbnails_select_column(str, Enum):
    created_at = "created_at"
    height = "height"
    id = "id"
    key = "key"
    last_fetched_at = "last_fetched_at"
    remote_youtube_channel_id = "remote_youtube_channel_id"
    updated_at = "updated_at"
    url = "url"
    width = "width"


class youtube_channel_thumbnails_update_column(str, Enum):
    last_fetched_at = "last_fetched_at"


class youtube_channels_constraint(str, Enum):
    youtube_channels_pkey = "youtube_channels_pkey"
    youtube_channels_remote_youtube_channel_id_key = (
        "youtube_channels_remote_youtube_channel_id_key"
    )


class youtube_channels_select_column(str, Enum):
    created_at = "created_at"
    enabled = "enabled"
    id = "id"
    last_fetched_at = "last_fetched_at"
    registered_at = "registered_at"
    remote_youtube_channel_id = "remote_youtube_channel_id"
    updated_at = "updated_at"


class youtube_channels_update_column(str, Enum):
    enabled = "enabled"
    last_fetched_at = "last_fetched_at"
    registered_at = "registered_at"


class youtube_video_detail_logs_constraint(str, Enum):
    youtube_video_detail_logs_pkey = "youtube_video_detail_logs_pkey"


class youtube_video_detail_logs_select_column(str, Enum):
    created_at = "created_at"
    fetched_at = "fetched_at"
    id = "id"
    updated_at = "updated_at"
    youtube_video_detail_id = "youtube_video_detail_id"


class youtube_video_detail_logs_update_column(str, Enum):
    _PLACEHOLDER = "_PLACEHOLDER"


class youtube_video_details_constraint(str, Enum):
    youtube_video_details_pkey = "youtube_video_details_pkey"
    youtube_video_details_values_key = "youtube_video_details_values_key"


class youtube_video_details_select_column(str, Enum):
    actual_end_time = "actual_end_time"
    actual_start_time = "actual_start_time"
    created_at = "created_at"
    description = "description"
    has_live_streaming_details = "has_live_streaming_details"
    id = "id"
    last_fetched_at = "last_fetched_at"
    live_broadcast_content = "live_broadcast_content"
    privacy_status = "privacy_status"
    published_at = "published_at"
    remote_youtube_channel_id = "remote_youtube_channel_id"
    remote_youtube_video_id = "remote_youtube_video_id"
    scheduled_end_time = "scheduled_end_time"
    scheduled_start_time = "scheduled_start_time"
    title = "title"
    updated_at = "updated_at"
    upload_status = "upload_status"


class youtube_video_details_select_column_youtube_video_details_aggregate_bool_exp_bool_and_arguments_columns(
    str, Enum
):
    has_live_streaming_details = "has_live_streaming_details"


class youtube_video_details_select_column_youtube_video_details_aggregate_bool_exp_bool_or_arguments_columns(
    str, Enum
):
    has_live_streaming_details = "has_live_streaming_details"


class youtube_video_details_update_column(str, Enum):
    last_fetched_at = "last_fetched_at"


class youtube_videos_constraint(str, Enum):
    youtube_videos_pkey = "youtube_videos_pkey"
    youtube_videos_remote_youtube_video_id_key = (
        "youtube_videos_remote_youtube_video_id_key"
    )


class youtube_videos_select_column(str, Enum):
    created_at = "created_at"
    enabled = "enabled"
    id = "id"
    last_fetched_at = "last_fetched_at"
    registered_at = "registered_at"
    remote_youtube_video_id = "remote_youtube_video_id"
    updated_at = "updated_at"


class youtube_videos_update_column(str, Enum):
    last_fetched_at = "last_fetched_at"

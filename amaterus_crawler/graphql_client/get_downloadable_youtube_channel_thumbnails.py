# Generated by ariadne-codegen
# Source: graphql_queries/

from typing import List

from .base_model import BaseModel


class GetDownloadableYoutubeChannelThumbnails(BaseModel):
    youtube_channel_thumbnails: List[
        "GetDownloadableYoutubeChannelThumbnailsYoutubeChannelThumbnails"
    ]


class GetDownloadableYoutubeChannelThumbnailsYoutubeChannelThumbnails(BaseModel):
    url: str
    key: str
    width: int
    height: int
    youtube_channel: (
        "GetDownloadableYoutubeChannelThumbnailsYoutubeChannelThumbnailsYoutubeChannel"
    )


class GetDownloadableYoutubeChannelThumbnailsYoutubeChannelThumbnailsYoutubeChannel(
    BaseModel
):
    remote_youtube_channel_id: str


GetDownloadableYoutubeChannelThumbnails.model_rebuild()
GetDownloadableYoutubeChannelThumbnailsYoutubeChannelThumbnails.model_rebuild()

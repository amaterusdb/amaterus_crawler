# Generated by ariadne-codegen
# Source: graphql_queries/

from typing import Optional

from .base_model import BaseModel


class CreateYoutubeChannelDetails(BaseModel):
    insert_youtube_channel_details: Optional[
        "CreateYoutubeChannelDetailsInsertYoutubeChannelDetails"
    ]


class CreateYoutubeChannelDetailsInsertYoutubeChannelDetails(BaseModel):
    affected_rows: int


CreateYoutubeChannelDetails.model_rebuild()
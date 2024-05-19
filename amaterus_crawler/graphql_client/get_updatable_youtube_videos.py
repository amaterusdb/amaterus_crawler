# Generated by ariadne-codegen
# Source: graphql_queries/

from typing import List

from .base_model import BaseModel


class GetUpdatableYoutubeVideos(BaseModel):
    youtube_videos: List["GetUpdatableYoutubeVideosYoutubeVideos"]


class GetUpdatableYoutubeVideosYoutubeVideos(BaseModel):
    remote_youtube_video_id: str


GetUpdatableYoutubeVideos.model_rebuild()
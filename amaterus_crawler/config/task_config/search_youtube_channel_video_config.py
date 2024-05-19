from typing import Literal

from pydantic import BaseModel


class SearchYoutubeChannelVideoConfigOptions(BaseModel):
    override_hasura: bool = False
    hasura_url: str | None = None
    hasura_access_token: str | None = None
    hasura_admin_secret: str | None = None
    hasura_role: str | None = None

    override_youtube_api_key: bool = False
    youtube_api_key: str | None = None


class SearchYoutubeChannelVideoConfig(BaseModel):
    type: Literal["search_youtube_channel_video"]
    enabled: bool
    options: SearchYoutubeChannelVideoConfigOptions | None = None

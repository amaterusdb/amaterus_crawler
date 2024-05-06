from typing import Annotated, Literal

from pydantic import BaseModel, Field


class UpdateYoutubeChannelConfigOptions(BaseModel):
    override_hasura: bool = False
    hasura_url: str | None = None
    hasura_access_token: str | None = None
    override_youtube_api_key: bool = False
    youtube_api_key: str | None = None


class UpdateYoutubeChannelConfig(BaseModel):
    type: Literal["update_youtube_channel"]
    enabled: bool
    options: Annotated[UpdateYoutubeChannelConfigOptions | None, Field(default=None)]

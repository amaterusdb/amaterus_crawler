from typing import Literal

from pydantic import BaseModel


class UpdateYoutubeVideoDetailConfigOptions(BaseModel):
    override_hasura: bool = False
    hasura_url: str | None = None
    hasura_access_token: str | None = None
    hasura_admin_secret: str | None = None
    hasura_role: str | None = None

    override_youtube_api_key: bool = False
    youtube_api_key: str | None = None


class UpdateYoutubeVideoDetailConfig(BaseModel):
    type: Literal["update_youtube_video_detail"]
    enabled: bool
    options: UpdateYoutubeVideoDetailConfigOptions | None = None

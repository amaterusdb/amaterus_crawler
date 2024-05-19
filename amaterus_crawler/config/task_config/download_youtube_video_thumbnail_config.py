from typing import Literal

from pydantic import BaseModel


class DownloadYoutubeVideoThumbnailConfigOptions(BaseModel):
    override_hasura: bool = False
    hasura_url: str | None = None
    hasura_access_token: str | None = None
    hasura_admin_secret: str | None = None
    hasura_role: str | None = None

    override_s3: bool = False
    s3_endpoint_url: str | None = None
    s3_bucket: str | None = None
    s3_access_key_id: str | None = None
    s3_secret_access_key: str | None = None

    object_key_prefix: str | None = None


class DownloadYoutubeVideoThumbnailConfig(BaseModel):
    type: Literal["download_youtube_video_thumbnail"]
    enabled: bool
    options: DownloadYoutubeVideoThumbnailConfigOptions | None = None

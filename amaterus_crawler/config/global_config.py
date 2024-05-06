from pydantic import BaseModel


class GlobalConfig(BaseModel):
    hasura_url: str | None = None
    hasura_access_token: str | None = None
    hasura_admin_secret: str | None = None
    hasura_role: str | None = None
    youtube_api_key: str | None = None

from pydantic import BaseModel


class ServerConfig(BaseModel):
    host: str | None = None
    port: int | None = None

    override_hasura: bool = False
    hasura_url: str | None = None
    hasura_access_token: str | None = None
    hasura_admin_secret: str | None = None
    hasura_role: str | None = None

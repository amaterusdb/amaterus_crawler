import httpx
from pydantic import BaseModel, TypeAdapter

from .base import (
    YoutubeChannelUpdateError,
    YoutubeChannelUpdateQuery,
    YoutubeChannelUpdater,
)


class YoutubeChannelsInsertInput(BaseModel):
    remote_youtube_channel_id: str
    name: str
    icon_url: str | None
    youtube_channel_handle: str | None


class YoutubeChannelUpdaterHasura(YoutubeChannelUpdater):
    def __init__(
        self,
        hasura_url: str,
        hasura_access_token: str | None = None,
        hasura_admin_secret: str | None = None,
        hasura_role: str | None = None,
    ):
        self.hasura_url = hasura_url
        self.hasura_access_token = hasura_access_token
        self.hasura_admin_secret = hasura_admin_secret
        self.hasura_role = hasura_role

    async def update_youtube_channels(
        self,
        update_queries: list[YoutubeChannelUpdateQuery],
    ) -> None:
        hasura_url = self.hasura_url
        hasura_access_token = self.hasura_access_token
        hasura_admin_secret = self.hasura_admin_secret
        hasura_role = self.hasura_role

        hasura_graphql_api_url = hasura_url
        if not hasura_graphql_api_url.endswith("/"):
            hasura_graphql_api_url += "/"
        hasura_graphql_api_url += "v1/graphql"

        headers = {}
        if hasura_access_token is not None:
            headers.update(
                {
                    "Authorization": f"Bearer {hasura_access_token}",
                }
            )
        if hasura_admin_secret is not None:
            headers.update(
                {
                    "X-Hasura-Admin-Secret": hasura_admin_secret,
                }
            )
        if hasura_role is not None:
            headers.update(
                {
                    "X-Hasura-Role": hasura_role,
                }
            )

        objects: list[YoutubeChannelsInsertInput] = []
        for update_query in update_queries:
            objects.append(
                YoutubeChannelsInsertInput(
                    remote_youtube_channel_id=update_query.remote_youtube_channel_id,
                    name=update_query.name,
                    icon_url=update_query.icon_url,
                    youtube_channel_handle=update_query.youtube_channel_handle,
                ),
            )

        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(
                    url=hasura_graphql_api_url,
                    headers=headers,
                    json={
                        "query": """
mutation UpsertYoutubeChannels {
  insert_youtube_channels(
    objects: $objects
    on_conflict: {
      constraint: youtube_channels_youtube_channel_id_key
      update_columns: [
        name
        icon_url
        youtube_channel_handle
      ]
    }
  ) {
    affected_rows
  }
}
""",
                        "variables": {
                            "objects": TypeAdapter(
                                list[YoutubeChannelsInsertInput]
                            ).dump_python(objects),
                        },
                    },
                )

                res.raise_for_status()
        except httpx.HTTPError:
            raise YoutubeChannelUpdateError("Failed to update youtube channel infos.")

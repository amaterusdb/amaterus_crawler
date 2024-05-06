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
        access_token: str,
    ):
        self.hasura_url = hasura_url
        self.access_token = access_token

    async def update_youtube_channels(
        self,
        update_queries: list[YoutubeChannelUpdateQuery],
    ) -> None:
        hasura_url = self.hasura_url
        access_token = self.access_token

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
                    url=hasura_url,
                    headers={
                        "Authorization": f"Bearer {access_token}",
                    },
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
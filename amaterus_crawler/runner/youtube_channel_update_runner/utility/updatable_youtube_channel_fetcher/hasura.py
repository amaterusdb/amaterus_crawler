import httpx
from pydantic import BaseModel

from .base import (
    UpdatableYoutubeChannel,
    UpdatableYoutubeChannelFetcher,
    UpdatableYoutubeChannelFetchError,
    UpdatableYoutubeChannelFetchResult,
)


class GetYoutubeChannelInfosResponseBodyDataYoutubeChannel(BaseModel):
    remote_youtube_channel_id: str
    name: str


class GetYoutubeChannelInfosResponseBodyData(BaseModel):
    youtube_channels: list[GetYoutubeChannelInfosResponseBodyDataYoutubeChannel]


class GetYoutubeChannelInfosResponseBody(BaseModel):
    data: GetYoutubeChannelInfosResponseBodyData


class UpdatableYoutubeChannelFetcherHasura(UpdatableYoutubeChannelFetcher):
    def __init__(
        self,
        hasura_url: str,
        hasura_access_token: str,
    ):
        self.hasura_url = hasura_url
        self.hasura_access_token = hasura_access_token

    async def fetch_updatable_youtube_channels(
        self,
    ) -> UpdatableYoutubeChannelFetchResult:
        hasura_url = self.hasura_url
        hasura_access_token = self.hasura_access_token

        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(
                    url=hasura_url,
                    headers={
                        "Authorization": f"Bearer {hasura_access_token}",
                    },
                    json={
                        "query": """
query GetYoutubeChannelIds {
  youtube_channels(
    where: {
      auto_update_enabled: {
        _eq: true
      }
    }
    order_by: {
      auto_updated_at: asc_nulls_first
    }
  ) {
    id
    name
  }
}
""",
                    },
                )

                res.raise_for_status()
        except httpx.HTTPError:
            raise UpdatableYoutubeChannelFetchError(
                "Failed to fetch youtube channel ids."
            )

        response = GetYoutubeChannelInfosResponseBody.model_validate(res.json())
        youtube_channels = response.data.youtube_channels

        updatable_youtube_channels: list[UpdatableYoutubeChannel] = []
        for youtube_channel in youtube_channels:
            updatable_youtube_channels.append(
                UpdatableYoutubeChannel(
                    remote_youtube_channel_id=youtube_channel.remote_youtube_channel_id,
                    name=youtube_channel.name,
                )
            )

        return UpdatableYoutubeChannelFetchResult(
            updatable_youtube_channels=updatable_youtube_channels,
        )

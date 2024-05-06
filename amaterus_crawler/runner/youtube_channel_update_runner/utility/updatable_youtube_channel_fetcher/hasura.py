from logging import getLogger

import httpx
from pydantic import BaseModel

from .base import (
    UpdatableYoutubeChannel,
    UpdatableYoutubeChannelFetcher,
    UpdatableYoutubeChannelFetchError,
    UpdatableYoutubeChannelFetchResult,
)

logger = getLogger(__name__)


class GetYoutubeChannelInfosResponseBodyDataYoutubeChannel(BaseModel):
    remote_youtube_channel_id: str
    name: str


class GetYoutubeChannelInfosResponseBodyData(BaseModel):
    youtube_channels: list[GetYoutubeChannelInfosResponseBodyDataYoutubeChannel]


class GetYoutubeChannelInfosResponseBodyError(BaseModel):
    message: str


class GetYoutubeChannelInfosResponseBody(BaseModel):
    data: GetYoutubeChannelInfosResponseBodyData
    errors: list[GetYoutubeChannelInfosResponseBodyError] | None = None


class UpdatableYoutubeChannelFetcherHasura(UpdatableYoutubeChannelFetcher):
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

    async def fetch_updatable_youtube_channels(
        self,
    ) -> UpdatableYoutubeChannelFetchResult:
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

        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(
                    url=hasura_graphql_api_url,
                    headers=headers,
                    json={
                        "query": """
query GetUpdatableYoutubeChannels {
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
    remote_youtube_channel_id
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

        response_body = GetYoutubeChannelInfosResponseBody.model_validate(res.json())
        if response_body.errors is not None and len(response_body.errors) > 0:
            logger.error(f"Hasura response body: {response_body.model_dump_json()}")
            raise UpdatableYoutubeChannelFetchError("Hasura error occured.")

        youtube_channels = response_body.data.youtube_channels

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

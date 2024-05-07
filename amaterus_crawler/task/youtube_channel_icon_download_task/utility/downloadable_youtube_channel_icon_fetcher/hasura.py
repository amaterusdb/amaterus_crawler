from logging import getLogger

import httpx
from pydantic import BaseModel

from .base import (
    DownloadableYoutubeChannelIcon,
    DownloadableYoutubeChannelIconFetcher,
    DownloadableYoutubeChannelIconFetchError,
    DownloadableYoutubeChannelIconFetchResult,
)

logger = getLogger(__name__)


class YoutubeChannel(BaseModel):
    name: str
    icon_url: str | None


class CrawlerYoutubeChannel(BaseModel):
    remote_youtube_channel_id: str
    youtube_channel: YoutubeChannel | None


class GetDownloadableYoutubeChannelIconsResponseBodyData(BaseModel):
    crawler__youtube_channel_configs: list[CrawlerYoutubeChannel]


class GetDownloadableYoutubeChannelIconsResponseBodyError(BaseModel):
    message: str


class GetDownloadableYoutubeChannelIconsResponseBody(BaseModel):
    data: GetDownloadableYoutubeChannelIconsResponseBodyData | None = None
    errors: list[GetDownloadableYoutubeChannelIconsResponseBodyError] | None = None


class DownloadableYoutubeChannelIconFetcherHasura(
    DownloadableYoutubeChannelIconFetcher
):
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

    async def fetch_downloadable_youtube_channel_icons(
        self,
    ) -> DownloadableYoutubeChannelIconFetchResult:
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
query GetDownloadableYoutubeChannelIcons {
  crawler__youtube_channel_configs(
    where: {
      auto_update_enabled: {
        _eq: true
      }
      youtube_channel: {
        # storage__youtube_channel_icon が null、または is_downloaded が false
        _not: {
          storage__youtube_channel_icon: {
            is_downloaded: {
              _eq: true
            }
          }
        }
      }
    }
  ) {
    remote_youtube_channel_id
    youtube_channel {
      name
      icon_url
    }
  }
}
""",
                    },
                )

                res.raise_for_status()
        except httpx.HTTPError:
            raise DownloadableYoutubeChannelIconFetchError(
                "Failed to fetch downloadable youtube channel icons."
            )

        response_body = GetDownloadableYoutubeChannelIconsResponseBody.model_validate(
            res.json()
        )
        if response_body.errors is not None and len(response_body.errors) > 0:
            logger.error(f"Hasura response body: {response_body.model_dump_json()}")
            raise DownloadableYoutubeChannelIconFetchError("Hasura error occured.")

        if response_body.data is None:
            logger.error(f"Hasura response body: {response_body.model_dump_json()}")
            raise DownloadableYoutubeChannelIconFetchError("Hasura error occured.")

        crawler_youtube_channels = response_body.data.crawler__youtube_channel_configs

        downloadable_youtube_channel_icons: list[DownloadableYoutubeChannelIcon] = []
        for crawler_youtube_channel in crawler_youtube_channels:
            youtube_channel = crawler_youtube_channel.youtube_channel
            if youtube_channel is None:
                # チャンネルが未取得
                continue

            icon_url = youtube_channel.icon_url
            if icon_url is None:
                # アイコンURLが未取得
                continue

            youtube_channel_name = youtube_channel.name

            downloadable_youtube_channel_icons.append(
                DownloadableYoutubeChannelIcon(
                    remote_youtube_channel_id=crawler_youtube_channel.remote_youtube_channel_id,
                    remote_icon_url=icon_url,
                    youtube_channel_name=youtube_channel_name,
                )
            )

        # TODO: is_downloaded=false の storage__youtube_channel_icons を追加

        return DownloadableYoutubeChannelIconFetchResult(
            downloadable_youtube_channel_icons=downloadable_youtube_channel_icons,
        )

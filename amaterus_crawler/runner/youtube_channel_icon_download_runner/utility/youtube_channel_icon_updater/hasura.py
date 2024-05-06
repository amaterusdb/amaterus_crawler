from datetime import timezone
from logging import getLogger

import httpx
from pydantic import BaseModel, TypeAdapter

from .base import (
    YoutubeChannelIconUpdateError,
    YoutubeChannelIconUpdateQuery,
    YoutubeChannelIconUpdater,
)

logger = getLogger(__name__)


class StorageYoutubeChannelIconInsertInput(BaseModel):
    remote_youtube_channel_id: str
    remote_icon_url: str
    is_downloaded: bool
    downloaded_at: str | None
    object_key: str | None
    object_sha256_digest: str | None


class CrawlerYoutubeChannelIconsInsertInput(BaseModel):
    remote_youtube_channel_id: str
    auto_downloaded_at: str | None


class UpsertYouTubeChannelsResponseBodyDataInsertCrawlerYoutubeChannels(BaseModel):
    affected_rows: int


class UpsertYouTubeChannelsResponseBodyDataInsertStorageYoutubeChannelIcons(BaseModel):
    affected_rows: int


class UpsertYouTubeChannelsResponseBodyData(BaseModel):
    insert_crawler__youtube_channel_icon_download_runner__youtube_channels: (
        UpsertYouTubeChannelsResponseBodyDataInsertCrawlerYoutubeChannels
    )
    insert_storage__youtube_channel_icons: (
        UpsertYouTubeChannelsResponseBodyDataInsertStorageYoutubeChannelIcons
    )


class UpsertYouTubeChannelsResponseBodyError(BaseModel):
    message: str


class UpsertYouTubeChannelsResponseBody(BaseModel):
    data: UpsertYouTubeChannelsResponseBodyData | None = None
    errors: list[UpsertYouTubeChannelsResponseBodyError] | None = None


class YoutubeChannelIconUpdaterHasura(YoutubeChannelIconUpdater):
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

    async def update_youtube_channel_icons(
        self,
        update_queries: list[YoutubeChannelIconUpdateQuery],
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

        crawler_youtube_channel_objects: list[CrawlerYoutubeChannelIconsInsertInput] = (
            []
        )
        storage_youtube_channel_icon_objects: list[
            StorageYoutubeChannelIconInsertInput
        ] = []
        for update_query in update_queries:
            # 送信時点でタイムゾーン付きであることを保証する
            downloaded_at_string: str | None = None
            if update_query.downloaded_at is not None:
                downloaded_at_aware = update_query.downloaded_at.astimezone(
                    tz=timezone.utc
                )
                downloaded_at_string = downloaded_at_aware.isoformat()

            crawler_youtube_channel_objects.append(
                CrawlerYoutubeChannelIconsInsertInput(
                    remote_youtube_channel_id=update_query.remote_youtube_channel_id,
                    auto_downloaded_at=downloaded_at_string,
                ),
            )
            storage_youtube_channel_icon_objects.append(
                StorageYoutubeChannelIconInsertInput(
                    remote_youtube_channel_id=update_query.remote_youtube_channel_id,
                    remote_icon_url=update_query.remote_icon_url,
                    is_downloaded=update_query.is_downloaded,
                    downloaded_at=downloaded_at_string,
                    object_key=update_query.object_key,
                    object_sha256_digest=update_query.object_sha256_digest,
                )
            )

        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(
                    url=hasura_graphql_api_url,
                    headers=headers,
                    json={
                        "query": """  # noqa: B950
mutation UpsertYoutubeChannelIcons(
  $crawler_youtube_channel_objects: [crawler__youtube_channel_icon_download_runner__youtube_channels_insert_input!]!
  $storage_youtube_channel_icon_objects: [storage__youtube_channel_icons_insert_input!]!
) {
  insert_crawler__youtube_channel_icon_download_runner__youtube_channels(
    objects: $crawler_youtube_channel_objects
    on_conflict: {
      constraint: crawler__youtube_channel_icon_dow_remote_youtube_channel_id_key
      update_columns: [
        auto_downloaded_at
      ]
    }
  ) {
    affected_rows
  }

  insert_storage__youtube_channel_icons(
    objects: $storage_youtube_channel_icon_objects
    on_conflict: {
      constraint: storage__youtube_channel_icons_remote_youtube_channel_id_remote
      update_columns: [
        is_downloaded
        downloaded_at
        object_key
        object_sha256_digest
      ]
    }
  ) {
    affected_rows
  }
}
""",
                        "variables": {
                            "crawler_youtube_channel_objects": TypeAdapter(
                                list[CrawlerYoutubeChannelIconsInsertInput]
                            ).dump_python(crawler_youtube_channel_objects),
                            "storage_youtube_channel_icon_objects": TypeAdapter(
                                list[StorageYoutubeChannelIconInsertInput]
                            ).dump_python(storage_youtube_channel_icon_objects),
                        },
                    },
                )

                res.raise_for_status()
        except httpx.HTTPError:
            raise YoutubeChannelIconUpdateError(
                "Failed to update youtube channel icons."
            )

        response_body = UpsertYouTubeChannelsResponseBody.model_validate(res.json())
        if response_body.errors is not None and len(response_body.errors) > 0:
            logger.error(f"Hasura response body: {response_body.model_dump_json()}")
            raise YoutubeChannelIconUpdateError("Hasura error occured.")

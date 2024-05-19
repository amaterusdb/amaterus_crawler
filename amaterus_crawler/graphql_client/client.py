# Generated by ariadne-codegen
# Source: graphql_queries/

from typing import Any, Dict, List

from .async_base_client import AsyncBaseClient
from .create_youtube_channel import CreateYoutubeChannel
from .create_youtube_channel_details import CreateYoutubeChannelDetails
from .create_youtube_channel_thumbnail_object import CreateYoutubeChannelThumbnailObject
from .create_youtube_video_details import CreateYoutubeVideoDetails
from .get_downloadable_youtube_channel_thumbnails import (
    GetDownloadableYoutubeChannelThumbnails,
)
from .get_updatable_youtube_channels import GetUpdatableYoutubeChannels
from .input_types import (
    youtube_channel_details_insert_input,
    youtube_video_details_insert_input,
)


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def create_youtube_channel(
        self, remote_youtube_channel_id: str, **kwargs: Any
    ) -> CreateYoutubeChannel:
        query = gql(
            """
            mutation CreateYoutubeChannel($remote_youtube_channel_id: String!) {
              insert_youtube_channels_one(
                object: {remote_youtube_channel_id: $remote_youtube_channel_id}
              ) {
                id
              }
            }
            """
        )
        variables: Dict[str, object] = {
            "remote_youtube_channel_id": remote_youtube_channel_id
        }
        response = await self.execute(
            query=query,
            operation_name="CreateYoutubeChannel",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return CreateYoutubeChannel.model_validate(data)

    async def create_youtube_channel_details(
        self, objects: List[youtube_channel_details_insert_input], **kwargs: Any
    ) -> CreateYoutubeChannelDetails:
        query = gql(
            """
            mutation CreateYoutubeChannelDetails($objects: [youtube_channel_details_insert_input!]!) {
              insert_youtube_channel_details(
                objects: $objects
                on_conflict: {constraint: youtube_channel_details_remote_youtube_channel_id_title_descrip, update_columns: [last_fetched_at]}
              ) {
                affected_rows
              }
            }
            """
        )
        variables: Dict[str, object] = {"objects": objects}
        response = await self.execute(
            query=query,
            operation_name="CreateYoutubeChannelDetails",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return CreateYoutubeChannelDetails.model_validate(data)

    async def create_youtube_channel_thumbnail_object(
        self,
        remote_youtube_channel_thumbnail_url: str,
        fetched_at: Any,
        object_key: str,
        sha_256_digest: str,
        object_size: int,
        content_type: str,
        **kwargs: Any
    ) -> CreateYoutubeChannelThumbnailObject:
        query = gql(
            """
            mutation CreateYoutubeChannelThumbnailObject($remote_youtube_channel_thumbnail_url: String!, $fetched_at: timestamptz!, $object_key: String!, $sha256_digest: String!, $object_size: Int!, $content_type: String!) {
              insert_youtube_channel_thumbnail_objects_one(
                object: {remote_youtube_channel_thumbnail_url: $remote_youtube_channel_thumbnail_url, fetched_at: $fetched_at, object_key: $object_key, sha256_digest: $sha256_digest, object_size: $object_size, content_type: $content_type}
              ) {
                id
              }
            }
            """
        )
        variables: Dict[str, object] = {
            "remote_youtube_channel_thumbnail_url": remote_youtube_channel_thumbnail_url,
            "fetched_at": fetched_at,
            "object_key": object_key,
            "sha256_digest": sha_256_digest,
            "object_size": object_size,
            "content_type": content_type,
        }
        response = await self.execute(
            query=query,
            operation_name="CreateYoutubeChannelThumbnailObject",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return CreateYoutubeChannelThumbnailObject.model_validate(data)

    async def create_youtube_video_details(
        self, objects: List[youtube_video_details_insert_input], **kwargs: Any
    ) -> CreateYoutubeVideoDetails:
        query = gql(
            """
            mutation CreateYoutubeVideoDetails($objects: [youtube_video_details_insert_input!]!) {
              insert_youtube_video_details(
                objects: $objects
                on_conflict: {constraint: youtube_video_details_actual_end_time_remote_youtube_channel_id, update_columns: [last_fetched_at]}
              ) {
                affected_rows
              }
            }
            """
        )
        variables: Dict[str, object] = {"objects": objects}
        response = await self.execute(
            query=query,
            operation_name="CreateYoutubeVideoDetails",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return CreateYoutubeVideoDetails.model_validate(data)

    async def get_downloadable_youtube_channel_thumbnails(
        self, **kwargs: Any
    ) -> GetDownloadableYoutubeChannelThumbnails:
        query = gql(
            """
            query GetDownloadableYoutubeChannelThumbnails {
              youtube_channel_thumbnails(
                where: {youtube_channel: {enabled: {_eq: true}}, _not: {youtube_channel_thumbnail_object: {}}}
              ) {
                url
                key
                width
                height
                youtube_channel {
                  remote_youtube_channel_id
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=query,
            operation_name="GetDownloadableYoutubeChannelThumbnails",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetDownloadableYoutubeChannelThumbnails.model_validate(data)

    async def get_updatable_youtube_channels(
        self, **kwargs: Any
    ) -> GetUpdatableYoutubeChannels:
        query = gql(
            """
            query GetUpdatableYoutubeChannels {
              youtube_channels(
                where: {enabled: {_eq: true}}
                order_by: {last_fetched_at: asc_nulls_first}
                limit: 50
              ) {
                remote_youtube_channel_id
              }
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=query,
            operation_name="GetUpdatableYoutubeChannels",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetUpdatableYoutubeChannels.model_validate(data)

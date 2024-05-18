from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from ....graphql_client import Client, GraphQLClientError
from .model import YoutubeChannelCreateRequestBody, YoutubeChannelCreateResponseBody


def create_youtube_channel_router(
    graphql_client: Client,
) -> APIRouter:
    router = APIRouter()

    @router.post("/youtube_channel/create")
    async def route_youtube_channel_create(
        body: YoutubeChannelCreateRequestBody,
    ) -> YoutubeChannelCreateResponseBody:
        try:
            result = await graphql_client.create_youtube_channel(
                remote_youtube_channel_id=body.remote_youtube_channel_id,
            )
        except GraphQLClientError:
            raise HTTPException(
                status_code=500,
            )

        if result.insert_youtube_channels_one is None:
            raise HTTPException(
                status_code=500,
            )

        return YoutubeChannelCreateResponseBody(
            youtube_channel_id=result.insert_youtube_channels_one.id,
        )

    return router

from pydantic import BaseModel


class YoutubeChannelCreateRequestBody(BaseModel):
    remote_youtube_channel_id: str


class YoutubeChannelCreateResponseBody(BaseModel):
    youtube_channel_id: str

import httpx
from pydantic import BaseModel


class YoutubeApiSearchResultItemSnippet(BaseModel):
    liveBroadcastContent: str


class YoutubeApiSearchResultItemId(BaseModel):
    videoId: str


class YoutubeApiSearchResultItem(BaseModel):
    id: YoutubeApiSearchResultItemId
    snippet: YoutubeApiSearchResultItemSnippet | None = None


class YoutubeApiSearchResult(BaseModel):
    items: list[YoutubeApiSearchResultItem] | None = None


class YoutubeApiSearch:
    def __init__(
        self,
        youtube_api_key: str,
    ):
        self.youtube_api_key = youtube_api_key

    async def list(
        self,
        channel_id: str,
    ) -> YoutubeApiSearchResult:
        youtube_api_key = self.youtube_api_key

        async with httpx.AsyncClient() as client:
            search_response = await client.get(
                "https://www.googleapis.com/youtube/v3/search",
                params={
                    "key": youtube_api_key,
                    "part": "id,snippet",
                    "channelId": channel_id,
                    "type": "video",
                    "order": "date",  # createdAt desc
                    "maxResults": "10",
                },
            )

        search_api_dict = search_response.json()
        return YoutubeApiSearchResult.model_validate(search_api_dict)

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class YoutubeVideoUpsertQuery:
    remote_youtube_video_id: str
    """
    動画ID
    """
    fetched_at: datetime
    """
    クローラによる自動的な情報取得の日時を表すタイムゾーン付き日時
    """


class YoutubeVideoUpsertError(Exception):
    pass


class YoutubeVideoUpserter(ABC):
    @abstractmethod
    async def upsert_youtube_videos(
        self,
        upsert_queries: list[YoutubeVideoUpsertQuery],
    ) -> None: ...

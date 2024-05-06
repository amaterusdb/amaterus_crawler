from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class YoutubeLiveVideoFindResultVideo:
    remote_youtube_video_id: str
    """
    YouTube上の動画ID
    """
    title: str
    """
    動画タイトル
    """

    remote_youtube_channel_id: str
    """
    YouTube上のチャンネルID
    """
    channel_title: str
    """
    チャンネル名
    """

    is_premier_video: bool | None
    """
    プレミア公開かどうか。 None は判別不可
    """
    is_processed: bool
    """
    YouTube側で動画の処理が完了済みかどうか
    """
    is_ended: bool
    """
    配信が終了済みかどうか
    """

    thumbnail_url: str
    """
    サムネイルURL
    """

    actual_start_time: datetime | None
    """
    配信開始時間を表すタイムゾーン付き日時
    """
    actual_end_time: datetime | None
    """
    配信終了時間を表すタイムゾーン付き日時
    """
    scheduled_start_time: datetime | None
    """
    配信開始予定時間を表すタイムゾーン付き日時
    """
    scheduled_end_time: datetime | None
    """
    配信終了予定時間を表すタイムゾーン付き日時
    """


@dataclass
class YoutubeLiveVideoFindResult:
    videos: list[YoutubeLiveVideoFindResultVideo]


class YoutubeLiveVideoFindError(Exception):
    pass


class YoutubeLiveVideoFinder(ABC):
    @abstractmethod
    async def find_videos(self) -> YoutubeLiveVideoFindResult: ...

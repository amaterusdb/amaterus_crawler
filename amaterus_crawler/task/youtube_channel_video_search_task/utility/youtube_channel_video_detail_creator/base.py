from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class YoutubeVideoDetailCreateQueryThumbnail:
    key: str
    """
    サムネイルの種類
    """
    url: str
    """
    サムネイルのURL
    """
    width: int
    """
    サムネイルの幅
    """
    height: int
    """
    サムネイルの高さ
    """


@dataclass
class YoutubeVideoDetailCreateQuery:
    remote_youtube_channel_id: str
    """
    チャンネルID
    """
    remote_youtube_video_id: str
    """
    動画ID
    """
    title: str
    """
    動画のタイトル
    """
    description: str
    """
    動画の説明文
    """
    published_at: datetime
    """
    動画の公開日時
    """
    privacy_status: str
    """
    動画の公開設定
    """
    upload_status: str
    """
    動画のアップロード状態
    """
    live_broadcast_content: str
    """
    配信の状態
    """
    scheduled_start_time: datetime | None
    """
    配信のスケジュールされた開始日時
    """
    scheduled_end_time: datetime | None
    """
    配信のスケジュールされた終了日時
    """
    actual_start_time: datetime | None
    """
    配信の実際の開始日時
    """
    actual_end_time: datetime | None
    """
    配信の実際の終了日時
    """
    thumbnails: list[YoutubeVideoDetailCreateQueryThumbnail]
    """
    動画のサムネイル
    """
    fetched_at: datetime
    """
    クローラによる自動的な情報取得の日時を表すタイムゾーン付き日時
    """


class YoutubeVideoDetailCreateError(Exception):
    pass


class YoutubeVideoDetailCreator(ABC):
    @abstractmethod
    async def create_youtube_video_details(
        self,
        create_queries: list[YoutubeVideoDetailCreateQuery],
    ) -> None: ...

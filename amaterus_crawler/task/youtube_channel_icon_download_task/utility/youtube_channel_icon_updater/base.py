from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class YoutubeChannelIconUpdateQuery:
    remote_youtube_channel_id: str
    """
    チャンネルID
    """
    remote_icon_url: str
    """
    アイコンURL
    """
    is_downloaded: bool = False
    """
    ダウンロード済みかどうか
    """
    downloaded_at: datetime | None = None
    """
    ダウンロードした日時を表すタイムゾーン付き日時
    """
    object_key: str | None = None
    """
    ダウンロードしたファイルのオブジェクトキー
    """
    object_sha256_digest: str | None = None
    """
    ダウンロードしたファイルの SHA256 ハッシュ値
    """


class YoutubeChannelIconUpdateError(Exception):
    pass


class YoutubeChannelIconUpdater(ABC):
    @abstractmethod
    async def update_youtube_channel_icons(
        self,
        update_queries: list[YoutubeChannelIconUpdateQuery],
    ) -> None: ...

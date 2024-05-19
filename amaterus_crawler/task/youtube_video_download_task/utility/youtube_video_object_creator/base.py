from abc import ABC, abstractmethod
from datetime import datetime


class YoutubeVideoObjectCreateError(Exception):
    pass


class YoutubeVideoObjectCreator(ABC):
    @abstractmethod
    async def create_youtube_video_object(
        self,
        remote_youtube_video_id: str,
        object_key: str,
        sha256_digest: str,
        object_size: int,
        content_type: str,
        fetched_at: datetime,
    ) -> None:
        """
        Args:
            remote_youtube_video_id (str): YouTubeの動画ID
            object_key (str): 動画ファイルのオブジェクトキー
            sha256_digest (str): 動画ファイルの SHA256 ハッシュ値
            object_size (int): 動画ファイルのオブジェクトサイズ
            content_type (str): 動画ファイルのMime Type
            fetched_at (datetime): クローラによる自動的な情報取得の日時を表すタイムゾーン付き日時
        Returns:
           None
        """
        ...

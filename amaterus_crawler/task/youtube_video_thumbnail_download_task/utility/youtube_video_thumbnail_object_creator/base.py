from abc import ABC, abstractmethod
from datetime import datetime


class YoutubeVideoThumbnailObjectCreateError(Exception):
    pass


class YoutubeVideoThumbnailObjectCreator(ABC):
    @abstractmethod
    async def create_youtube_video_thumbnail_object(
        self,
        remote_youtube_video_thumbnail_url: str,
        object_key: str,
        sha256_digest: str,
        object_size: int,
        content_type: str,
        fetched_at: datetime,
    ) -> None:
        """
        Args:
            remote_youtube_video_thumbnail_url (str): サムネイルのURL
            object_key (str): サムネイルのオブジェクトキー
            sha256_digest (str): サムネイルの SHA256 ハッシュ値
            object_size (int): サムネイルのオブジェクトサイズ
            content_type (str): サムネイルのMime Type
            fetched_at (datetime): クローラによる自動的な情報取得の日時を表すタイムゾーン付き日時
        Returns:
           None
        """
        ...

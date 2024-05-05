from dataclasses import dataclass


@dataclass
class VideoInspection:
    duration: float
    """
    動画ファイルの再生時間の秒数
    """

    width: int
    """
    動画ファイルの映像の幅
    """

    height: int
    """
    動画ファイルの映像の高さ
    """

    num_frames: int
    """
    動画ファイルの映像のフレーム数
    """

    frame_rate: float
    """
    動画ファイルの映像のフレームレート
    """

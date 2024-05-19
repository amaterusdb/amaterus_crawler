from pathlib import Path
from typing import Annotated

import yaml
from pydantic import BaseModel, Field

from .global_config import GlobalConfig
from .server_config import ServerConfig
from .task_config import (
    DownloadYoutubeChannelThumbnailConfig,
    SearchYoutubeChannelVideoConfig,
    UpdateYoutubeChannelConfig,
)

TaskConfigType = (
    UpdateYoutubeChannelConfig
    | DownloadYoutubeChannelThumbnailConfig
    | SearchYoutubeChannelVideoConfig
)


class AmaterusCrawlerConfig(BaseModel):
    global_config: Annotated[GlobalConfig, Field(alias="global")]
    server_config: Annotated[ServerConfig, Field(alias="server")]
    task_configs: Annotated[
        list[TaskConfigType],
        Field(alias="tasks", default_factory=lambda: []),
    ]


def parse_amaterus_crawler_config_from_file(config_file: Path) -> AmaterusCrawlerConfig:
    with config_file.open(mode="r", encoding="utf-8") as fp:
        config_dict = yaml.safe_load(fp)

    return AmaterusCrawlerConfig.model_validate(config_dict)

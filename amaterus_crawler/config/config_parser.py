from pathlib import Path
from typing import Annotated

import yaml
from pydantic import BaseModel, Field

from .global_config import GlobalConfig
from .runner_config import DownloadYoutubeChannelIconConfig, UpdateYoutubeChannelConfig

RunnerConfigType = UpdateYoutubeChannelConfig | DownloadYoutubeChannelIconConfig


class AmaterusCrawlerConfig(BaseModel):
    global_config: Annotated[GlobalConfig, Field(alias="global")]
    runner_configs: Annotated[
        list[RunnerConfigType],
        Field(alias="runners", default_factory=lambda: []),
    ]


def parse_amaterus_crawler_config_from_file(config_file: Path) -> AmaterusCrawlerConfig:
    with config_file.open(mode="r", encoding="utf-8") as fp:
        config_dict = yaml.safe_load(fp)

    return AmaterusCrawlerConfig.model_validate(config_dict)

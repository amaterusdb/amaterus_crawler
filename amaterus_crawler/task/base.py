from abc import ABC, abstractmethod


class AmaterusCrawlerTask(ABC):
    @abstractmethod
    async def run(self) -> None: ...

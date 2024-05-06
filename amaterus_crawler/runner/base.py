from abc import ABC, abstractmethod


class Runner(ABC):
    @abstractmethod
    async def run(self) -> None: ...

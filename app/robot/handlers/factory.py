from abc import abstractmethod
from telegram import Update


class Handler:
    type = ...

    @abstractmethod
    async def process(self, *args, **kwargs):
        pass

    @abstractmethod
    async def support(self, *args, **kwargs):
        pass


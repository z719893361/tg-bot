from abc import abstractmethod


class HandlerFactory:
    @abstractmethod
    async def process(self, *args, **kwargs):
        pass

    @abstractmethod
    async def support(self, *args, **kwargs):
        pass

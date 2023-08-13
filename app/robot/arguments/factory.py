from abc import abstractmethod
from inspect import Parameter
from telegram import Update


class MethodArgumentResolver:

    @abstractmethod
    async def suppert(self, parameter: Parameter):
        pass

    @abstractmethod
    async def resovle(self, parameter: Parameter, update: Update, context):
        pass


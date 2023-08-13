from abc import abstractmethod
from typing import Type, Union
from telegram import Update, Message, CallbackQuery
from telegram.constants import ChatType


class Handler:
    evet_type: Type[ChatType]
    chat_type: Union[Message, CallbackQuery]

    @abstractmethod
    async def process(self, *args, **kwargs):
        pass

    @abstractmethod
    async def support(self, *args, **kwargs):
        pass

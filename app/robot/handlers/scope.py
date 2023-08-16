from typing import Set
from telegram import Message, CallbackQuery
from telegram.constants import ChatType


class ActionHandlerRegistry:
    def __init__(self, operation_type):
        self._operation_type = operation_type
        self._supporters: Set[ActionHandlerRegistry] = {self}

    def support(self, operation_type):
        return operation_type in self._supporters

    def __or__(self, other):
        self._supporters.add(other)
        return self

    def __hash__(self):
        return hash(self._operation_type)

    def __eq__(self, other):
        return self._operation_type == other


class ReplyScope:
    Group = ActionHandlerRegistry(ChatType.GROUP)
    Private = ActionHandlerRegistry(ChatType.PRIVATE)
    Message = ActionHandlerRegistry(Message)
    CallbackQuery = ActionHandlerRegistry(CallbackQuery)


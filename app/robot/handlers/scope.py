from typing import Set
from telegram import Message, CallbackQuery
from telegram.constants import ChatType


class ActionHandlerRegistry:
    def __init__(self, operation_type):
        self.operation_type = operation_type
        self.supporters: Set[ActionHandlerRegistry] = {self}

    def support(self, operation_type):
        return operation_type in self.supporters

    def __or__(self, other):
        self.supporters.add(other)
        return self

    def __hash__(self):
        return hash(self.operation_type)

    def __eq__(self, other):
        return self.operation_type == other


class ReplyScope:
    Group = ActionHandlerRegistry(ChatType.GROUP)
    Private = ActionHandlerRegistry(ChatType.PRIVATE)
    Message = ActionHandlerRegistry(Message)
    CallbackQuery = ActionHandlerRegistry(CallbackQuery)




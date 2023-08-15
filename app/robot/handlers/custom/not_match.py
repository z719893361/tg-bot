from telegram import Message

from robot.handlers.factory import HandlerFactory
from robot.handlers.comosite import handles
from robot.handlers.scope import ReplyScope


@handles.register(scope=ReplyScope.Message | ReplyScope.Private, order=100)
class NotMatch(HandlerFactory):

    async def support(self):
        return True

    async def process(self, message: Message):
        await message.reply_text('消息不是广告词或者命令')

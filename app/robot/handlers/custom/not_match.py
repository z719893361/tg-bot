from telegram.constants import ChatType
from robot.handlers.factory import Handler
from telegram import Message


class NotMatch(Handler):
    evet_type = Message
    chat_type = ChatType.PRIVATE

    async def support(self):
        return True

    async def process(self, message: Message):
        await message.reply_text('消息不是广告词或者命令')

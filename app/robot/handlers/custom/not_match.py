from robot.handlers.factory import Handler
from telegram import Message


class NotMatch(Handler):
    type = Message

    async def support(self):
        return True

    async def process(self, message: Message):
        await message.reply_text('消息不是广告词或者命令')

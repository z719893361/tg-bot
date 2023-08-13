from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Message, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ChatType
from jinja2 import Template
from config.config import TemplateConstant
from db import crud
from robot.handlers.factory import Handler


class Start(Handler):
    evet_type = Message
    chat_type = ChatType.PRIVATE

    async def support(self, message: str) -> bool:
        return message == '/start'

    async def process(
            self,
            db: AsyncSession,
            robot_id: int,
            robot_username: str,
            robot_nickname: str,
            from_user_id: int,
            from_username: str,
            from_nickname: str,
            message: Message
    ) -> None:
        content, parse_mode = await crud.template.get_template_content(db, robot_id, TemplateConstant.WELCOME_MESSAGE)
        await crud.user.insert_user(db, message.from_user.id)
        template = Template(content)
        text = template.render(
            robot_id=robot_id,
            robot_username=robot_username,
            robot_nickname=robot_nickname,
            from_id=from_user_id,
            from_username=from_username,
            from_nickname=from_nickname,
        )
        keyboard = ReplyKeyboardMarkup(
            [
                [KeyboardButton("📨发布广告"), KeyboardButton("💰我要充值")],
                [KeyboardButton("👤个人中心"), KeyboardButton("👥进内部群")]
            ],
            resize_keyboard=True
        )
        await message.reply_text(text, reply_markup=keyboard, parse_mode=parse_mode, reply_to_message_id=message.message_id)

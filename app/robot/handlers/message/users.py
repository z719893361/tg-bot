from telegram import Message
from jinja2 import Template
from sqlalchemy.ext.asyncio import AsyncSession
from config.config import TemplateConstant
from robot.handlers.comosite import handles
from robot.handlers.factory import HandlerFactory
from robot.handlers.scope import ReplyScope
from db import crud


@handles.register(ReplyScope.Message | ReplyScope.Private)
class User(HandlerFactory):

    async def support(self, message: str) -> bool:
        return message == '👤个人中心'

    async def process(
            self,
            db: AsyncSession,
            robot_id: int,
            message: Message,
            from_user_id: int,
            from_username: str,
            from_nickname: str
    ) -> None:
        amount = await crud.user.get_user_amount(db, from_user_id)
        content, parse_mode = await crud.template.get_template_content(db, robot_id, TemplateConstant.USER_PROFILE)
        template = Template(content)
        text = template.render(
            user_id=from_user_id,
            username=from_username,
            nickname=from_nickname,
            amount=amount
        )
        await message.reply_text(text=text, parse_mode=parse_mode, reply_to_message_id=message.message_id)

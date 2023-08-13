import re
from sqlalchemy.ext.asyncio import AsyncSession
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, Bot
from telegram.constants import ChatType
from jinja2 import Template
from config.config import TemplateConstant
from db import crud
from robot.handlers.factory import Handler


class JoinGroupMessage(Handler):
    evet_type = Message
    chat_type = ChatType.PRIVATE

    async def support(self, message: str) -> bool:
        return message == '👥进内部群'

    async def process(self, db: AsyncSession, robot_id: int, message: Message) -> None:
        group_model = await crud.group.get_group_model(db, robot_id)
        content, parse_mode = await crud.template.get_template_content(db, robot_id, TemplateConstant.VIP_GROUP_PROMPT)
        template = Template(content)
        template_render = template.render(
            price=group_model.price,
        )
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text='✔确认加群', callback_data="group_join_ok"),
                InlineKeyboardButton(text='❌取消加群', callback_data='group_join_no'),
            ]
        ])
        await message.reply_text(
            text=template_render,
            reply_markup=keyboard,
            parse_mode=parse_mode,
            reply_to_message_id=message.id
        )


class JoinGroupCall(Handler):
    evet_type = CallbackQuery
    chat_type = ChatType.PRIVATE

    async def support(self, data: str) -> bool:
        return data in ['group_join_ok', 'group_join_no']

    async def process(
            self,
            db: AsyncSession,
            bot: Bot,
            robot_id: int,
            from_id: int,
            data: str,
            call: CallbackQuery
    ) -> None:
        if data == 'group_join_no':
            await call.delete_message()
            return
        group_model = await crud.group.get_group_model(
            db=db,
            robot_id=robot_id
        )
        link_match = re.search(
            pattern='https://t.me/(.+)',
            string=group_model.link
        )
        if link_match is None:
            return
        if await crud.user.update_user_balance(db, from_id, -group_model.price):
            invite_link = await bot.create_chat_invite_link(chat_id='@' + link_match.group(1))
            await call.edit_message_text(
                text="加群链接: " + invite_link.invite_link
            )
        else:
            content, parse = await crud.template.get_template_content(
                db=db,
                robot_id=robot_id,
                name=TemplateConstant.INSUFFICIENT_BALANCE
            )
            await call.edit_message_text(text=content, parse_mode=parse)

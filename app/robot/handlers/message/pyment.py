import re
from datetime import datetime, timedelta
from jinja2 import Template
from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from decimal import Decimal

from telegram.constants import ChatType

from config.config import TemplateConstant
from db import crud
from models.form.order import OrderForm
from robot.handlers.factory import Handler


class PymentRecharge(Handler):
    evet_type = CallbackQuery
    chat_type = ChatType.PRIVATE

    pattern = re.compile(r'recharge_(\d+.?\d*)')

    async def support(self, data: str):
        return self.pattern.match(data)

    async def process(
            self,
            db: AsyncSession,
            call: CallbackQuery,
            robot_id: int,
            chat_id: int,
            from_id: int,
            message_id: int,
            data: str
    ):
        option_id = self.pattern.match(data).group(1)
        wallet_model = await crud.wallet.get_wallet_model(db, robot_id)
        recharge_model = await crud.recharge.get_option_model(db, option_id)
        orders_model = await crud.order.get_order_all(db, wallet_model.expires)
        existing_amounts = {row.amount for row in orders_model}
        amount_increment = Decimal('0.001')
        amount_recharge = recharge_model.amount
        while amount_recharge in existing_amounts:
            amount_recharge += amount_increment
        new_order = OrderForm(
            robot_id=robot_id,
            user_id=from_id,
            chat_id=chat_id,
            message_id=message_id,
            amount=amount_recharge,
            give=recharge_model.give,
            status=0
        )
        await crud.order.insert_order(
            db=db,
            form=new_order
        )
        content, parse_mode = await crud.template.get_template_content(
            db=db,
            robot_id=robot_id,
            name=TemplateConstant.AMOUNT_SELECTED_PROMPT
        )
        create_time = datetime.now()
        expires_time = create_time + timedelta(seconds=wallet_model.expires)
        template = Template(content)
        text = template.render(
            address=wallet_model.address,
            amount=amount_recharge,
            create_time=create_time,
            expires_time=expires_time,
            expires_seconds=wallet_model.expires

        )
        await call.edit_message_text(
            text=text,
            parse_mode=parse_mode
        )


async def create_buttom(db, robot_id):
    recharge_options = await crud.recharge.get_option_model_all(db, robot_id)
    colum = []
    for option in recharge_options:
        keyboard = InlineKeyboardButton(
            text=f'%sU' % str(option.amount).rstrip('0').rstrip("."),
            callback_data="recharge_%d" % option.id
        )
        colum.append([keyboard])
    return InlineKeyboardMarkup(colum)


class PymentMessage(Handler):
    evet_type = Message
    chat_type = ChatType.PRIVATE

    async def support(self, message: str):
        return message == '💰我要充值'

    async def process(self, db: AsyncSession, message: Message, robot_id: int):
        reply_markup = await create_buttom(db, robot_id)
        content, parse_mode = await crud.template.get_template_content(
            db=db,
            robot_id=robot_id,
            name=TemplateConstant.RECHARGE_BUTTON_PROMPT
        )
        await message.reply_text(
            text=content,
            reply_to_message_id=message.message_id,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )


class RechargeViewCallback(Handler):
    """
    充值按钮
    """
    evet_type = CallbackQuery
    chat_type = ChatType.PRIVATE

    async def support(self, message: str):
        return message == 'recharge'

    async def process(self, db: AsyncSession, robot_id: int, call: CallbackQuery):
        keyboard = await create_buttom(db, robot_id)
        content, parse_mode = await crud.template.get_template_content(
            db=db,
            robot_id=robot_id,
            name=TemplateConstant.RECHARGE_BUTTON_PROMPT
        )
        await call.edit_message_text(text=content, reply_markup=keyboard, parse_mode=parse_mode)

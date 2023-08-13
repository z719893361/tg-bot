import re
from jinja2 import Template, Environment, FileSystemLoader
from sqlalchemy.ext.asyncio import AsyncSession
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from telegram import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config.config import TemplateConstant
from db import crud
from robot.handlers.factory import Handler

env = Environment(loader=FileSystemLoader('robot/template'))


class AdPrompt(Handler):
    """
    点击广告发布
    """
    type = Message

    async def support(self, message: str) -> bool:
        return message == '📨发布广告'

    async def process(self, message: Message, context: ContextTypes.DEFAULT_TYPE):
        text = env.get_template('ad/step_1').render()
        await message.reply_text(text, reply_to_message_id=message.message_id)


class AdContentParser(Handler):
    """
    广告内容解析
    """
    type = Message

    pattern_name = re.compile(r'项目名称\s*[:：]\s*([^\n]+)')
    pattern_desc = re.compile(r'项目介绍\s*[:：]\s*([^\n]+)')
    pattern_contacts = re.compile(r'联系人\s*[:：]\s*([^\n]+)')
    pattern_price = re.compile(r'价格\s*[:：]\s*([^\n]+)')
    pattern_channel = re.compile(r'频道\s*[:：]\s*([^\n$]+)')
    pattern_button = re.compile(r'([^-\s]+)\s*-\s*([^\n\s$|]+)')

    async def support(self, content: str):
        return all([
            self.pattern_name.search(content),
            self.pattern_desc.search(content),
            self.pattern_contacts.search(content),
            self.pattern_price.search(content)
        ])

    @staticmethod
    def get_regex_result(regex, content) -> str:
        result = regex.search(content)
        return result.group(1) if result else None

    async def process(
            self,
            db: AsyncSession,
            message: Message,
            context: ContextTypes.DEFAULT_TYPE,
            robot_id: int,
            content: str,
            from_username: str
    ):
        project_name = self.get_regex_result(self.pattern_name, content)
        project_desc = self.get_regex_result(self.pattern_desc, content)
        project_contact = self.get_regex_result(self.pattern_contacts, content)
        project_price = self.get_regex_result(self.pattern_price, content)
        project_channel = self.get_regex_result(self.pattern_channel, content)
        ad_content, parse_mode = await crud.template.get_template_content(
            db=db,
            robot_id=robot_id,
            name=TemplateConstant.ADVERTISEMENT_DETAILS
        )
        ad_template = Template(ad_content)
        ad_content = ad_template.render(
            project_name=project_name,
            project_desc=project_desc,
            project_contact=project_contact,
            project_price=project_price,
            project_channel=project_channel,
            publisher=from_username
        )
        ad_botton_content, _ = await crud.template.get_template_content(
            db=db,
            robot_id=robot_id,
            name=TemplateConstant.ADVERTISEMENT_BUTTON
        )
        # 构建广告按钮
        markup = []
        for line in ad_botton_content.split('\n'):
            line_keyboard = []
            for title, url in self.pattern_button.findall(line):
                line_keyboard.append(InlineKeyboardButton(text=title, url=url))
            markup.append(line_keyboard)

        # 数据暂存
        ad_keyboard = InlineKeyboardMarkup(markup)
        context.user_data['push_ad_content'] = ad_content
        context.user_data['push_ad_parse_mode'] = parse_mode
        context.user_data['push_ad_keyboard'] = ad_keyboard
        await message.reply_text(text=ad_content, parse_mode=parse_mode, reply_markup=ad_keyboard)
        # 广告确认发布
        ad_confirm_content, parse_mode = await crud.template.get_template_content(db, robot_id, TemplateConstant.ADVERTISEMENT_CONFIRMATION)
        push_ad_price = await crud.ad_price.get_price(db, robot_id)
        context.bot_data['push_ad_price'] = push_ad_price
        ad_confirm_template = Template(ad_confirm_content)
        ad_confirm_text = ad_confirm_template.render(push_ad_price=push_ad_price)
        ad_confirm_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text='✔立即发布', callback_data='push_ad_ok'),
                InlineKeyboardButton(text='❌取消发布', callback_data='push_ad_no'),
            ]
        ])
        await message.reply_text(text=ad_confirm_text, parse_mode=parse_mode, reply_markup=ad_confirm_keyboard)


class AdPublisher(Handler):
    type = CallbackQuery

    async def support(self, data: str):
        return data in ['push_ad_ok', 'push_ad_no']

    async def process(
            self, db: AsyncSession,
            robot_id: int,
            from_id: int,
            message: Message,
            context: ContextTypes.DEFAULT_TYPE,
            data: str
    ):
        if data == 'push_ad_no':
            await message.delete()
            return
        # 获取广告价格
        ad_price = context.bot_data['push_ad_price']
        content = context.user_data.get('push_ad_content')
        parse_mode = context.user_data.get('push_ad_parse_mode')
        keyboard = context.user_data.get('push_ad_keyboard')
        if await crud.user.update_user_balance(db, from_id, -ad_price):
            await push_advertisement(db, robot_id, message, content, keyboard, parse_mode)
            await message.edit_text('发布成功', parse_mode=parse_mode)
        else:
            await message.edit_text('余额不足', parse_mode=parse_mode)


async def push_advertisement(db: AsyncSession, robot_id: int, message: Message, content, reply_markup, parse_mode):
    bot = message.get_bot()
    channels_model = await crud.channel.get_channel_by_robot(db, robot_id)
    for channel_model in channels_model:
        match = re.search('https://t.me/(.+)', channel_model.link)
        if not match:
            continue
        channel_username = match.group(1)
        await bot.send_message(
            chat_id=f'@{channel_username}',
            text=content,
            parse_mode=parse_mode,
            reply_markup=reply_markup
        )

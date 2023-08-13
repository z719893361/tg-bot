from inspect import Parameter
from telegram import Update, User, Bot, Message, CallbackQuery
from telegram.ext import ContextTypes

from robot.arguments.factory import MethodArgumentResolver


class RobotID(MethodArgumentResolver):

    async def suppert(self, parameter: Parameter):
        return parameter.name == 'robot_id' and parameter.annotation == int

    async def resovle(self, parameter: Parameter, update: Update, context: ContextTypes.DEFAULT_TYPE):
        return update.get_bot().id


class RobotUserName(MethodArgumentResolver):
    async def suppert(self, parameter: Parameter):
        return parameter.name == 'robot_username' and parameter.annotation == str

    async def resovle(self, parameter: Parameter, update: Update, context: ContextTypes.DEFAULT_TYPE):
        return update.get_bot().username


class RobotNickName(MethodArgumentResolver):
    async def suppert(self, parameter: Parameter):
        return parameter.name == 'robot_nickname' and parameter.annotation == str

    async def resovle(self, parameter: Parameter, update: Update, context: ContextTypes.DEFAULT_TYPE):
        me = update.get_bot()
        return me.first_name or '' + me.last_name or ''


class RobotUser(MethodArgumentResolver):

    async def suppert(self, parameter: Parameter):
        return parameter.annotation == User

    async def resovle(self, parameter: Parameter, update: Update, context: ContextTypes.DEFAULT_TYPE):
        return update.get_bot().get_me()


class GetRobot(MethodArgumentResolver):

    async def suppert(self, parameter: Parameter):
        return parameter.annotation == Bot

    async def resovle(self, parameter: Parameter, update: Update, context: ContextTypes.DEFAULT_TYPE):
        return update.get_bot()


class FromID(MethodArgumentResolver):

    async def suppert(self, parameter: Parameter):
        return parameter.name in ('from_id', 'from_user_id') and parameter.annotation == int

    async def resovle(self, parameter: Parameter, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message:
            return update.message.from_user.id
        if update.callback_query:
            return update.callback_query.from_user.id


class FromUserName(MethodArgumentResolver):

    async def suppert(self, parameter: Parameter):
        return parameter.name == 'from_username' and parameter.annotation == str

    async def resovle(self, parameter: Parameter, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message:
            user: User = update.message.from_user
        elif update.callback_query:
            user: User = update.callback_query.from_user
        else:
            return
        return user.username


class FromNickName(MethodArgumentResolver):
    async def suppert(self, parameter: Parameter):
        return parameter.name == 'from_nickname' and parameter.annotation == str

    async def resovle(self, parameter: Parameter, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message:
            user: User = update.message.from_user
        elif update.callback_query:
            user: User = update.callback_query.from_user
        else:
            return
        return user.first_name or '' + user.last_name


class FromUser(MethodArgumentResolver):
    async def suppert(self, parameter: Parameter):
        return parameter.annotation == User

    async def resovle(self, parameter: Parameter, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message:
            return update.message.from_user
        if update.callback_query:
            return update.callback_query.from_user


class FromChatID(MethodArgumentResolver):
    async def suppert(self, parameter: Parameter):
        return parameter.name in ['chat_id', 'from_chat_id'] and parameter.annotation == int

    async def resovle(self, parameter: Parameter, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message:
            return update.message.chat.id
        if update.callback_query:
            return update.callback_query.message.chat.id


class FromMessageID(MethodArgumentResolver):
    async def suppert(self, parameter: Parameter):
        return parameter.name == 'message_id' and parameter.annotation == int

    async def resovle(self, parameter: Parameter, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message:
            return update.message.message_id
        if update.callback_query:
            return update.callback_query.message.message_id


class FromMessageReplyID(MethodArgumentResolver):

    async def suppert(self, parameter: Parameter):
        return parameter.name == 'reply_id' and parameter.annotation == int

    async def resovle(self, parameter: Parameter, update: Update, context):
        if update.message:
            return update.message.reply_to_message.id
        if update.callback_query:
            return update.callback_query.message.reply_to_message.id


class FromCallback(MethodArgumentResolver):
    async def suppert(self, parameter: Parameter):
        return parameter.annotation == CallbackQuery

    async def resovle(self, parameter: Parameter, update: Update, context: ContextTypes.DEFAULT_TYPE):
        return update.callback_query


class FromMessage(MethodArgumentResolver):
    async def suppert(self, parameter: Parameter):
        return parameter.annotation == Message

    async def resovle(self, parameter: Parameter, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message:
            return update.message
        if update.callback_query:
            return update.callback_query.message


class MessageData(MethodArgumentResolver):
    async def suppert(self, parameter: Parameter):
        return parameter.name in ['message', 'data', 'content'] and parameter.annotation == str

    async def resovle(self, parameter: Parameter, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message:
            return update.message.text
        if update.callback_query:
            return update.callback_query.data


class ContextData(MethodArgumentResolver):
    async def suppert(self, parameter: Parameter):
        return parameter.annotation == ContextTypes.DEFAULT_TYPE

    async def resovle(self, parameter: Parameter, update: Update, context):
        return context

from inspect import Parameter
from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Update

from db import get_db
from robot.arguments.factory import MethodArgumentResolver


class DBSession(MethodArgumentResolver):
    async def suppert(self, parameter: Parameter):
        return parameter.annotation == AsyncSession

    async def resovle(self, parameter: Parameter, update: Update, context):
        return get_db()


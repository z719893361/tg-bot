import inspect
from telegram.ext import ContextTypes
from inspect import Parameter
from telegram import Update
from robot.arguments.param import Depends
from robot.arguments.factory import MethodArgumentResolver


class DependsResolver(MethodArgumentResolver):
    async def suppert(self, parameter: Parameter):
        return issubclass(parameter.default, Depends)

    async def resovle(self, parameter: Parameter, update: Update, context: ContextTypes.DEFAULT_TYPE):
        funct: Depends = parameter.default
        if inspect.isasyncgenfunction(funct):
            return await funct.dependency()
        else:
            return funct.dependency()



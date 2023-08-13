from inspect import isasyncgen, Parameter, signature, isgenerator
from pathlib import Path
from typing import List, Dict, Any
from telegram import Update, Message, CallbackQuery
from telegram.constants import ChatType
from typing import Generator
from telegram.ext import ContextTypes
from robot.handlers.factory import Handler
from robot.handlers.custom.not_match import NotMatch
from robot.arguments.composite import arguments_composite
from robot.utlis.load import load_classes_from_directory

import logging

logger = logging.getLogger('消息')
logger.setLevel(logging.INFO)


class Comosite(Handler):
    handle: List[Handler] = []

    def add_handle(self, handle: Handler):
        self.handle.append(handle)

    async def support(self, update: Update):
        return update.message or update.callback_query

    async def process(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        generator: List[Generator] = []
        current_context: Dict[Parameter, Any] = {}
        envet_type = None
        if update.message:
            envet_type = Message
        if update.callback_query:
            envet_type = CallbackQuery
        try:
            for handle in self.handle:
                # 事件类型判断
                if handle.chat_type != handle.chat_type or handle.evet_type != envet_type:
                    continue
                # 判断是否支持处理
                arguments = await self.build_params(handle.support, update, context, current_context, generator)
                if not await handle.support(*arguments):
                    continue
                # 消息处理
                arguments = await self.build_params(handle.process, update, context, current_context, generator)
                await handle.process(*arguments)
                break
        except Exception as e:
            logger.error(e)
        for generator in generator:
            await self.close_generator(generator)

    @staticmethod
    async def build_params(
            function,
            update,
            context: ContextTypes.DEFAULT_TYPE,
            current_context: Dict,
            generator: List[Generator]
    ) -> List:
        arguments = []
        for param in signature(function).parameters.values():
            name = current_context.get(param)
            if name is not None:
                arguments.append(name)
                continue
            result_value = await arguments_composite.resovle(param, update, context)
            if isasyncgen(result_value):
                generator.append(result_value)
                result_value = await anext(result_value)
            arguments.append(result_value)
            current_context[param] = result_value
        return arguments

    @staticmethod
    async def close_generator(generator):
        if isasyncgen(generator):
            async for _ in generator:
                pass
        if isgenerator(generator):
            for _ in generator:
                pass


handle_comosite = Comosite()

current_dir = Path(__file__).absolute().parent
for cls in load_classes_from_directory(current_dir.joinpath('message'), Handler):
    handle_comosite.add_handle(cls())

# 没有指令匹配
handle_comosite.add_handle(NotMatch())

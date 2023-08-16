import logging
from typing import List, Dict, Any
from typing import Generator
from pathlib import Path
from inspect import isasyncgen, Parameter, signature, isgenerator
from telegram.ext import ContextTypes
from telegram import Update, Message, CallbackQuery
from robot.handlers.factory import HandlerFactory
from robot.arguments.composite import arguments_composite
from robot.handlers.scope import ActionHandlerRegistry
from robot.utlis.load import scan_and_load, load_module

logger = logging.getLogger('消息')
logger.setLevel(logging.ERROR)


class DecoratorInfo:
    handler: HandlerFactory = ...
    scope: ActionHandlerRegistry = ...
    order: int = ...

    def __init__(self, handler_cls, scpoe, order):
        self.handler = handler_cls
        self.scope = scpoe
        self.order = order


class Comosite(HandlerFactory):
    _handles: List[DecoratorInfo] = []

    def register(self, scope, order=0):
        def decorator(cls):
            self._handles.append(DecoratorInfo(cls(), scope, order))
            self._handles.sort(key=lambda x: x.order)

        return decorator

    async def support(self, update: Update):
        return True

    async def process(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        generator: List[Generator] = []
        current_context: Dict[Parameter, Any] = {}
        envet_type = None
        if update.message:
            envet_type = Message
        if update.callback_query:
            envet_type = CallbackQuery
        try:
            for handle in self._handles:
                if not handle.scope.support(envet_type) or not handle.scope.support(update.effective_chat.type):
                    continue
                arguments = await self.build_params(handle.handler.support, update, context, current_context, generator)
                if not await handle.handler.support(*arguments):
                    continue
                arguments = await self.build_params(handle.handler.process, update, context, current_context, generator)
                await handle.handler.process(*arguments)
                break
        except Exception as e:
            logger.error(e)
        for generator in generator:
            await self.close_generator(generator)

    @staticmethod
    async def build_params(
            func,
            update,
            context: ContextTypes.DEFAULT_TYPE,
            current_context: Dict,
            generator: List[Generator]
    ) -> List:
        arguments = []
        for param in signature(func).parameters.values():
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


handles = Comosite()

# 扫描并导入当前目录下所有Py文件，无需显式导入
load_module(Path(__file__).parent)
load_module(Path(__file__).parent)
load_module(Path(__file__).parent)

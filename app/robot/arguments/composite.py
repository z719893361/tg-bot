from inspect import Parameter
from pathlib import Path
from typing import List, Dict, Set
from telegram import Update
from telegram.ext import ContextTypes

from robot.utlis.load import load_classes
from robot.arguments.factory import MethodArgumentResolver


class CompositeResolver(MethodArgumentResolver):
    # 解析器
    araumentResolves: List[MethodArgumentResolver] = []
    # 可解析参数缓存
    aragumentResolveCache: Dict[Parameter, MethodArgumentResolver] = {}
    # 不可解析参数缓存
    unresolvableParameters: Set[Parameter] = set()

    async def suppert(self, parameter: Parameter):
        return self.get_parameter_resolve(parameter) is not None

    async def resovle(self, parameter: Parameter, update: Update, context: ContextTypes.DEFAULT_TYPE):
        resolve = await self.get_parameter_resolve(parameter)
        if resolve is None:
            return
        return await resolve.resovle(parameter, update, context)

    async def get_parameter_resolve(self, parameter):
        if parameter in self.unresolvableParameters:
            return
        if parameter in self.aragumentResolveCache:
            return self.aragumentResolveCache.get(parameter)
        for resovle in self.araumentResolves:
            if await resovle.suppert(parameter):
                self.aragumentResolveCache[parameter] = resovle
                return resovle
        self.unresolvableParameters.add(parameter)

    def add_resolve(self, resovle: MethodArgumentResolver):
        self.araumentResolves.append(resovle)


arguments_composite = CompositeResolver()
current_dir = Path(__file__).parent.joinpath('Impl')
for cls in load_classes(current_dir, MethodArgumentResolver):
    arguments_composite.add_resolve(cls())


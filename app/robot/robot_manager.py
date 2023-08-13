from typing import Optional, Union, Dict, List
from telegram import Update
from telegram.ext import ApplicationBuilder, BaseHandler, ContextTypes, Application
from robot.handlers.comosite import handle_comosite


class AllHandler(BaseHandler):
    def __init__(self):
        super().__init__(self.handle)

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await handle_comosite.process(update, context)

    def check_update(self, update: object) -> Optional[Union[bool, object]]:
        return update


class RobotManager:
    def __init__(self):
        self.robot_manager: Dict[int, Application] = {}

    async def add(self, robot_id: int, token: str):
        app = ApplicationBuilder().token(token).build()
        app.add_handler(AllHandler())
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        self.robot_manager[robot_id] = app

    async def stop(self, robot_id: int):
        bot = self.robot_manager.get(robot_id)
        if bot is None:
            return
        self.robot_manager.pop(robot_id)
        await bot.updater.stop()
        await bot.stop()
        await bot.shutdown()

    def get_robot(self, robot_id: int) -> Application:
        return self.robot_manager.get(robot_id)

    def get_robots(self) -> List[Application]:
        return list(self.robot_manager.values())

    def get_robots_id(self) -> List[int]:
        return list(self.robot_manager.keys())

    def __contains__(self, item):
        return item in self.robot_manager


robot_manager = RobotManager()

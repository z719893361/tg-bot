from db import crud
from db.database import get_async_db, engine, Base
from robot import robot_manager, callback
from utils.transfer_manager import usdt_monitor_manage, TransactionMonitor
import logging


logger = logging.getLogger("启动事件")

logger.setLevel(logging.INFO)


async def robot_startup():
    """
    程序启动阶段启动机器人
    """
    async with get_async_db() as db:
        for robot in await crud.robot.get_robot_all(db):
            wallet_model = await crud.wallet.get_wallet_model(db, robot.robot_id)
            monitor = TransactionMonitor(wallet_model.address, wallet_model.expires, callback=callback.callback)
            await robot_manager.add(robot.robot_id, robot.token)
            logger.info('启动机器人: %d - %s', robot.robot_id, robot.name)
            await usdt_monitor_manage.add(robot_id=robot.robot_id, monitor=monitor)
            logger.info('启动钱包监控: %s', wallet_model.address)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


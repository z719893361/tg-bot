from robot import robot_manager
from utils.transfer_manager import usdt_monitor_manage
import logging

logger = logging.getLogger("终止事件")
logger.setLevel(logging.INFO)


async def robot_shutdown():
    for robot_id in robot_manager.get_robots_id():
        logger.info('关闭机器机器人: %d', robot_id)
        await robot_manager.stop(robot_id)
        monitor = usdt_monitor_manage.get_monitor(robot_id)
        logger.info('关闭钱包监控: %s', monitor.address)
        await usdt_monitor_manage.stop(robot_id)

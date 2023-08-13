from db import crud
from db.database import get_async_db
from robot.robot_manager import robot_manager


async def callback(transaction_id: str, amount: float, seconds: int):
    async with get_async_db() as db:
        order_model = await crud.order.get_order(db, amount, seconds)
        if order_model is None:
            return
        order_model.status = 1
        await crud.user.update_user_balance(db, order_model.user_id, order_model.amount + order_model.give)
        robot_id = order_model.robot_id
        chat_id = order_model.chat_id
        message_id = order_model.message_id
    robot = robot_manager.get_robot(robot_id)
    await robot.bot.edit_message_text('充值成功', chat_id=chat_id, message_id=message_id)

from typing import List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import RobotModel, TemplateModel, RechargeOptionModel, WalletModel, AdPriceModel, GroupModel
from config import default_data


async def insert_robot(db: AsyncSession, robot_id: int, name: str, token: str):
    db.add(RobotModel(robot_id=robot_id, name=name, token=token))


async def get_robot_model(db: AsyncSession, _id: int) -> RobotModel:
    stmt = select(RobotModel).where(RobotModel.id == _id)
    return await db.scalar(stmt)


async def update_robot(db: AsyncSession, _id: int, name: str, token: str):
    robot = await get_robot_model(db, _id)
    robot.name = name
    robot.token = token


async def delete_robot(db: AsyncSession, robot_ids: List[int]):
    stmt = delete(RobotModel).where(RobotModel.robot_id.in_(robot_ids))
    await db.execute(stmt)


async def get_robot_all(db: AsyncSession) -> List[RobotModel]:
    robots = await db.scalars(select(RobotModel))
    return robots.all()


async def init_default(db: AsyncSession, robot_id: int) -> None:
    template = []
    recharge_option = []
    for item in default_data.template:
        template.append(TemplateModel(robot_id=robot_id, **item.dict()))
    for option in default_data.recharge_option:
        recharge_option.append(RechargeOptionModel(robot_id=robot_id, amount=option.amount, give=option.give))
    db.add_all(template)
    db.add_all(recharge_option)
    db.add(AdPriceModel(robot_id=robot_id, price=default_data.advertisement_fee))
    db.add(GroupModel(robot_id=robot_id, link=default_data.group.link, price=default_data.group.price))
    db.add(WalletModel(robot_id=robot_id, address=default_data.wallet.address, expires=default_data.wallet.expires, ))

from typing import List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import RechargeOptionModel
from models.form.config import RechargeOptionForm


async def insert_recharge_option(db: AsyncSession, robot_id: int, option: RechargeOptionForm):
    db.add(RechargeOptionModel(robot_id=robot_id, amount=option.amount, give=option.give))


async def get_option_model_all(db: AsyncSession, robot_id: int) -> List[RechargeOptionModel]:
    stmt = select(RechargeOptionModel).where(RechargeOptionModel.robot_id == robot_id)
    models = await db.scalars(stmt)
    return models.all()


async def get_option_model(db: AsyncSession, _id: int) -> RechargeOptionModel:
    stmt = select(RechargeOptionModel).where(RechargeOptionModel.id == _id)
    model = await db.scalar(stmt)
    return model


async def update_recharge_option(db: AsyncSession, option: RechargeOptionForm):
    model = await get_option_model(db, option.id)
    if model is None:
        return
    model.amount = option.amount
    model.give = option.give


async def delete_recharge_option(db: AsyncSession, ids: List[int]):
    stmt = delete(RechargeOptionModel).where(RechargeOptionModel.id.in_(ids))
    await db.execute(stmt)


async def delete_recharge_option_by_robot_id(db: AsyncSession, robot_ids: List[int]):
    stmt = delete(RechargeOptionModel).where(RechargeOptionModel.robot_id.in_(robot_ids))
    await db.execute(stmt)

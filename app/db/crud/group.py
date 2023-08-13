from typing import List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import GroupModel
from models.form.config import GroupForm


async def get_group_model(db: AsyncSession, robot_id: int) -> GroupModel:
    stmt = select(GroupModel).where(GroupModel.robot_id == robot_id)
    return await db.scalar(stmt)


async def delete_group(db: AsyncSession, robot_ids: List[int]):
    stmt = delete(GroupModel).where(GroupModel.robot_id.in_(robot_ids))
    await db.execute(stmt)


async def upsert_group(db: AsyncSession, robot_id: int, form: GroupForm):
    group_model = await get_group_model(db, robot_id)
    if group_model is None:
        db.add(GroupModel(**form.model_dump()))
        return
    group_model.link = form.link
    group_model.price = form.price

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from db.models import ChannelModel


async def insert_channel(db: AsyncSession, robot_id: int, link: str):
    db.add(ChannelModel(robot_id=robot_id, link=link))


async def delete_channel_by_id(db: AsyncSession, ids: List[int]):
    stmt = delete(ChannelModel).where(ChannelModel.id.in_(ids))
    await db.execute(stmt)


async def delete_channel_by_robot_id(db: AsyncSession, robot_ids: List[int]):
    stmt = delete(ChannelModel).where(ChannelModel.robot_id.in_(robot_ids))
    await db.execute(stmt)


async def get_channel_by_robot(db: AsyncSession, roboot_id: int) -> List[ChannelModel]:
    stmt = select(ChannelModel).where(ChannelModel.robot_id == roboot_id)
    models = await db.scalars(stmt)
    return models.all()



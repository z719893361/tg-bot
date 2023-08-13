from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from decimal import Decimal
from db.models import AdPriceModel


async def insert_price(db: AsyncSession, robot_id: int, price: float):
    db.add(AdPriceModel(robot_id=robot_id, price=price))


async def get_price_model(db: AsyncSession, robot_id: int) -> AdPriceModel:
    stmt = select(AdPriceModel).where(AdPriceModel.robot_id == robot_id)
    return await db.scalar(stmt)


async def get_price(db: AsyncSession, robot_id: int) -> Decimal:
    price_model = await get_price_model(db, robot_id)
    if price_model:
        return price_model.price
    else:
        return Decimal('0')


async def update_price(db: AsyncSession, robot_id: int, price: float):
    price_model = await get_price_model(db, robot_id)
    if price_model:
        price_model.price = price


async def delete_ad_price_by_robot_id(db: AsyncSession, robot_id: List[int]):
    stmt = delete(AdPriceModel).where(AdPriceModel.robot_id.in_(robot_id))
    await db.execute(stmt)

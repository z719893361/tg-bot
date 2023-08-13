from datetime import datetime, timedelta
from typing import List
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import OrderModel
from models.form.order import OrderForm


async def get_order_all(db: AsyncSession, seconds=1200) -> List[OrderModel]:
    stmt = select(OrderModel).where(OrderModel.create_time > datetime.now() - timedelta(seconds=seconds))
    models = await db.scalars(stmt)
    return models.all()


async def get_order(db: AsyncSession, amount: float, seconds=1200) -> OrderModel:
    stmt = select(OrderModel).where(and_(
        OrderModel.amount == amount,
        OrderModel.status == 0,
        OrderModel.create_time >= datetime.now() - timedelta(seconds=seconds)
    ))
    model = await db.scalar(stmt)
    return model


async def insert_order(db: AsyncSession, form: OrderForm):
    db.add(OrderModel(**form.model_dump()))

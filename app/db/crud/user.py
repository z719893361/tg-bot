from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models import UserModel, UserLoginModel
from decimal import Decimal


async def insert_user(db: AsyncSession, user_id: int):
    model = await get_user(db, user_id)
    if model is None:
        db.add(UserModel(user_id=user_id, amount=0))


async def update_user_balance(db: AsyncSession, user_id: int, amount: Decimal):
    user = await get_user(db, user_id)
    if user is None:
        await insert_user(db, user_id)
        return False
    if user.amount + amount >= 0:
        user.amount += amount
        return True
    else:
        return False


async def get_user(db: AsyncSession, user_id: int) -> UserModel:
    stmt = select(UserModel).where(UserModel.user_id == user_id)
    user = await db.scalar(stmt)
    return user


async def get_user_amount(db: AsyncSession, user_id: int) -> Decimal:
    stmt = select(UserModel).where(UserModel.user_id == user_id)
    user: UserModel = await db.scalar(stmt)
    if user is None:
        return Decimal('0')
    else:
        return user.amount


async def get_user_login(db: AsyncSession, username: str, password: str) -> UserLoginModel:
    stmt = select(UserLoginModel).where(UserLoginModel.username == username and UserLoginModel.password == password)
    user = await db.scalar(stmt)
    return user

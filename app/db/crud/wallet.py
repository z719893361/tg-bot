from typing import List
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import WalletModel
from models.form.config import WalletForm


async def insert_wallet(db: AsyncSession, robot_id, address: str):
    db.add(WalletModel(robot_id=robot_id, address=address))


async def delete_wallet(db: AsyncSession, _id: int):
    await db.delete(WalletModel(id=_id))


async def delete_wallet_by_robot_id(db: AsyncSession, robot_ids: List[int]):
    stmt = delete(WalletModel).where(WalletModel.robot_id.in_(robot_ids))
    await db.execute(stmt)


async def update_wallet(db: AsyncSession, robot_id: int, form: WalletForm):
    wallet = await get_wallet_model(db, robot_id)
    if wallet is None:
        return
    wallet.address = form.address
    wallet.expires = form.expires


async def get_wallet_model(db: AsyncSession, robot_id: int) -> WalletModel:
    stmt = select(WalletModel).where(WalletModel.robot_id == robot_id)
    return await db.scalar(stmt)


async def get_wallet_address(db: AsyncSession, robot_id: int) -> str:
    wallet = await get_wallet_model(db, robot_id)
    return wallet.address if wallet.address else ''

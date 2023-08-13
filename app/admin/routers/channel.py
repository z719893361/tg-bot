from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from models.form.base import IdsForm
from models.form.config import ChannelForm
from models.response import Result
from db import get_db, crud
from models.schemas.channel import ChannelSchema

router = APIRouter(prefix='/channel/{robot_id}')


@router.get('', name='查询频道', response_model=Result[List[ChannelSchema]])
async def query_channels(robot_id: int, db: AsyncSession = Depends(get_db)):
    data = await crud.channel.get_channel_by_robot(db, robot_id)
    return Result.ok("查询成功", data)


@router.post('/add', name='增加频道')
async def insert_channel(robot_id: int, channel: ChannelForm, db: AsyncSession = Depends(get_db)):
    await crud.channel.insert_channel(db, robot_id, channel.link)
    return Result.ok("新增成功")


@router.post('/delete', name='删除频道')
async def delete_channels(channel: IdsForm, db: AsyncSession = Depends(get_db)):
    await crud.channel.delete_channel_by_id(db, channel.ids)
    return Result.ok("删除成功")

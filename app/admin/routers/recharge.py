from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import crud, get_db
from models.form.config import RechargeOptionForm
from models.form.base import IdsForm
from models.response import Result
from models.schemas.recharge import RechargeSchema


router = APIRouter(prefix='/recharge/{robot_id}', tags=['充值接口'])


@router.get('/list', name='查询充值选项', response_model=Result[List[RechargeSchema]])
async def query_recharge_options(robot_id: int, db: AsyncSession = Depends(get_db)):
    data = await crud.recharge.get_option_model_all(db, robot_id)
    return Result.ok("查询成功", data)


@router.post('/add', name="新增充值选项")
async def add_option(robot_id: int, recharge_option: RechargeOptionForm, db: AsyncSession = Depends(get_db)):
    await crud.recharge.insert_recharge_option(db, robot_id, recharge_option)
    return Result.ok("新增成功")


@router.post('/delete', name="删除充值选项")
async def delete_options(ids: IdsForm, db: AsyncSession = Depends(get_db)):
    await crud.recharge.delete_recharge_option(db, ids.ids)
    return Result.ok("删除成功")


@router.post('/update', name="修改充值选项")
async def update_option(recharge_option: RechargeOptionForm, db: AsyncSession = Depends(get_db)):
    await crud.recharge.update_recharge_option(db, recharge_option)
    return Result.ok("修改成功")

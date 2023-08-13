from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.form.config import RobotConfigForm
from models.response import Result
from models.schemas.config import ConfigSchema
from db import crud, get_db
from utils.transfer_manager import usdt_monitor_manage


router = APIRouter(prefix='/config/{robot_id}', tags=['配置数据'])


@router.post('/update', name="修改基本信息")
async def config_set(robot_id: int, config: RobotConfigForm, db: AsyncSession = Depends(get_db)):
    await crud.config.update_config(db, robot_id, config)
    await usdt_monitor_manage.update_monitor(robot_id, config.wallet.address, config.wallet.expires)
    return Result.ok("保存成功")


@router.get('/info', name="获取数据", response_model=Result[ConfigSchema], response_model_by_alias=False)
async def query_config(robot_id: int, db: AsyncSession = Depends(get_db)):
    data = await crud.config.get_config(db, robot_id)
    return Result.ok("查询成功", data)


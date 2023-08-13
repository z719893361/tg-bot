import json

import requests
import telegram
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Bot
from typing import List

from models.form.base import IdsForm
from models.form.robot import RobotCreateFrom, RobotUpdateFrom
from models.response import Result
from db import crud, get_db
from models.schemas.robot import RobotSchema
from robot.robot_manager import robot_manager
from robot.callback import callback
from utils.transfer_manager import usdt_monitor_manage, TransactionMonitor
from config.config import default_data


router = APIRouter(prefix='/robot', tags=["机器人"])


@router.post('/add', name="添加机器人")
async def insert_robot(robot: RobotCreateFrom, db: AsyncSession = Depends(get_db)):
    try:
        bot = Bot(robot.token)
        me = await bot.get_me()
        robot_id = me.id
    except telegram.error.InvalidToken:
        return Result.error("Token无效")
    except requests.exceptions.ConnectTimeout:
        return Result.error("无法连接到telegram")
    if robot_id in usdt_monitor_manage or robot_id in robot_manager:
        return Result.error('机器人已存在')
    await crud.robot.insert_robot(db, robot_id, robot.name, robot.token)
    await crud.robot.init_default(db, robot_id)
    monitor = TransactionMonitor(default_data.wallet.address, default_data.wallet.expires, callback=callback)
    await robot_manager.add(robot_id, robot.token)
    await usdt_monitor_manage.add(robot_id, monitor)
    return Result.ok(message="新增成功")


@router.post('/delete', name="删除机器人")
async def delete_robot(ids: IdsForm, db: AsyncSession = Depends(get_db)):
    # 删除机器人
    await crud.robot.delete_robot(db, ids.ids)
    # 删模板
    await crud.template.delete_template_by_robot_id(db, ids.ids)
    # 删充值按钮
    await crud.recharge.delete_recharge_option_by_robot_id(db, ids.ids)
    # 删群组
    await crud.group.delete_group(db, ids.ids)
    # 删频道
    await crud.channel.delete_channel_by_robot_id(db, ids.ids)
    # 删钱包
    await crud.wallet.delete_wallet_by_robot_id(db, ids.ids)
    # 删除广告价格
    await crud.ad_price.delete_ad_price_by_robot_id(db, ids.ids)
    # 停止机器人
    for robot_id in ids.ids:
        await robot_manager.stop(robot_id)
        await usdt_monitor_manage.stop(robot_id)
    return Result.ok(message="删除成功")


@router.post('/update', name="修改机器人")
async def update_robot(robot: RobotUpdateFrom, db: AsyncSession = Depends(get_db)):
    await crud.robot.update_robot(db, robot.id, robot.name, robot.token)
    return Result.ok(message="修改成功")


@router.get('/list', response_model=Result[List[RobotSchema]])
async def get_robot_list(db: AsyncSession = Depends(get_db)):
    data = await crud.robot.get_robot_all(db)
    return Result.ok(data=data)



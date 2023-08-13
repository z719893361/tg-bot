from sqlalchemy.ext.asyncio import AsyncSession

from db import crud
from models.form.config import RobotConfigForm
from models.schemas.config import ConfigSchema


# 获取所有配置
async def get_config(db: AsyncSession, robot: int) -> ConfigSchema:
    template_models = await crud.template.get_template_model_all(db, robot)
    # 获取模板数据
    templates = {model.name: model for model in template_models}
    # 获取钱包地址
    wallet_model = await crud.wallet.get_wallet_model(db, robot)
    # 获取广告价格
    ad_price_model = await crud.ad_price.get_price_model(db, robot)
    # 获取加群信息
    group_model = await crud.group.get_group_model(db, robot)

    return ConfigSchema(template=templates, wallet=wallet_model, ad_price=ad_price_model.price, group=group_model)


async def update_config(db: AsyncSession, robot_id: int, config: RobotConfigForm):
    await crud.ad_price.update_price(db, robot_id, config.ad_price)
    await crud.wallet.update_wallet(db, robot_id, config.wallet)
    await crud.group.upsert_group(db, robot_id, config.group)
    for template in config.template.values():
        await crud.template.update_template(db, robot_id, template)

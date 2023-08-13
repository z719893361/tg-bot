from typing import Dict, Optional, Union
from pydantic import BaseModel, ConfigDict


class Template(BaseModel):
    name: str

    content: str
    # 类型
    parse_mode: int

    model_config = ConfigDict(from_attributes=True)


class Group(BaseModel):
    id: int
    # 群链接
    link: str
    # 入群价格
    price: float

    model_config = ConfigDict(from_attributes=True)


class Wallet(BaseModel):
    id: Union[int, None] = ...
    address: str
    expires: int

    model_config = ConfigDict(from_attributes=True)


class ConfigSchema(BaseModel):
    # 模板数据
    template: Dict[str, Template]
    # 钱包地址
    wallet: Wallet
    # 广告价格
    ad_price: float = 0
    # 群组链接
    group: Optional[Group] = None

    model_config = ConfigDict(from_attributes=True)

from typing import List, Optional, Dict
from pydantic import BaseModel


class TemplateForm(BaseModel):
    name: str
    content: str
    parse_mode: int


class GroupForm(BaseModel):
    id: int
    link: str
    price: float


class WalletForm(BaseModel):
    id: int
    address: str
    expires: int


class RobotConfigForm(BaseModel):
    wallet: WalletForm
    template: Dict[str, TemplateForm]
    ad_price: float
    group: GroupForm


class RechargeOptionForm(BaseModel):
    # 记录Id
    id: Optional[int] = None
    # 充值金额
    amount: float
    # 赠送金额
    give: float


class RechargeOptionsForm(BaseModel):
    # 机器人ID
    robot_id: int
    # 选项内容
    opntis: List[RechargeOptionForm]


class ChannelForm(BaseModel):
    link: str

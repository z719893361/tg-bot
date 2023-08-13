import datetime

from sqlalchemy import Column, Integer, BIGINT, VARCHAR, TEXT, Numeric, SMALLINT, DATETIME, UniqueConstraint
from telegram.constants import ParseMode

from db.database import Base, engine
from typing import Union
from decimal import Decimal


class RobotModel(Base):
    """
    机器人信息表
    """
    __tablename__ = "robots"
    id = Column(Integer, primary_key=True, autoincrement=True)
    robot_id = Column(BIGINT, unique=True, comment="机器人ID")
    name = Column(VARCHAR(255), comment="机器人名称")
    token = Column(VARCHAR(255), comment="Token")


class WalletModel(Base):
    """
    钱包地址表
    """
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    robot_id = Column(BIGINT, unique=True, comment="机器人ID")
    address = Column(VARCHAR(255), comment="钱包地址")
    expires = Column(Integer, default=1200, comment="订单有效时间")


class RechargeOptionModel(Base):
    """
    充值选项表
    """
    __tablename__ = "recharge_options"
    id = Column(Integer, primary_key=True, autoincrement=True)
    robot_id = Column(BIGINT, index=True, comment="关联robots.robot_id")
    amount = Column(Numeric(precision=16, scale=6), comment="充值选项")
    give = Column(Numeric(precision=16, scale=6), comment="赠送金额")


class UserModel(Base):
    """
    用户表
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT, unique=True, comment="用户ID")
    amount: Decimal = Column(Numeric(precision=16, scale=6), comment="用户余额")


class ChannelModel(Base):
    """
    频道表
    """
    __tablename__ = "channels"
    id = Column(Integer, primary_key=True, autoincrement=True)
    robot_id = Column(BIGINT, index=True, comment="机器人Id - 关联robots.robot_id字段")
    link = Column(VARCHAR(255), comment="频道链接")


class GroupModel(Base):
    """
    群组表
    """
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    robot_id = Column(BIGINT, unique=True, comment="机器人ID")
    link = Column(VARCHAR(255), comment="群链接")
    price: Decimal = Column(Numeric(16, 6), comment="进群价格")


class OrderModel(Base):
    """
    充值记录表, 用户和充值金额做关联，用于区分用户
    """
    __tablename__ = "recharge_orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    robot_id = Column(BIGINT, index=True, comment="机器人ID")
    user_id = Column(BIGINT, index=True, comment="用户ID")
    chat_id = Column(BIGINT, comment="聊天会话ID")
    message_id = Column(BIGINT, comment="消息ID")
    amount: Decimal = Column(Numeric(precision=16, scale=6), index=True, comment="交易金额")
    give: Decimal = Column(Numeric(precision=16, scale=6), comment="赠送金额")
    status = Column(SMALLINT, index=True, default=0, comment="交易状态, 0:未完成|1:已完成")
    create_time = Column(DATETIME, index=True, comment="创建时间", default=datetime.datetime.now)


class TemplateModel(Base):
    """
    消息模板表，用于设置回复消息时的内容
    """
    __tablename__ = 'message_templates'
    id = Column(Integer, primary_key=True, autoincrement=True)
    robot_id = Column(BIGINT, comment="机器人ID")
    name = Column(VARCHAR(255), comment="模板名称")
    content = Column(TEXT, comment="模板内容")
    parse_mode = Column(SMALLINT, default=0, comment="模板解析类型, 0:普通文本|1:MARKDOWN|2:HTML")

    # 定义唯一索引
    __table_args__ = (
        UniqueConstraint('robot_id', 'name', name='uq_robot_name'),
    )

    def get_parse_mode(self) -> Union[str, None]:
        return [None, ParseMode.MARKDOWN, ParseMode.HTML][self.parse_mode]


class AdPriceModel(Base):
    """
    发送广告价格表
    """
    __tablename__ = 'ad_price'
    id = Column(Integer, primary_key=True, autoincrement=True)
    robot_id = Column(BIGINT, comment='机器人ID')
    price: Decimal = Column(Numeric(16, 6), comment='价格')


class UserLoginModel(Base):
    """
    后台登录用户表
    """
    __tablename__ = 'login'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(255), index=True, comment="用户名")
    password = Column(VARCHAR(255), comment="密码")



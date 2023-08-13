from typing import List
from pydantic import BaseModel


class TemplateConstant:
    WELCOME_MESSAGE = 'welcome_message'
    RECHARGE_BUTTON_PROMPT = 'recharge_button_prompt'
    AMOUNT_SELECTED_PROMPT = 'amount_selected_prompt'
    USER_PROFILE = 'user_profile'
    ADVERTISEMENT_CONFIRMATION = 'advertisement_confirmation'
    ACTIVITY_NOTICE = 'activity_notice'
    INSUFFICIENT_BALANCE = 'insufficient_balance'
    ADVERTISEMENT_DETAILS = 'advertisement_details'
    VIP_GROUP_PROMPT = 'vip_group_prompt'
    ADVERTISEMENT_BUTTON = 'advertisement_button'


data = {
    "template": [
        {
            'name': 'welcome_message',
            'content': "欢迎使用自助机器人",
            'parse_mode': 0
        },
        {
            'name': 'recharge_button_prompt',
            'content': "请选择余额：",
            'parse_mode': 0
        },
        {
            'name': 'amount_selected_prompt',
            'content': '*转账地址，注意小数*\n`{{address}}`\n\n*注意小数点* `{{"%.3f" | format(amount)}}` *USDT 注意小数点*\n\n*充值时间：{{ create_time.strftime("%Y-%m-%d %H:%M:%S") }}*\n*请在{{ expires_seconds//60 }}分钟内完成付款，转错不认*\n*收款地址为USDT-TRC20*\n*转账10分钟后没到账联系客服处理>>*[客服地址](https://t.me/fakadb_bot)',
            'parse_mode': 1
        },
        {
            'name': 'user_profile',
            'content': "用户ID：{{user_id}}\n姓氏：{{nickname}}\n用户名：{{username}}\nUSDT余额：{{amount}}",
            'parse_mode': 0
        },
        {
            'name': 'advertisement_confirmation',
            'content': "发布将在审核后,收费:{{\"%.2f\" | format(push_ad_price)}}USDT？\n确定发布吗？",
            'parse_mode': 0
        },
        {
            'name': 'activity_notice',
            'content': "没有活动",
            'parse_mode': 0
        },
        {
            'name': 'insufficient_balance',
            'content': "余额不足,请充值",
            'parse_mode': 0
        },
        {
            'name': 'advertisement_details',
            'content': '*项目名称：{{project_name}}*\n*项目介绍：{{project_desc}}*\n*联系人：{{project_contact}}*\n*价格：{{project_price}}*\n*频道：{{project_channel}}*\n\n👉[查看发布人](https://t.me/@{{publisher}})',
            'parse_mode': 1
        },
        {
            'name': 'vip_group_prompt',
            'content': "加入VIP群\n收费:{{'%.3f' | format(price)}} USDT",
            'parse_mode': 0
        },
        {
            'name': 'advertisement_button',
            'content': "按钮1 - http://www.example.com | 按钮2 - http://www.example.com\n按钮3 - http://www.example.com",
            'parse_mode': 0
        }
    ],
    "group": {
        "link": "https://t.me/join_group_test",
        "price": 10
    },
    "recharge_option": [
        {
            "amount": 5,
            "give": 0
        },
        {
            "amount": 10,
            "give": 0
        },
        {
            "amount": 30,
            "give": 0
        },
        {
            "amount": 50,
            "give": 0
        }
    ],
    "wallet": {
        "address": "TP5oszNDkVnS7J9MXE8ZyNCeyPixeUNwhq",
        "expires": 1200
    },
    "advertisement_fee": 6
}


# 定义模板模型
class RechargeOption(BaseModel):
    amount: int
    give: int


# 定义钱包模型
class Wallet(BaseModel):
    address: str
    expires: int


class Group(BaseModel):
    link: str
    price: int


class Template(BaseModel):
    name: str
    content: str
    parse_mode: int


class AppData(BaseModel):
    template: List[Template]
    group: Group
    recharge_option: List[RechargeOption]
    wallet: Wallet
    advertisement_fee: int


default_data = AppData.model_validate(data)

import logging
from admin.app import app

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] - %(message)s",  # 设置日志消息格式
    datefmt="%Y-%m-%d %H:%M:%S"  # 设置日期时间格式
)

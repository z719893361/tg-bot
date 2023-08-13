from pydantic import BaseModel


class LoginForm(BaseModel):
    # 用户名
    username: str
    # 密码
    password: str

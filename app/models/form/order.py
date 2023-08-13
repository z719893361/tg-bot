from pydantic import BaseModel


class OrderForm(BaseModel):
    robot_id: int
    user_id: int
    chat_id: int
    message_id: int
    amount: float
    give: float
    status: int


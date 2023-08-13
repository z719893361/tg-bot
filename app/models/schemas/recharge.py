from pydantic import BaseModel


class RechargeSchema(BaseModel):
    id: int
    amount: float
    give: float


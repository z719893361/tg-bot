from pydantic import BaseModel


class RobotCreateFrom(BaseModel):
    name: str
    token: str


class RobotUpdateFrom(RobotCreateFrom):
    id: int


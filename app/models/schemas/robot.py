from pydantic import BaseModel


class RobotSchema(BaseModel):
    id: int
    robot_id: int
    name: str
    token: str


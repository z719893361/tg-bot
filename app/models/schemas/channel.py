from pydantic import BaseModel


class ChannelSchema(BaseModel):
    id: int
    link: str

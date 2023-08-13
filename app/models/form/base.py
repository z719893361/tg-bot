from typing import List
from pydantic import BaseModel


class IdsForm(BaseModel):
    ids: List[int]


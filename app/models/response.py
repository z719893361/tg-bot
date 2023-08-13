from typing import Generic, TypeVar, Union
from pydantic import BaseModel

T = TypeVar('T')


class Result(BaseModel, Generic[T]):
    status: int
    message: Union[str, None] = None
    data: T = None

    @classmethod
    def ok(cls, message: str = None, data: T = None):
        return cls(status=0, message=message, data=data)

    @classmethod
    def error(cls, message: str = None):
        return cls(status=400, message=message)

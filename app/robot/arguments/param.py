from typing import Optional, Callable, Any


class Depends:
    def __init__(self,  dependency: Optional[Callable[..., Any]]):
        self.dependency = dependency

    def __repr__(self) -> str:
        attr = getattr(self.dependency, "__name__", type(self.dependency).__name__)
        return f"{self.__class__.__name__}({attr})"


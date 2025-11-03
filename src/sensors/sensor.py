from abc import ABC, abstractmethod
from typing import Any


class Sensor(ABC):
    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def get_value(self) -> Any:
        pass

    def __str__(self) -> str:
        return self.__class__.__name__

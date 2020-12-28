from abc import ABC, abstractmethod
from typing import List

from models.Rules import Rules


class Field(ABC):
    def __init__(self, width: int, height: int, rules: Rules) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.rules = rules

    @abstractmethod
    def set_point(self, value: bool, x: int, y: int) -> None:
        pass

    @abstractmethod
    def get_point(self, x: int, y: int) -> bool:
        pass

    @abstractmethod
    def get_neighbourhood(self, x: int, y: int) -> List[bool]:
        pass

    @abstractmethod
    def get_alive_neighbours_count(self, x: int, y: int) -> int:
        pass

    @abstractmethod
    def step(self):
        pass

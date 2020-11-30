from abc import ABC, abstractmethod
from typing import List

from rules import Rules


# class Field(ABC):
#     def __init__(self, width: int, height: int, rules: Rules) -> None:
#         super().__init__()
#         self.width = width
#         self.height = height
#         self.rules = rules
#
#     @abstractmethod
#     def set_point(self, value: bool, x: int, y: int) -> None:
#         pass
#
#     @abstractmethod
#     def get_point(self, x: int, y: int) -> bool:
#         pass
#
#     @abstractmethod
#     def get_neighbourhood(self, x: int, y: int) -> List[bool]:
#         pass
#
#     @abstractmethod
#     def get_alive_neighbours_count(self, x: int, y: int) -> int:
#         pass
#
#     @abstractmethod
#     def step(self):
#         pass


# class SimpleField(Field):
#     """ Поле фиксированного размера. Не умеет работать с маской соседей """
#     def __init__(self, width: int, height: int) -> None:
#         super().__init__(width, height)
#         self.width = width
#         self.height = height
#         self.map = [list([False] * width) for i in range(0, height)]
#
#     def set_point(self, value: bool, x: int, y: int) -> None:
#         if 0 <= x < self.width and 0 <= y < self.height:
#             self.map[y][x] = value
#
#     def get_point(self, x: int, y: int) -> bool:
#         if 0 <= x < self.width and 0 <= y < self.height:
#             return self.map[y][x]
#
#     def get_neighbourhood(self, x: int, y: int) -> List[bool]:
#         """
#         Получить список состояний соседних клеток
#
#         :param x: координата x центральной клетки
#         :param y: координата y центральной клетки
#         :return: Список от 3 до 8 соседних клеток
#         """
#         if 0 <= x < self.width and 0 <= y < self.height:
#             return [self.get_point(x + i, y + j) for j in range(-1, 2) for i in range(-1, 2)
#                     if (j != 0 or i != 0) and 0 <= y + j < self.height and 0 <= x + i < self.width]
#
#     def get_alive_neighbours_count(self, x: int, y: int, mask: List[int]) -> int:
#         return sum(1 for point in self.get_neighbourhood(x, y) if point)


class BorderedField:
    """ Поле фиксированного размера, окруженное со всех сторон дополнительной границей из вечно "мёртвых" клеток """
    def __init__(self, width: int, height: int, rules: Rules) -> None:
        self.width = width
        self.height = height
        self.rules = rules
        self.field = [list([False] * (width + 2)) for i in range(0, height + 2)]

    def set_point(self, value: bool, x: int, y: int, field=None) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            if field is not None:
                field[y + 1][x + 1] = value
            else:
                self.field[y + 1][x + 1] = value

    def get_point(self, x: int, y: int) -> bool:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.field[y + 1][x + 1]
        else:
            return False

    def inverse_point(self, x: int, y: int):
        new_value = not bool(self.get_point(x, y))
        self.set_point(new_value, x, y)
        return new_value

    def get_neighbourhood(self, x: int, y: int) -> List[bool]:
        """
        Получить список состояний восьми соседних клеток

        :param x: координата x центральной клетки
        :param y: координата y центральной клетки
        :return: Список значений соседних клеток. Индексы массива соответствуют следующим клеткам окрестности
            0 1 2
            3 Х 4
            5 6 7
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return [self.get_point(x + i, y + j) for j in range(-1, 2) for i in range(-1, 2) if j != 0 or i != 0]

    def get_alive_neighbours_count(self, x: int, y: int) -> int:
        # print(self.get_neighbourhood(x, y))
        return sum(point for i, point in enumerate(self.get_neighbourhood(x, y)) if self.rules.mask[i])

    def step(self):
        new_field = [list([False] * len(self.field[0])) for i in range(len(self.field))]
        for j in range(self.height):
            for i in range(self.width):
                neighbours_count = self.get_alive_neighbours_count(i, j)
                # print(neighbours_count)
                if self.get_point(i, j):
                    # клетка живая
                    print(neighbours_count)
                    print(self.rules.is_survived(neighbours_count))
                    self.set_point(self.rules.is_survived(neighbours_count), i, j, new_field)
                else:
                    # клетка не живая
                    self.set_point(self.rules.was_born(neighbours_count), i, j, new_field)
        self.field = new_field

    def print(self):
        for j in range(len(self.field)):
            print(self.field[j])




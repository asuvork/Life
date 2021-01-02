import random
from typing import List

from models.Rules import Rules


class BorderedField:
    """ Поле фиксированного размера, окруженное со всех сторон дополнительной границей из вечно "мёртвых" клеток """
    def __init__(self, width: int, height: int, rules: Rules) -> None:
        self.width = width
        self.height = height
        self.rules = rules
        self.field = self.get_empty_field()

    def get_empty_field(self):
        return [list([False] * (self.width + 2)) for _ in range(self.height + 2)]

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

    def inverse_point(self, x: int, y: int) -> bool:
        new_value = not bool(self.get_point(x, y))
        self.set_point(new_value, x, y)
        return new_value

    def get_field(self):
        # print(self.width, self.height)
        # print(self.field)
        return [self.field[i][1:-1] for i in range(1, self.height + 1)]

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
        new_field = self.get_empty_field()
        for j in range(self.height):
            for i in range(self.width):
                neighbours_count = self.get_alive_neighbours_count(i, j)
                # print(neighbours_count)
                if self.get_point(i, j):
                    # клетка живая
                    self.set_point(self.rules.is_survived(neighbours_count), i, j, new_field)
                else:
                    # клетка не живая
                    self.set_point(self.rules.was_born(neighbours_count), i, j, new_field)
        self.field = new_field

    def print(self):
        for j in range(len(self.field)):
            print(self.field[j])

    def randomize(self, border):
        for i in range(1, self.height + 1):
            self.field[i][1:-1] = [1 if random.randint(0, 100) >= border else 0 for _ in range(self.width)]


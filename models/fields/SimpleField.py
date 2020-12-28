from typing import List


class SimpleField:
    """ Поле фиксированного размера. Не умеет работать с маской соседей """
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.width = width
        self.height = height
        self.map = [list([False] * width) for i in range(0, height)]

    def set_point(self, value: bool, x: int, y: int) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            self.map[y][x] = value

    def get_point(self, x: int, y: int) -> bool:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.map[y][x]

    def get_neighbourhood(self, x: int, y: int) -> List[bool]:
        """
        Получить список состояний соседних клеток

        :param x: координата x центральной клетки
        :param y: координата y центральной клетки
        :return: Список от 3 до 8 соседних клеток
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return [self.get_point(x + i, y + j) for j in range(-1, 2) for i in range(-1, 2)
                    if (j != 0 or i != 0) and 0 <= y + j < self.height and 0 <= x + i < self.width]

    def get_alive_neighbours_count(self, x: int, y: int, mask: List[int]) -> int:
        return sum(1 for point in self.get_neighbourhood(x, y) if point)
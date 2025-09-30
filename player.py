"""Класс игрока (голова змейки)."""

import arcade

from config import CELL_SIZE, GRID_HEIGHT, GRID_WIDTH, SNAKE_HEAD_COLOR


class Player:
    """Класс игрока (голова змейки).

    Отвечает за положение, направление и отрисовку головы.
    Позиции хранятся в координатах клеток (integers).
    """

    def __init__(self, x: int, y: int) -> None:
        """Инициализация игрока (головы змейки)."""
        self.x = x
        self.y = y
        self.dx = 1
        self.dy = 0

    def set_direction(self, dx: int, dy: int) -> None:
        """Изменить направление движения."""
        self.dx = dx
        self.dy = dy

    def update(self) -> None:
        """Переместить голову на одну клетку в направлении."""
        self.x += self.dx
        self.y += self.dy

    def draw(self) -> None:
        """Нарисовать квадрат игрока (головы змейки)."""
        px = self.x * CELL_SIZE
        py = self.y * CELL_SIZE
        arcade.draw_lbwh_rectangle_filled(
            px,
            py,
            CELL_SIZE,
            CELL_SIZE,
            SNAKE_HEAD_COLOR,
        )

    def out_of_bounds(self) -> bool:
        """Проверяет, вышел ли игрок за границы игрового поля."""
        return not (0 <= self.x < GRID_WIDTH and 0 <= self.y < GRID_HEIGHT)

    def get_pos(self) -> tuple:
        """Возвращает координаты игрока (головы змейки)."""
        return (self.x, self.y)

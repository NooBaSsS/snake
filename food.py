"""Класс еды."""

import random

import arcade

from config import CELL_SIZE, FOOD_COLOR, GRID_HEIGHT, GRID_WIDTH


class Food:
    """Класс еды (единичный элемент)."""

    def __init__(self, forbidden_positions: set) -> None:
        """Инициализация еды."""
        self.x = 0
        self.y = 0
        self.reposition(forbidden_positions)

    def reposition(self, forbidden_positions: set) -> None:
        """Поместить еду в случайную клетку, не совпадающую с forbidden_positions."""  # noqa: RUF002
        attempts = 0
        while True:
            attempts += 1
            self.x = random.randrange(0, GRID_WIDTH)  # noqa: S311
            self.y = random.randrange(0, GRID_HEIGHT)  # noqa: S311
            if (self.x, self.y) not in forbidden_positions:
                break

    def draw(self) -> None:
        """Отрисовка еды."""
        px = self.x * CELL_SIZE + CELL_SIZE / 2
        py = self.y * CELL_SIZE + CELL_SIZE / 2
        arcade.draw_circle_filled(px, py, CELL_SIZE * 0.45, FOOD_COLOR)

    def get_pos(self) -> tuple:
        """Возвращает координаты еды."""
        return (self.x, self.y)

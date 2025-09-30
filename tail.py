"""Класс хвоста змейки."""

import arcade

from config import CELL_SIZE, SNAKE_TAIL_COLOR


class Tail:
    """Класс хвоста змейки.

    Хранит список сегментов в виде списка позиций (x, y) в клетках.
    Последний элемент списка — ближайший к голове сегмент.
    """

    def __init__(self, initial_length: int = 3) -> None:
        """Инициализация хвоста."""
        self.segments = []
        self.target_length = initial_length

    def prepend_head_pos(self, head_pos: tuple) -> None:
        """Добавляем сегмент в начало хвоста."""
        self.segments.insert(0, head_pos)
        # обрезаем хвост
        if len(self.segments) > self.target_length:
            self.segments = self.segments[: self.target_length]

    def grow(self, amount: int = 1) -> None:
        """Увеличиваем цель длины хвоста — при поедании еды."""
        self.target_length += amount

    def draw(self) -> None:
        """Отрисовка сегментов хвоста."""
        for x, y in self.segments:
            px = x * CELL_SIZE
            py = y * CELL_SIZE
            arcade.draw_lbwh_rectangle_filled(
                px,
                py,
                CELL_SIZE,
                CELL_SIZE,
                SNAKE_TAIL_COLOR,
            )

    def collides_with(self, pos: tuple) -> bool:
        """Проверяем, перекрыл ли хвост позицию pos (x,y)."""
        return pos in self.segments

    def get_segments(self) -> list:
        """Возвращает список сегментов хвоста."""
        return list(self.segments)

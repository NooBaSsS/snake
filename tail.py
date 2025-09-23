"""Хвост."""

import pygame as pg

import config


class Tail:
    """Хвост."""

    def __init__(self, cell_size: int) -> None:
        """Инициализация."""
        self.cell_size = cell_size
        self.segments = []  # список клеток (x, y)

    def follow(self, new_head_pos: tuple) -> None:
        """Следование голове."""
        if self.segments:
            self.segments.insert(0, new_head_pos)
            self.segments.pop()

    def grow(self, new_segment: tuple) -> None:
        """Добавление сегмента."""
        self.segments.append(new_segment)

    def draw(self, surface: pg.Surface) -> None:
        """Отрисовка."""
        for x, y in self.segments:
            rect = pg.Rect(
                x * self.cell_size,
                y * self.cell_size,
                self.cell_size,
                self.cell_size,
            )
            pg.draw.rect(surface, config.RED, rect)

    def get_segments(self) -> tuple[int, int]:
        """Получение сегментов."""
        return self.segments

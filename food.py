"""Еда."""

import random

import pygame as pg

import config


class Food(pg.sprite.Sprite):
    """Еда на поле."""

    def __init__(
        self,
        exclude: list[tuple[int, int]],
        cells: list[tuple[int, int]],
    ) -> None:
        """Инициализация."""
        super().__init__()
        self.cell_size = config.CELL_SIZE
        self.image = pg.Surface((self.cell_size, self.cell_size))
        self.image.fill(config.RED)
        self.rect = self.image.get_rect()
        self.position = self.random_position(exclude, cells)
        self.update_rect()

    def random_position(
        self,
        exclude: list[tuple],
        cells: list[tuple[int, int]],
    ) -> tuple[int, int]:
        """Генерация случайной позиции на сетке, исключая занятые клетки."""
        free_cells = [cell for cell in cells if cell not in exclude]
        return random.choice(free_cells)  # noqa: S311

    def respawn(self, exclude: list[tuple], cells: list[tuple[int, int]]) -> None:
        """Перемещает еду в новую случайную позицию."""
        self.position = self.random_position(exclude, cells)
        self.update_rect()

    def update_rect(self) -> None:
        """Обновление rect для отрисовки на экране."""
        self.rect.topleft = (
            self.position[0] * self.cell_size,
            self.position[1] * self.cell_size,
        )

    def get_pos(self) -> tuple[int, int]:
        """Получение позиции."""
        return self.position

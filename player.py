"""Игрок."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

import config

if TYPE_CHECKING:
    from tail import Tail


class Player(pg.sprite.Sprite):
    """Игрок."""

    def __init__(self) -> None:
        """Инициализация."""
        super().__init__()
        self.start_pos = config.PLAYER_START_POS
        self.cell_size = config.CELL_SIZE
        self.image = pg.Surface((self.cell_size, self.cell_size))
        self.image.fill(config.GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (
            self.start_pos[0] * self.cell_size,
            self.start_pos[1] * self.cell_size,
        )

        self.grid_pos = self.start_pos
        self.direction = (1, 0)

    def handle_keys(self, event: pg.event.Event) -> None:
        """Обработка нажатия клавиш."""
        if event.key == config.K_UP:  # FIX: запретить разворот
            self.set_direction((0, -1))
        elif event.key == config.K_DOWN:
            self.set_direction((0, 1))
        elif event.key == config.K_LEFT:
            self.set_direction((-1, 0))
        elif event.key == config.K_RIGHT:
            self.set_direction((1, 0))

    def set_direction(self, new_dir: tuple) -> None:
        """Изменение направления."""
        dx, dy = new_dir
        cur_dx, cur_dy = self.direction
        if (dx, dy) != (-cur_dx, -cur_dy):
            self.direction = new_dir

    def move(self) -> None:
        """Перемещение."""
        x, y = self.grid_pos
        dx, dy = self.direction
        self.grid_pos = (x + dx, y + dy)
        self.rect.topleft = (
            self.grid_pos[0] * self.cell_size,
            self.grid_pos[1] * self.cell_size,
        )

    def check_collision(self, tail: Tail, food: tuple) -> int:
        """Проверка столкновения."""
        x, y = self.grid_pos
        cell_width = config.CELL_WIDTH
        cell_height = config.CELL_HEIGHT
        if x < 0 or x >= cell_width or y < 0 or y >= cell_height:
            return -1  # выход за пределы
        if (x, y) in tail.get_segments():
            return -1  # столкновение с хвостом  # noqa: RUF003
        if (x, y) == food:
            return 1  # еда
        return 0

    def get_pos(self) -> tuple[int, int]:
        """Получение позиции."""
        return self.grid_pos

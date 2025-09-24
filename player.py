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

    def handle_keys(self) -> bool:
        """Обработка нажатия клавиш."""
        for event in pg.event.get():  # FIX: запретить разворот
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN:
                if event.key in (config.K_QUIT, config.K_Q):
                    return False
                if event.key == config.K_UP:
                    self.set_direction((0, -1))
                elif event.key == config.K_DOWN:
                    self.set_direction((0, 1))
                elif event.key == config.K_LEFT:
                    self.set_direction((-1, 0))
                elif event.key == config.K_RIGHT:
                    self.set_direction((1, 0))
        return True

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
        # TODO: комментарий к кодам
        x, y = self.grid_pos
        cell_width = config.CELL_WIDTH
        cell_height = config.CELL_HEIGHT
        if x < 0 or x >= cell_width or y < 0 or y >= cell_height:
            return -1
        if (x, y) in tail.get_segments():
            return -1
        if (x, y) == food:
            return 1
        return 0

    def get_pos(self) -> tuple[int, int]:
        """Получение позиции."""
        return self.grid_pos

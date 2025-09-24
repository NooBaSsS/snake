"""Основной модуль."""

import sys

import pygame as pg

import config
from food import Food
from player import Player
from tail import Tail


def main() -> None:
    """Основная функция."""
    pg.init()
    cell_size = config.CELL_SIZE
    grid_width, grid_height = (config.CELL_WIDTH, config.CELL_HEIGHT)
    screen = pg.display.set_mode((grid_width * cell_size, grid_height * cell_size))
    clock = pg.time.Clock()
    cells = []

    for col in range(config.CELL_WIDTH):
        for row in range(config.CELL_HEIGHT):
            cells.append((col, row))  # noqa: PERF401

    player = Player()
    tail = Tail(cell_size=cell_size)
    food = Food(exclude=(player.get_pos(), tail.get_segments()), cells=cells)

    all_sprites = pg.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(food)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key in (config.K_QUIT, config.K_Q):
                    running = False
                else:
                    player.handle_keys(event=event)

        old_pos = player.grid_pos
        player.move()
        tail.follow(old_pos)
        if player.check_collision(tail, food.get_pos()) == -1:
            print("Game Over")
            running = False
        elif player.check_collision(tail, food.get_pos()) == 1:
            tail.grow(player.grid_pos)
            food.respawn(exclude=(player.get_pos(), tail.get_segments()), cells=cells)

        screen.fill(config.GAME_BG_COLOR)
        tail.draw(screen)
        all_sprites.draw(screen)
        pg.display.flip()

        clock.tick(config.FPS)

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()

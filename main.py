"""Змейка."""

import arcade

from config import (
    BG_COLOR,
    CELL_SIZE,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    SCREEN_WIDTH,
    SNAKE_FPS,
)
from food import Food
from player import Player
from tail import Tail


class SnakeGame(arcade.Window):
    """Основное окно игры."""

    def __init__(self) -> None:
        """Инициализация окна."""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(BG_COLOR)
        self.reset()

    def reset(self) -> None:
        """Сброс состояния игры."""  # noqa: RUF002
        start_x = (SCREEN_WIDTH // CELL_SIZE) // 2
        start_y = (SCREEN_HEIGHT // CELL_SIZE) // 2
        self.player = Player(start_x, start_y)
        self.tail = Tail(initial_length=3)
        self.food = Food(forbidden_positions={self.player.get_pos()})
        self.game_over = False

        self.prev_dx = self.player.dx
        self.prev_dy = self.player.dy

        self.move_interval = 1.0 / SNAKE_FPS
        self.time_since_move = 0.0

    def on_draw(self) -> None:
        """Рисование окна."""
        self.clear()
        self.food.draw()
        self.tail.draw()
        self.player.draw()
        if self.game_over:
            arcade.draw_text(
                "Game Over — press R to restart",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.WHITE,
                20,
                anchor_x="center",
                anchor_y="center",
            )

    def on_update(self, delta_time: float) -> None:
        """Обновление состояния игры."""
        if self.game_over:
            return

        self.time_since_move += delta_time
        if self.time_since_move < self.move_interval:
            return

        self.time_since_move = 0

        old_pos = self.player.get_pos()
        self.player.update()

        if self.player.out_of_bounds():
            self.end_game()
            return

        if self.tail.collides_with(self.player.get_pos()):
            self.end_game()
            return

        self.tail.prepend_head_pos(old_pos)

        if self.player.get_pos() == self.food.get_pos():
            self.tail.grow(1)
            forbidden = set(self.tail.get_segments())
            forbidden.add(self.player.get_pos())
            self.food.reposition(forbidden)

        self.prev_dx = self.player.dx
        self.prev_dy = self.player.dy

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            arcade.exit()
            return

        if self.game_over:
            if symbol == arcade.key.R:
                self.reset()
            return

        dir_map = {
            arcade.key.UP: (0, 1),
            arcade.key.W: (0, 1),
            arcade.key.DOWN: (0, -1),
            arcade.key.S: (0, -1),
            arcade.key.LEFT: (-1, 0),
            arcade.key.A: (-1, 0),
            arcade.key.RIGHT: (1, 0),
            arcade.key.D: (1, 0),
        }
        if symbol in dir_map:
            dx, dy = dir_map[symbol]
            if (dx, dy) == (-self.prev_dx, -self.prev_dy):
                return
            self.player.set_direction(dx, dy)

    def end_game(self) -> None:
        """Завершение игры."""
        self.game_over = True
        arcade.unschedule(self.on_update)


def main() -> None:
    """Запуск игры."""
    SnakeGame()
    arcade.run()


if __name__ == "__main__":
    main()

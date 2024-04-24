import tkinter
import random

WINDOW_BG = 'black'
CANVAS_BG = 'white'
TILE_SIZE = 100
LINE_COLOR = 'black'
SNAKE_COLOR = 'green'
FOOD_COLOR = 'green'
SECTION_COLOR = 'grey'
MENU_TEXT_COLOR = 'black'
MENU_FONT_NAME = 'Impact'
FPS = 5


class App:
    def __init__(self) -> None:
        self.window = tkinter.Tk()
        self.window.attributes('-fullscreen', True)
        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()
        self.window['bg'] = WINDOW_BG
        self.canvas = tkinter.Canvas(
            self.window,
            width=self.width // TILE_SIZE * TILE_SIZE,
            height=self.height // TILE_SIZE * TILE_SIZE,
            bg=CANVAS_BG,
            highlightthickness=0
        )
        self.canvas.pack(expand=True)
        self.canvas.update()
        self.draw_lines()
        self.game = Game(
            self.canvas,
            'Up',
            'Down',
            'Left',
            'Right',
        )
        self.window.mainloop()

    def draw_lines(self) -> None:
        for i in range(1, self.width // TILE_SIZE):
            self.canvas.create_line(
                i * TILE_SIZE,
                0,
                i * TILE_SIZE,
                self.height,
                fill=LINE_COLOR
            )
        for i in range(1, self.height // TILE_SIZE):
            self.canvas.create_line(
                0,
                i * TILE_SIZE,
                self.width,
                i * TILE_SIZE,
                fill=LINE_COLOR,
            )


class Game:
    def __init__(self,
                 canvas: tkinter.Canvas,
                 key_up: str,
                 key_down: str,
                 key_left: str,
                 key_right: str,
                 ) -> None:
        self.key_up = key_up
        self.key_down = key_down
        self.key_left = key_left
        self.key_right = key_right
        self.canvas = canvas
        self.canvas.bind('<Key>', self.on_key)
        self.canvas.focus_set()
        self.cols = self.canvas.winfo_width() // TILE_SIZE
        self.rows = self.canvas.winfo_height() // TILE_SIZE
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()
        self.snake = None
        self.is_running = 0
        self.food = None
        self.last_key = None
        self.show_menu()

    def show_menu(self) -> None:
        self.canvas.create_text(
            self.width // 2,
            self.height // 2,
            text='Enter - играть \n Esc - выйти',
            fill=MENU_TEXT_COLOR,
            font=(MENU_FONT_NAME, int(min((self.width, self.height)) * 0.23)),
            justify='center',
        )

    def start(self) -> None:
        self.food = Food(
                self.canvas,
                2,
                2,
                FOOD_COLOR
            )
        self.snake = Snake(
            self.cols // 2,
            self.rows // 2,
            self.canvas,
            SNAKE_COLOR,
            'Up',
            'Down',
            'Left',
            'Right',
        )
        self.canvas.delete(self.snake.tag, self.food.tag)
        self.update()

    def update(self) -> None:
        self.last_direction = None
        if not self.food:
            col = random.randint(0, self.cols - 1)
            row = random.randint(0, self.rows - 1)
            self.food = Food(
                self.canvas,
                col,
                row,
                FOOD_COLOR
            )
        self.food.draw()
        self.snake.change_direction()
        self.snake.collide_borders()
        self.snake.draw()
        self.snake.collide_body()
        self.snake.eat_food(self)
        if self.snake.is_active:
            self.snake.move()
            self.canvas.after(1000 // FPS, self.update)
        else:
            self.is_running = 0
            self.show_menu()

    def on_key(self, event: tkinter.Event) -> None:
        if event.keysym == 'Escape':
            self.canvas.winfo_toplevel().destroy()
        elif event.keysym == 'Return':
            if not self.is_running:
                self.start()
        else:
            self.snake.last_key = event.keysym


class Snake:
    def __init__(
            self,
            col: int,
            row: int,
            canvas: tkinter.Canvas,
            color: str,
            key_up: str,
            key_down: str,
            key_left: str,
            key_right: str,
    ) -> None:
        self.key_up = key_up
        self.key_down = key_down
        self.key_left = key_left
        self.key_right = key_right
        self.col = col
        self.row = row
        self.color = color
        self.canvas = canvas
        self.last_key = None
        self.direction = (1, 0)
        self.max_col = self.canvas.winfo_width() // TILE_SIZE
        self.max_row = self.canvas.winfo_height() // TILE_SIZE
        self.tag = 'snake'
        self.body = []
        self.is_active = 1

    def draw(self) -> None:
        self.canvas.delete('snake')
        for section in self.body:
            self.canvas.create_rectangle(
                section[0] * TILE_SIZE,
                section[1] * TILE_SIZE,
                section[0] * TILE_SIZE + TILE_SIZE,
                section[1] * TILE_SIZE + TILE_SIZE,
                fill=SECTION_COLOR,
                tags=self.tag
            )

        self.canvas.create_rectangle(
            self.col * TILE_SIZE,
            self.row * TILE_SIZE,
            self.col * TILE_SIZE + TILE_SIZE,
            self.row * TILE_SIZE + TILE_SIZE,
            fill=self.color,
            tags='snake'
        )

    def change_direction(self) -> None:
        if self.last_key == self.key_right:
            new_direction = (1, 0)
        elif self.last_key == self.key_left:
            new_direction = (-1, 0)
        elif self.last_key == self.key_up:
            new_direction = (0, -1)
        elif self.last_key == self.key_down:
            new_direction = (0, 1)
        else:
            return

        if self.direction[0] == -new_direction[0]:
            return
        if self.direction[1] == -new_direction[1]:
            return
        self.direction = new_direction
        self.last_key = None

    def move(self) -> None:
        if not self.is_active:
            return
        if self.body:
            self.body = [(self.col, self.row)] + self.body[:-1]
        self.col += self.direction[0]
        self.row += self.direction[1]

    def collide_borders(self) -> None:
        self.canvas.update()
        if self.col >= self.max_col:  # справа
            self.canvas['bg'] = 'red'
            self.is_active = 0
        if self.row >= self.max_row:  # снизу
            self.canvas['bg'] = 'red'
            self.is_active = 0
        if self.col <= -1:  # слева
            self.canvas['bg'] = 'red'
            self.is_active = 0
        if self.row <= -1:  # снизу
            self.canvas['bg'] = 'red'
            self.is_active = 0

    def collide_body(self) -> None:
        if (self.col, self.row) in self.body:
            self.is_active = 0

    def eat_food(self, game: Game) -> None:
        if self.col == game.food.col:
            if self.row == game.food.row:
                self.body.append((game.food.col, game.food.row))
                self.canvas.delete(game.food.tag)
                game.food = None


class Food:
    def __init__(
            self,
            canvas: tkinter.Canvas,
            col: int,
            row: int,
            color: str,
    ) -> None:
        self.canvas = canvas
        self.col = col
        self.row = row
        self.color = color
        self.tag = 'food'

    def draw(self) -> None:
        self.canvas.create_rectangle(
            self.col * TILE_SIZE,
            self.row * TILE_SIZE,
            self.col * TILE_SIZE + TILE_SIZE,
            self.row * TILE_SIZE + TILE_SIZE,
            fill=self.color,
            tags='food'
        )


App()

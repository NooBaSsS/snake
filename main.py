import tkinter
import random

WINDOW_BG = 'black'
CANVAS_BG = 'white'
TILE_SIZE = 100
LINE_COLOR = 'black'
SNAKE_COLOR = 'red'
FOOD_COLOR = 'green'
SECTION_COLOR = 'grey'
FPS = 5


class App:
    def __init__(self) -> None:
        self.window = tkinter.Tk()
        self.window.attributes('-fullscreen', True)
        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()
        self.window.bind('<Key>', self.on_key)
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

    def on_key(self, event: tkinter.Event) -> None:
        if event.keysym == 'Escape':
            self.window.destroy()
        else:
            self.game.on_key(event)

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
        self.cols = self.canvas.winfo_width() // TILE_SIZE
        self.rows = self.canvas.winfo_height() // TILE_SIZE
        self.snake = Snake(
            self.cols // 2,
            self.rows // 2,
            canvas,
            SNAKE_COLOR,
        )
        self.food = None
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
        # self.snake.change_direction(self.last_direction)
        self.snake.collide_borders()
        self.snake.draw()
        self.snake.collide_body()
        self.snake.eat_food(self)
        if self.snake.is_active:
            self.snake.move()
            self.canvas.after(1000 // FPS, self.update)

    def on_key(self, event: tkinter.Event) -> None:
        if event.keysym == self.key_right:
            self.last_direction = (1, 0)
        if event.keysym == self.key_left:
            self.last_direction = (-1, 0)
        if event.keysym == self.key_up:
            self.last_direction = (0, -1)
        if event.keysym == self.key_down:
            self.last_direction = (0, 1)


class Snake:
    def __init__(
            self,
            col: int,
            row: int,
            canvas: tkinter.Canvas,
            color: str,
    ) -> None:
        self.col = col
        self.row = row
        self.color = color
        self.canvas = canvas
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

    def change_direction(self, direction) -> None:
        if self.direction[0] == direction[0] * -1:
            return
        if self.direction[1] == direction[1] * -1:
            return
        self.direction = direction

    def move(self) -> None:
        if not self.is_active:
            return
        if self.body:
            self.body = [(self.col, self.row)] + self.body[:-1]
        self.col += self.direction[0]
        self.row += self.direction[1]

    def collide_borders(self) -> None:
        self.canvas.update()
        '''
        text = tkinter.Text(self.canvas,
                            height=self.canvas.winfo_screenheight(),
                            width=self.canvas.winfo_screenwidth(),
                            bg='blue'
                            )
        label = tkinter.Label(text, text='', pady=100)
        label.config(font=('Arial', 56))
        label.pack()
        text.pack()
        input()
        '''
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

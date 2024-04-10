import tkinter

WINDOW_BG = 'black'
CANVAS_BG = 'white'
TILE_SIZE = 32
LINE_COLOR = 'black'
SNAKE_COLOR = 'red'
FPS = 3


class App:
    def __init__(self) -> None:
        self.window = tkinter.Tk()
        self.window.attributes('-fullscreen', True)
        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()
        self.canvas_side = min((self.height, self.width))
        self.tiles_ammount = self.canvas_side // TILE_SIZE
        self.window.bind('<Key>', self.on_key)
        self.window['bg'] = WINDOW_BG
        self.canvas = tkinter.Canvas(
            self.window,
            width=self.canvas_side,
            height=self.canvas_side,
            bg=CANVAS_BG,
            highlightthickness=0
        )
        self.canvas.pack()
        self.canvas.update()
        self.draw_lines()
        self.game = Game(self.canvas, self.tiles_ammount)
        self.window.mainloop()

    def on_key(self, event: tkinter.Event) -> None:
        if event.keysym == 'Escape':
            self.window.destroy()
        else:
            self.game.on_key(event)

    def draw_lines(self) -> None:
        for i in range(1, int(self.tiles_ammount)):
            self.canvas.create_line(
                i * TILE_SIZE,
                0,
                i * TILE_SIZE,
                self.height,
                fill=LINE_COLOR
            )
            self.canvas.create_line(
                0,
                i * TILE_SIZE,
                self.width,
                i * TILE_SIZE,
                fill=LINE_COLOR,
            )


class Game:
    def __init__(self, canvas: tkinter.Canvas, tiles_ammount: int) -> None:
        self.canvas = canvas
        self.size = tiles_ammount
        self.snake = Snake(
            self.size // 2,
            self.size // 2,
            TILE_SIZE,
            canvas,
            SNAKE_COLOR,
            'Up',
            'Down',
            'Left',
            'Right',
            self.size
        )
        self.update()

    def update(self) -> None:
        self.canvas.delete('snake')
        self.snake.collide_borders()
        self.snake.draw()
        if self.snake.is_active:
            self.snake.move()
            self.canvas.after(1000 // FPS, self.update)

    def on_key(self, event) -> None:
        self.snake.on_key(event)


class Snake:
    def __init__(
            self,
            col: int,
            row: int,
            size: int,
            canvas: tkinter.Canvas,
            color: str,
            key_up: str,
            key_down: str,
            key_left: str,
            key_right: str,
            tiles_ammount: int
    ) -> None:
        self.col = col
        self.row = row
        self.size = size
        self.color = color
        self.canvas = canvas
        self.key_up = key_up
        self.key_down = key_down
        self.key_left = key_left
        self.key_right = key_right
        self.direction = (1, 0)
        self.max_col = self.canvas.winfo_width() // TILE_SIZE
        self.max_row = self.canvas.winfo_height() // TILE_SIZE
        self.tiles_ammount = tiles_ammount
        self.is_active = 1

    def draw(self) -> None:
        self.canvas.create_rectangle(
            self.col * TILE_SIZE,
            self.row * TILE_SIZE,
            self.col * TILE_SIZE + self.size,
            self.row * TILE_SIZE + self.size,
            fill=self.color,
            tags='snake'
        )

    def on_key(self, event: tkinter.Event) -> None:
        if event.keysym == self.key_right:
            self.change_direction((1, 0))
        if event.keysym == self.key_left:
            self.change_direction((-1, 0))
        if event.keysym == self.key_up:
            self.change_direction((0, -1))
        if event.keysym == self.key_down:
            self.change_direction((0, 1))

    def change_direction(self, direction) -> None:

        if self.direction[0] == direction[0] * -1:
            return
        if self.direction[1] == direction[1] * -1:
            return
        self.direction = direction

    def move(self) -> None:
        self.col += self.direction[0]
        self.row += self.direction[1]

    def collide_borders(self) -> None:
        self.canvas.update()
        print(self.col, self.tiles_ammount)
        if self.col >= self.tiles_ammount - 1:
            self.is_active = 0


class Food:
    pass


App()

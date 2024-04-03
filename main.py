import tkinter

WINDOW_BG = 'black'
CANVAS_BG = 'white'
TILE_SIZE = 16
LINE_COLOR = 'black'
FPS = 30


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
        self.draw_lines()
        self.window.mainloop()

    def on_key(self, event: tkinter.Event) -> None:
        if event.keysym == 'Escape':
            self.window.destroy()

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
    def __init__(self) -> None:
        pass


class Snake:
    def __init__(self) -> None:
        pass


class Food:
    pass


App()

import tkinter as tk
from random import randint

# Sound effects (Windows-specific)
try:
    import winsound
    def play_eat_sound():
        winsound.Beep(1000, 100)  # High-pitched beep for eating food
    def play_game_over_sound():
        winsound.Beep(500, 500)   # Low-pitched beep for game over
except ImportError:
    def play_eat_sound():
        pass
    def play_game_over_sound():
        pass

# Constants
grid_size = 20
width = 20
height = 20

class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.start_button = tk.Button(self, text="Start Game", command=self.start_game)
        self.exit_button = tk.Button(self, text="Exit", command=master.quit)
        self.start_button.pack()
        self.exit_button.pack()

    def set_game(self, game):
        self.game = game

    def start_game(self):
        self.hide()
        self.game.show()
        self.game.start()

    def show(self):
        self.pack()

    def hide(self):
        self.pack_forget()

class SnakeGame(tk.Frame):
    def __init__(self, master, menu):
        super().__init__(master)
        self.menu = menu
        self.canvas = tk.Canvas(self, width=width*grid_size, height=height*grid_size, bg="black")
        self.canvas.pack()
        self.score_label = tk.Label(self, text="Score: 0")
        self.score_label.pack()
        self.return_button = None

    def start(self):
        if self.return_button is not None:
            self.return_button.destroy()
            self.return_button = None
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)
        self.score = 0
        self.food = self.generate_food()
        self.score_label.config(text=f"Score: {self.score}")
        self.update()

    def generate_food(self):
        while True:
            x = randint(0, width-1)
            y = randint(0, height-1)
            if (x, y) not in self.snake:
                return (x, y)

    def key_handler(self, event):
        if event.keysym == "w" and self.direction != (0, 1):
            self.direction = (0, -1)
        elif event.keysym == "s" and self.direction != (0, -1):
            self.direction = (0, 1)
        elif event.keysym == "a" and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif event.keysym == "d" and self.direction != (-1, 0):
            self.direction = (1, 0)

    def update(self):
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        if (new_head[0] < 0 or new_head[0] >= width or
            new_head[1] < 0 or new_head[1] >= height or
            new_head in self.snake):
            play_game_over_sound()
            self.score_label.config(text=f"Game Over, final score: {self.score}")
            self.return_button = tk.Button(self, text="Return to Menu", command=self.return_to_menu)
            self.return_button.pack()
            return
        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
            play_eat_sound()
        else:
            self.snake.pop()
        self.canvas.delete("all")
        for x, y in self.snake:
            self.canvas.create_rectangle(x*grid_size, y*grid_size, (x+1)*grid_size, (y+1)*grid_size, fill="green", outline="green")
        self.canvas.create_rectangle(self.food[0]*grid_size, self.food[1]*grid_size, (self.food[0]+1)*grid_size, (self.food[1]+1)*grid_size, fill="red", outline="red")
        self.score_label.config(text=f"Score: {self.score}")
        self.master.after(100, self.update)

    def return_to_menu(self):
        self.hide()
        self.menu.show()

    def show(self):
        self.pack()
        self.master.bind("<Key>", self.key_handler)

    def hide(self):
        self.pack_forget()
        self.master.unbind("<Key>")

# Main
root = tk.Tk()
root.title("Snake Game")
menu = MainMenu(root)
game = SnakeGame(root, menu)
menu.set_game(game)
menu.show()
root.mainloop()

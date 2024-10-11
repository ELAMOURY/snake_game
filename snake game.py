import tkinter as tk
import random
import winsound  # Pour jouer le son sur Windows

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        
        self.canvas = tk.Canvas(root, width=400, height=400, bg="black")
        self.canvas.pack()
        
        self.snake = [(20, 20), (20, 30), (20, 40)]
        self.food = self.create_food()
        self.direction = "Down"
        self.running = True  # Variable pour gérer l'état du jeu
        
        self.root.bind("<KeyPress>", self.change_direction)
        
        self.pause_button = tk.Button(root, text="Pause", command=self.pause_game)
        self.pause_button.pack(side=tk.LEFT)
        
        self.start_button = tk.Button(root, text="Start", command=self.start_game)
        self.start_button.pack(side=tk.RIGHT)
        
        self.replay_button = tk.Button(root, text="Replay", command=self.replay_game)
        self.replay_button.pack(side=tk.BOTTOM)
        self.replay_button.pack_forget()  # Hide the replay button initially
        
        self.update_snake()
        self.run_game()

    def create_food(self):
        x = random.randint(0, 19) * 20
        y = random.randint(0, 19) * 20
        return (x, y)

    def change_direction(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            self.direction = event.keysym

    def update_snake(self):
        head_x, head_y = self.snake[-1]
        if self.direction == "Up":
            new_head = (head_x, head_y - 20)
        elif self.direction == "Down":
            new_head = (head_x, head_y + 20)
        elif self.direction == "Left":
            new_head = (head_x - 20, head_y)
        elif self.direction == "Right":
            new_head = (head_x + 20, head_y)
        
        self.snake.append(new_head)
        if new_head == self.food:
            self.food = self.create_food()
            winsound.PlaySound("eat.wav", winsound.SND_ASYNC)  # Jouer le son
        else:
            self.snake.pop(0)

    def run_game(self):
        if self.running:
            self.update_snake()
            self.canvas.delete(tk.ALL)
            
            for segment in self.snake:
                self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="green")
            
            self.canvas.create_rectangle(self.food[0], self.food[1], self.food[0] + 20, self.food[1] + 20, fill="red")
            
            if self.check_collision():
                self.game_over()
            else:
                self.root.after(200, self.run_game)  # Increased delay to 200 milliseconds

    def check_collision(self):
        head_x, head_y = self.snake[-1]
        if head_x < 0 or head_x >= 400 or head_y < 0 or head_y >= 400:
            return True
        if len(self.snake) != len(set(self.snake)):
            return True
        return False

    def game_over(self):
        self.canvas.create_text(200, 200, text="Game Over", fill="white", font=("Arial", 24))
        self.running = False
        self.replay_button.pack(side=tk.BOTTOM)  # Show the replay button

    def pause_game(self):
        self.running = False

    def start_game(self):
        if not self.running:
            self.running = True
            self.run_game()

    def replay_game(self):
        self.snake = [(20, 20), (20, 30), (20, 40)]
        self.food = self.create_food()
        self.direction = "Down"
        self.running = True
        self.replay_button.pack_forget()  # Hide the replay button
        self.run_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
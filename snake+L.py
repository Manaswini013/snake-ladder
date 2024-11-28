import tkinter as tk
import random

class SnakeAndLadderGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Snake and Ladder Game")
        self.geometry("600x700")
        self.canvas = tk.Canvas(self, width=600, height=600)
        self.canvas.pack()

        # Create board
        self.create_board()
        self.player1_pos = 0
        self.player2_pos = 0
        self.players = {"Player 1": self.player1_pos, "Player 2": self.player2_pos}
        self.current_player = "Player 1"
        self.roll_button = tk.Button(self, text="Roll Dice", command=self.play_turn)
        self.roll_button.pack()

        self.dice_label = tk.Label(self, text="", font=("Helvetica", 20))
        self.dice_label.pack()

        # Dice faces as labels
        self.dice_faces = [tk.Label(self, text=str(i), font=("Helvetica", 32)) for i in range(1, 7)]
        for face in self.dice_faces:
            face.pack_forget()

    def create_board(self):
        # Draw the grid
        self.cells = {}
        for i in range(10):
            for j in range(10):
                x0 = j * 60
                y0 = 540 - i * 60
                x1 = x0 + 60
                y1 = y0 + 60
                cell_number = i * 10 + j + 1
                self.cells[cell_number] = (x0, y0, x1, y1)
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="white")
                self.canvas.create_text(x0 + 30, y0 + 30, text=str(cell_number))

        # Draw snakes and ladders
        self.snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        self.ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

        for start, end in self.snakes.items():
            self.draw_line(start, end, color="red")
        for start, end in self.ladders.items():
            self.draw_line(start, end, color="green")

        # Draw player pieces
        self.player1_piece = self.canvas.create_oval(10, 550, 30, 570, fill="blue")
        self.player2_piece = self.canvas.create_oval(30, 550, 50, 570, fill="yellow")

    def draw_line(self, start, end, color):
        x0, y0, _, _ = self.cells[start]
        x1, y1, _, _ = self.cells[end]
        self.canvas.create_line(x0 + 30, y0 + 30, x1 + 30, y1 + 30, fill=color, width=2)

    def roll_dice(self):
        roll = random.randint(1, 6)
        for face in self.dice_faces:
            face.pack_forget()
        self.dice_faces[roll - 1].pack()
        return roll

    def move_player(self, player, position):
        dice_roll = self.roll_dice()
        self.dice_label.config(text=f"{player} rolled a {dice_roll}")
        position += dice_roll

        if position > 100:
            position -= dice_roll
            self.dice_label.config(text=f"{player} needs an exact roll to finish.")

        if position in self.snakes:
            position = self.snakes[position]
        elif position in self.ladders:
            position = self.ladders[position]

        return position

    def update_piece_position(self, player_piece, position):
        x0, y0, x1, y1 = self.cells[position]
        if player_piece == self.player1_piece:
            self.canvas.coords(player_piece, x0 + 10, y0 + 10, x0 + 30, y0 + 30)
        else:
            self.canvas.coords(player_piece, x0 + 30, y0 + 30, x0 + 50, y0 + 50)

    def play_turn(self):
        current_position = self.players[self.current_player]
        new_position = self.move_player(self.current_player, current_position)
        self.players[self.current_player] = new_position

        if self.current_player == "Player 1":
            self.update_piece_position(self.player1_piece, new_position)
        else:
            self.update_piece_position(self.player2_piece, new_position)

        if new_position == 100:
            self.dice_label.config(text=f"{self.current_player} wins!")
            self.roll_button.config(state=tk.DISABLED)
            return

        self.current_player = "Player 2" if self.current_player == "Player 1" else "Player 1"

if __name__ == "__main__":
    game = SnakeAndLadderGame()
    game.mainloop()

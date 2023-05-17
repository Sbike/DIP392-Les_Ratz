import tkinter as tk
from tkinter import messagebox
import random

class Connect4:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect 4")
        self.master.resizable(False, False)

        self.grid = [[None for _ in range(7)] for _ in range(6)]
        self.current_player = "red"
        self.game_over = False
        self.tie = False
        self.score = {"red": 0, "blue": 0}
        self.play_against_computer = False ## Turn to True to play against the computer, to False to play against a real player

        self.canvas = tk.Canvas(self.master, width=700, height=600, bg="white")
        self.canvas.pack()

        self.reset_button = tk.Button(
            self.master, text="Restart", command=self.reset_game, height=2, width=10
        )
        self.reset_button.pack(side="bottom")

        self.canvas.bind("<Button-1>", self.play)

        self.draw_board()

    def play(self, event):
        if not self.game_over:
            col = event.x // 100
            row = self.get_available_row(col)

            if row is not None:
                self.place_piece(row, col, self.current_player)
                self.draw_piece(row, col, self.current_player)

                if self.check_winner(row, col, self.current_player):
                    messagebox.showinfo("Game Over", f"{self.current_player.capitalize()} player wins!")
                    self.game_over = True
                    self.score[self.current_player] += 1
                elif self.check_tie():
                    messagebox.showinfo("Game Over", "It's a tie!")
                    self.game_over = True
                    self.tie = True
                else:
                    self.switch_player()

                    if self.play_against_computer and not self.game_over:
                        row, col = self.computer_play()
                        self.place_piece(row, col, self.current_player)
                        self.draw_piece(row, col, self.current_player)

                        if self.check_winner(row, col, self.current_player):
                            messagebox.showinfo("Game Over", f"{self.current_player.capitalize()} player wins!")
                            self.game_over = True
                            self.score[self.current_player] += 1
                        elif self.check_tie():
                            messagebox.showinfo("Game Over", "It's a tie!")
                            self.game_over = True
                            self.tie = True
                        else:
                            self.switch_player()

    def draw_board(self):
        for row in range(6):
            for col in range(7):
                self.canvas.create_oval(
                    col * 100 + 10, row * 100 + 10, col * 100 + 90, row * 100 + 90, fill="white"
                )

    def draw_piece(self, row, col, color):
        self.canvas.create_oval(
            col * 100 + 10, row * 100 + 10, col * 100 + 90, row * 100 + 90, fill=color
        )

    def reset_game(self):
        self.game_over = False
        self.tie = False
        self.current_player = "red"
        self.grid = [[None for _ in range(7)] for _ in range(6)]
        self.canvas.delete("all")
        self.draw_board()

    def get_available_row(self, col):
        for row in range(5, -1, -1):
            if self.grid[row][col] is None:
                return row
        return None

    def place_piece(self, row, col, player):
        self.grid[row][col] = player

    def switch_player(self):
        self.current_player = "blue" if self.current_player == "red" else "red"

    def check_winner(self, row, col, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            for d in [-1, 1]:
                r, c = row + dr * d, col + dc * d
                while 0 <= r < 6 and 0 <= c < 7 and self.grid[r][c] == player:
                    count += 1
                    r += dr * d
                    c += dc * d
            if count >= 4:
                return True
        return False

    def check_tie(self):
        for row in self.grid:
            if None in row:
                return False
        return True

    def computer_play(self):
        col = random.randint(0, 6)
        row = self.get_available_row(col)
        while row is None:
            col = random.randint(0, 6)
            row = self.get_available_row(col)
        return row, col

root = tk.Tk()
game = Connect4(root)
root.mainloop()
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.board = [' ']*9
        self.current_winner = None
        self.player = 'X'
        self.x_icon = ImageTk.PhotoImage(Image.open("./img/rec.png").resize((70, 70), Image.Resampling.LANCZOS))
        self.o_icon = ImageTk.PhotoImage(Image.open("./img/close.png").resize((80, 80), Image.Resampling.LANCZOS))
        self.buttons = []
        self.create_widgets()

    def create_widgets(self):
        self.scoreboard = tk.Label(self.root, text="Player X's turn", font=('Helvetica', 20))
        self.scoreboard.grid(row=0, column=0, columnspan=3)
        for i in range(9):
            button = tk.Button(self.root, text='', 
                            command=lambda i=i: self.on_click(i), 
                            font=('Helvetica', 20), height=2, width=5, 
                            bg='white', relief='ridge', bd=5)
            button.grid(row=(i//3)+1, column=i%3, padx=5, pady=5)
            self.buttons.append(button)

    def on_click(self, index):
        if self.board[index] == ' ':
            self.board[index] = self.player
            self.update_button(index)
            if self.check_winner():
                messagebox.showinfo("Tic Tac Toe", f"Player {self.player} wins!")
                self.reset_game()
            elif self.check_tie():
                messagebox.showinfo("Tic Tac Toe", "It's a tie!")
                self.reset_game()
            else:
                self.player = 'O' if self.player == 'X' else 'X'
                self.scoreboard.config(text=f"Player {self.player}'s turn")

    def update_button(self, index):
        if self.board[index] == 'X':
            self.buttons[index].config(image=self.x_icon, text='', compound='center', height=80, width=80)
        elif self.board[index] == 'O':
            self.buttons[index].config(image=self.o_icon, text='', compound='center', height=80, width=80)

    def check_winner(self):
        # Check rows
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] != ' ':
                self.current_winner = self.board[i]
                return True
        # Check columns
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != ' ':
                self.current_winner = self.board[i]
                return True
        # Check diagonals
        if self.board[0] == self.board[4] == self.board[8] != ' ':
            self.current_winner = self.board[0]
            return True
        if self.board[2] == self.board[4] == self.board[6] != ' ':
            self.current_winner = self.board[2]
            return True
        return False

    def check_tie(self):
        return ' ' not in self.board

    def reset_game(self):
        self.board = [' ']*9
        self.player = 'X'
        self.scoreboard.config(text="Player X's turn")
        for button in self.buttons:
            button.config(image='', text='', height=2, width=5)

if __name__ == '__main__':
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

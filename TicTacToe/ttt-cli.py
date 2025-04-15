class TicTacToe():
    def __init__(self):
        self.board = [' ']*9
        self.current_winner = None
    
    def print_menu(self):
        print("Welcome to Tic Tac Toe!")
        print("Here is the current board:")
        self.print_board()
        print("To make a move, enter the number of the square you want to place your piece in.")
        print("The board is numbered as follows:")
        self.print_board_numbers()
        print("Player 1 is 'X' and Player 2 is 'O'.")
        print("Player 1 goes first.")
        print("Good luck!")

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')
            print('---------')

    def print_board_numbers(self):
        for row in [list(range(i*3+1, (i+1)*3+1)) for i in range(3)]:
            print('| ' + ' | '.join(map(str, row)) + ' |')
            print('---------')

    def make_move(self, square, player):
        if self.board[square-1] == ' ':
            self.board[square-1] = player
            return True
        else:
            return False
        
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
    
    def play_game(self):
        self.print_menu()
        player = 'X'
        while True:
            square = int(input(f"Player {player}, make your move: "))
            if self.make_move(square, player):
                self.print_board()
                if self.check_winner():
                    print(f"Player {player} wins!")
                    break
                if self.check_tie():
                    print("It's a tie!")
                    break
                player = 'O' if player == 'X' else 'X'
            else:
                print("Invalid move. Try again.")
        print("Game over.")

if __name__ == '__main__':
    game = TicTacToe()
    game.play_game()
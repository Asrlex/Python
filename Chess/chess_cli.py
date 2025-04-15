from chess import Chess

class ChessCLI:
    def __init__(self):
        self.chess = Chess()

    def print_board(self):
        print("    A  B  C  D  E  F  G  H")
        for i, row in enumerate(self.chess.board):
            print(8 - i, " ", " ".join(row), " ", 8 - i)
        print("     A  B  C  D  E  F  G  H")
    
    def get_user_input(self):
        return input("Play or exit: ")

    def get_game_mode(self):
        print("Select game mode:")
        print("1. Player vs Player")
        print("2. Player vs AI (not available)")
        return input("Enter 1 or 2: ")

    def get_move(self):
        from_square = input("Enter from square (e.g., B4) or 'exit' to quit: ")
        if from_square.lower() == 'exit':
            return None, None
        to_square = input("Enter to square (e.g., F7): ")
        return self.chess.notation_to_index(from_square), self.chess.notation_to_index(to_square)

    def play(self):
        if self.get_user_input().lower() == 'exit':
            return
        game_mode = self.get_game_mode()
        if game_mode != '1':
            print("PvAI is not available at the moment. Exiting.")
            return
        self.print_board()
        print(f"Current turn: {'White' if self.chess.turn == 'W' else 'Black'}")
        while True:
            from_square, to_square = self.get_move()
            if from_square is None:
                break
            if self.chess.is_valid_move(from_square, to_square):
                self.chess.move_piece(from_square, to_square)
                winner = self.chess.check_winner()  # Check for winner after each move
                if winner:
                    print(f"{winner} wins!")
                    self.print_board()
                    return
                self.chess.change_turn()
                self.print_board()
                print(f"Current turn: {'White' if self.chess.turn == 'W' else 'Black'}")
            else:
                print("Invalid move! Try again.")
                print("\n")
        print("Game over!")

def main():
    chess = ChessCLI()
    chess.play()

if __name__ == "__main__":
    main()
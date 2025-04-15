import time

class Chess:
    def __init__(self):
        self.board = [ 
            [ 'WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR' ],
            [ 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP' ],
            [ '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ' ],
            [ '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ' ],
            [ '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ' ],
            [ '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ' ],
            [ 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP' ],
            [ 'BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR' ] 
        ]
        self.black_pieces = ['BR', 'BR', 'BN', 'BN', 'BB', 'BB', 'BQ', 'BK', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP']
        self.white_pieces = ['WR', 'WR', 'WN', 'WN', 'WB', 'WB', 'WQ', 'WK', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP']
        self.turn = 'W'
        self.turns_played = 0
        self.start_time = time.time()
        self.log_file = "chess_log.txt"
        with open(self.log_file, 'w') as f:
            f.write("Game started\n")

    def notation_to_index(self, notation):
        col = ord(notation[0].lower()) - ord('a')
        row = 8 - int(notation[1])
        return row, col

    def move_piece(self, from_square, to_square):
        from_row, from_col = from_square
        to_row, to_col = to_square
        self.eat_piece(from_square, to_square)
        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = '  '
        self.log_action(from_square, to_square)
        self.turns_played += 1
        self.start_time = time.time()

    def is_valid_move(self, from_square, to_square):
        from_row, from_col = from_square
        piece = self.board[from_row][from_col]
        if piece == '  ' or piece[0] != self.turn or from_square == to_square or not self.is_within_bounds(*to_square):
            return False
        
        piece_type = piece[1]
        move_validators = {
            'P': self.is_valid_pawn_move,
            'R': self.is_valid_rook_move,
            'N': self.is_valid_knight_move,
            'B': self.is_valid_bishop_move,
            'Q': self.is_valid_queen_move,
            'K': self.is_valid_king_move
        }
        if piece_type in move_validators:
            return move_validators[piece_type](from_square, to_square)
        return False
    
    def is_within_bounds(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def is_capture(self, to_square):
        to_row, to_col = to_square
        target_piece = self.board[to_row][to_col]
        return target_piece != '  ' and target_piece[0] != self.turn

    def is_valid_pawn_move(self, from_square, to_square):
        from_row, from_col = from_square
        to_row, to_col = to_square
        piece = self.board[from_row][from_col]
        direction = 1 if piece[0] == 'W' else -1
        if from_col == to_col:
            if to_row - from_row == direction and not self.is_capture(to_square):
                return True
        elif abs(from_col - to_col) == 1:
            if to_row - from_row == direction and self.is_capture(to_square):
                return True
        return False

    def is_valid_rook_move(self, from_square, to_square):
        from_row, from_col = from_square
        to_row, to_col = to_square
        return from_row == to_row or from_col == to_col

    def is_valid_knight_move(self, from_square, to_square):
        from_row, from_col = from_square
        to_row, to_col = to_square
        return (abs(from_row - to_row) == 2 and abs(from_col - to_col) == 1) or \
                (abs(from_row - to_row) == 1 and abs(from_col - to_col) == 2)

    def is_valid_bishop_move(self, from_square, to_square):
        from_row, from_col = from_square
        to_row, to_col = to_square
        return abs(from_row - to_row) == abs(from_col - to_col)

    def is_valid_queen_move(self, from_square, to_square):
        return self.is_valid_rook_move(from_square, to_square) or self.is_valid_bishop_move(from_square, to_square)
    
    def is_valid_king_move(self, from_square, to_square):
        from_row, from_col = from_square
        to_row, to_col = to_square
        return abs(from_row - to_row) <= 1 and abs(from_col - to_col) <= 1

    def eat_piece(self, from_square, to_square):
        to_row, to_col = to_square
        target_piece = self.board[to_row][to_col]
        if target_piece == '  ':
            return
        from_row, from_col = from_square
        piece = self.board[from_row][from_col]
        if piece[0] != target_piece[0]:
            if piece[0] == 'W':
                self.black_pieces.remove(target_piece)
            else:
                self.white_pieces.remove(target_piece)
            return target_piece
        
    def change_turn(self):
        self.turn = 'W' if self.turn == 'B' else 'B'
        self.start_time = time.time()

    def log_action(self, from_square, to_square):
        from_row, from_col = from_square
        to_row, to_col = to_square
        piece = self.board[to_row][to_col]
        action = f"{piece} from {chr(from_col + ord('A'))}{8 - from_row} to {chr(to_col + ord('A'))}{8 - to_row}"
        with open(self.log_file, 'a') as f:
            f.write(f"Turn {self.turns_played + 1}: {action}\n")
            f.write(f"Time taken: {time.time() - self.start_time:.2f} seconds\n")
            f.write(self.get_board_state())

    def get_board_state(self):
        state = "\n".join([" ".join(row) for row in self.board])
        return f"{state}\n\n"

    def check_winner(self):
        if 'WK' not in self.white_pieces:
            return 'B'
        if 'BK' not in self.black_pieces:
            return 'W'
        return None

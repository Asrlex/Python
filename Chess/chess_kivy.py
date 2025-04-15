import time
import json
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window
from chess import Chess
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, Ellipse, Line
from datetime import datetime

class ChessKivy(App):
    def __init__(self, **kwargs):
        """Initialize the ChessKivy app."""
        super().__init__(**kwargs)
        self.chess = Chess()
        self.turns_played = 0
        self.start_time = time.time()
        self.log_file = "chess_kivy_log.txt"
        self.selected_piece = None
        self.selected_square = None
        self.buttons = []
        self.reset_log()

    def reset_log(self):
        """Reset the log file."""
        with open(self.log_file, 'w') as f:
            f.write("Game started\n")

    def log(self, message):
        """Log a message to the log file."""
        with open(self.log_file, 'a') as f:
            f.write(message + "\n")

    def build(self):
        """Build the main layout of the app."""
        tile_size = 35
        board_size = tile_size * 8
        window_width = board_size + 3.5 * tile_size
        window_height = board_size + 3 * tile_size

        Window.size = (window_width, window_height)
        Window.resizable = False

        main_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        game_layout = GridLayout(cols=1, rows=2, padding=2, spacing=2, size_hint=(None, None), size=(window_width*.9, window_height))
        header_layout = BoxLayout(size_hint=(1, None), height=tile_size, orientation='horizontal')
        board_layout = GridLayout(cols=9, rows=9, padding=2, spacing=2, size_hint=(None, None), size=(board_size*.9, board_size))

        menu_layout = BoxLayout(size_hint=(1, None), height=tile_size, orientation='horizontal')
        dropdown = DropDown()
        self.create_menu(menu_layout, dropdown, tile_size)
        self.create_header(header_layout, menu_layout, tile_size)
        self.create_board(board_layout, tile_size)

        game_layout.add_widget(header_layout)
        game_layout.add_widget(board_layout)
        main_layout.add_widget(game_layout)

        Clock.schedule_interval(self.update_timer, 0.1)

        return main_layout

    def create_menu(self, menu_layout, dropdown, tile_size):
        """Create the menu layout with buttons for new game, save game, load game, and exit."""
        new_game_btn = Button(text='New Game', font_size=12, size_hint_y=None, height=tile_size)
        new_game_btn.bind(on_release=self.new_game)
        dropdown.add_widget(new_game_btn)
        save_game_btn = Button(text='Save Game', font_size=12, size_hint_y=None, height=tile_size)
        save_game_btn.bind(on_release=self.save_game)
        dropdown.add_widget(save_game_btn)
        load_game_btn = Button(text='Load Game', font_size=12, size_hint_y=None, height=tile_size)
        load_game_btn.bind(on_release=self.load_game)
        dropdown.add_widget(load_game_btn)
        exit_btn = Button(text='Exit', font_size=12, size_hint_y=None, height=tile_size)
        exit_btn.bind(on_release=self.stop)
        dropdown.add_widget(exit_btn)
        menu_btn = Button(text='Menu', font_size=12, size_hint=(None, None), size=(tile_size * 2, tile_size))
        menu_btn.bind(on_release=dropdown.open)
        menu_layout.add_widget(menu_btn)

    def create_header(self, header_layout, menu_layout, tile_size):
        """Create the header layout with turn, turns played, and timer labels."""
        self.turn_label = Label(text=f"Turn: {self.chess.turn}", font_size=14)
        self.turns_played_label = Label(text=f"Turns Played: {self.turns_played}", font_size=14)
        self.timer_label = Label(text="Time: 0.00s", font_size=14)
        header_layout.add_widget(menu_layout)
        header_layout.add_widget(self.turn_label)
        header_layout.add_widget(self.turns_played_label)
        header_layout.add_widget(self.timer_label)

    def create_board(self, board_layout, tile_size):
        """Create the chessboard layout with buttons for each square."""
        board_layout.add_widget(Label(size_hint=(None, None), size=(tile_size, tile_size)))
        for col in 'ABCDEFGH':
            board_layout.add_widget(Label(text=col, font_size=14, size_hint=(None, None), size=(tile_size, tile_size)))
        for i in range(8):
            board_layout.add_widget(Label(text=str(i+1), font_size=14, size_hint=(None, None), size=(tile_size, tile_size)))
            for j in range(8):
                button = Button(font_size=14, size_hint=(None, None), size=(tile_size, tile_size))
                button.bind(on_press=self.on_button_press)
                button.coords = (i, j)
                self.buttons.append(button)
                board_layout.add_widget(button)
        self.update_board_buttons()

    def update_board_buttons(self):
        """Update the buttons on the board with the current state."""
        for i, row in enumerate(self.chess.board):
            for j, cell in enumerate(row):
                button = self.get_button_at(i, j)
                piece = cell.strip()
                button.text = piece if piece else ''
                self.set_button_color(button, i, j)

    def set_button_color(self, button, row, col):
        """Set the color of the button based on its position."""
        if (row + col) % 2 == 0:
            button.background_color = (1, 0.94, 0.84, 1)
            button.color = (0, 0, 0, 1)
        else:
            button.background_color = (0.1, 0.1, 0.1, 1)
            button.color = (1, 1, 1, 1)

    def new_game(self, instance):
        """Start a new game and reset the board and labels."""
        self.chess = Chess()
        self.turns_played = 0
        self.start_time = time.time()
        self.selected_piece = None
        self.selected_square = None
        self.turn_label.text = f"Turn: {self.chess.turn}"
        self.turns_played_label.text = f"Turns Played: {self.turns_played}"
        self.timer_label.text = "Time: 0.00s"
        self.update_board_buttons()
        self.reset_log()
        self.log("New game started")

    def update_timer(self, dt):
        """Update the timer label with the elapsed time."""
        elapsed_time = time.time() - self.start_time
        self.timer_label.text = f"Time: {elapsed_time:.2f}s"
        

    def on_button_press(self, instance):
        """Handle button press events for selecting and moving pieces."""
        row, col = instance.coords
        if self.selected_piece is None:
            if self.chess.board[row][col].strip() and self.chess.board[row][col].strip()[0] == self.chess.turn[0]:
                self.selected_piece = self.chess.board[row][col]
                self.selected_square = (row, col)
                instance.background_color = (0, 1, 0, 1)
        else:
            from_square = self.selected_square
            to_square = (row, col)
            if from_square != to_square and self.chess.is_valid_move(from_square, to_square):
                self.chess.move_piece(from_square, to_square)
                self.chess.log_action(from_square, to_square)
                self.turns_played += 1
                self.start_time = time.time()
                winner = self.chess.check_winner()
                if winner:
                    self.update_board(from_square, to_square)
                    self.on_win(winner)
                    return
                self.chess.change_turn()
                self.turn_label.text = f"Turn: {self.chess.turn}"
                self.turns_played_label.text = f"Turns Played: {self.turns_played}"
                self.selected_piece = None
                self.selected_square = None
                self.update_board(from_square, to_square)
            else:
                self.selected_piece = None
                self.selected_square = None

    def on_win(self, winner):
        """Handle the end of the game when a player wins."""
        self.turn_label.text = f"Winner: {winner}"
        
        self.log(f"Winner: {winner}")
        
        Clock.schedule_once(lambda dt: self.stop(), 2)

        self.show_win_popup(f"{winner} wins!", title="Game Over")

    def show_win_popup(self, message, title='Info'):
        """Show a win popup with a message and save log button."""
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        save_log_btn = Button(text='Save Log', size_hint_y=None, height=40)
        save_log_btn.bind(on_release=self.save_log_with_timestamp)
        content.add_widget(save_log_btn)
        popup = Popup(title=title, content=content, size_hint=(None, None), size=(300, 150), auto_dismiss=True, opacity=0.8)
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)

    def save_log_with_timestamp(self, instance):
        """Save the log of the current game to a new file with a timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_log_file = f"game_log_{timestamp}.txt"
        with open(new_log_file, 'w') as new_log_f:
            with open(self.log_file, 'r') as log_f:
                new_log_f.write(log_f.read())
        print(f"Log saved to {new_log_file}")

    def on_stop(self):
        """Handle the app stop event and log the game end."""
        self.log("Game ended")

    def update_board(self, from_square, to_square):
        """Update the board display after a piece is moved."""
        from_row, from_col = from_square
        to_row, to_col = to_square
        from_button = self.get_button_at(from_row, from_col)
        to_button = self.get_button_at(to_row, to_col)
        from_button.text = ''
        piece = self.chess.board[to_row][to_col].strip()
        if piece:
            to_button.text = piece
        
        log_message = f"Moving {self.chess.board[from_row][from_col]} from {from_square} to {to_square}"
        print(f"Turn {self.turns_played}: {log_message}")
        self.log(f"Turn {self.turns_played}: {log_message}")
        
        self.set_button_color(to_button, to_row, to_col)
        self.set_button_color(from_button, from_row, from_col)

    def get_button_at(self, row, col):
        """Get the button at the specified row and column."""
        return self.buttons[row * 8 + col]

    def save_game(self, instance):
        """Save the current game state to a file."""
        elapsed_time = time.time() - self.start_time
        game_state = {
            'board': self.chess.board,
            'turn': self.chess.turn,
            'turns_played': self.turns_played,
            'elapsed_time': elapsed_time,
            'pieces': {
                'white': self.chess.white_pieces,
                'black': self.chess.black_pieces
            }
        }
        with open('saved_game.json', 'w') as f:
            json.dump(game_state, f)
        with open('saved_game_log.txt', 'w') as f:
            with open(self.log_file, 'r') as log_f:
                f.write(log_f.read())
        print("Game saved")

    def load_game(self, instance):
        """Load a saved game state from a file."""
        try:
            with open('saved_game.json', 'r') as f:
                game_state = json.load(f)
            self.chess.board = game_state['board']
            self.chess.turn = game_state['turn']
            self.turns_played = game_state['turns_played']
            self.start_time = time.time() - game_state['elapsed_time']
            self.chess.white_pieces = game_state['pieces']['white']
            self.chess.black_pieces = game_state['pieces']['black']
            self.update_board_buttons()
            self.turn_label.text = f"Turn: {self.chess.turn}"
            self.turns_played_label.text = f"Turns Played: {self.turns_played}"
            
            with open('saved_game_log.txt', 'r') as f:
                with open(self.log_file, 'w') as log_f:
                    log_f.write(f.read())
            print("Game loaded")
        except FileNotFoundError:
            self.show_popup("No saved game found", title="Error")

    def show_popup(self, message, title='Info'):
        """Show a popup with a message."""
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        popup = Popup(title=title, content=content, size_hint=(None, None), size=(300, 150), auto_dismiss=True, opacity=0.8)
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)

if __name__ == '__main__':
    ChessKivy().run()
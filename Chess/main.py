import sys
from chess_kivy import ChessKivy
from chess_cli import ChessCLI

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ['cli', 'gui']:
        print("Usage: python main.py [cli|gui]")
        return

    if sys.argv[1] == 'cli':
        game = ChessCLI()
        game.play()
    else:
        ChessKivy().run()

if __name__ == "__main__":
    main()
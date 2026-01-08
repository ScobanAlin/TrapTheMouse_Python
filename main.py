import tkinter as tk
from tkinter import ttk

from GameBoard import GameBoard
from GameBoardUI import GameBoardUI
import json


class TrapTheMouseApp(tk.Tk):
    """Tkinter root aplication"""
    def __init__(self):
        """Initialize the main application window"""

        super().__init__()
        self.title("Trap the Mouse")
        self.geometry("900x600")
        style = ttk.Style()
        style.theme_use("aqua")
        self.resizable(False, False)
        self.focus_force()
        self.current_frame = None
        self.show_main_menu()

    def load_game(self, board):
        """Switch to the game board, to a saved board"""
        self.switch_frame(GameBoardUI, board)

    def switch_frame(self, frame_class, *args):
        """Replace the currently displayed frame."""
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame_class(self, *args)
        self.current_frame.pack(expand=True, fill="both")

    def show_main_menu(self):
        """Show the main menu"""
        self.switch_frame(MainMenu)

    def show_singleplayer_menu(self):
        """Show the single player menu"""
        self.switch_frame(SingleplayerMenu)

    def show_saved_games_menu(self):
        """Show the saved games menu"""
        self.switch_frame(SavedGamesMenu)

    def show_win_scene(self):
        """Show the win scene"""
        self.switch_frame(WinScene)

    def show_lose_scene(self):
        """Show the lose scene"""
        self.switch_frame(LoseScene)

    def start_game(self, mode, difficulty=None):
        """Start the game"""
        board = GameBoard(mode, difficulty)
        self.switch_frame(GameBoardUI, board)


class MainMenu(tk.Frame):
    """Main Menu frame"""
    def __init__(self, master):
        """Initialize the main menu frame"""
        super().__init__(master)
        ttk.Label(self, text="Trap the Mouse", font=("Arial", 20, "bold")).pack(pady=20)
        ttk.Button(
            self,
            text="Singleplayer",
            width=20,
            command=master.show_singleplayer_menu
        ).pack(pady=10)

        ttk.Button(self, text="Saved Games", width=20, command=master.show_saved_games_menu
                   ).pack(pady=10)

        ttk.Button(
            self,
            text="1vs1",
            width=20,
            command=lambda: master.start_game("1vs1")
        ).pack(pady=10)

        ttk.Button(self,
                   text="Exit Game",
                   width=20,
                   command=lambda: master.quit()).pack(pady=10)


class SavedGamesMenu(tk.Frame):
    """Saved games menu"""
    SAVE_FILE = "saves.json"

    def __init__(self, master):
        """Initialize the main menu frame"""
        super().__init__(master)

        ttk.Label(self, text="Saved Games", font=("Arial", 18, "bold")).pack(pady=20)

        saves = self._load_all_saves()

        if not saves:
            ttk.Label(self, text="No saved games found.").pack(pady=10)
        else:
            for name in saves:
                ttk.Button(
                    self,
                    text=name,
                    width=30,
                    command=lambda n=name: self._load_save(n)
                ).pack(pady=5)

        ttk.Button(
            self,
            text="Back",
            width=20,
            command=master.show_main_menu
        ).pack(pady=20)

    def _load_all_saves(self):
        """Load all saves from json file"""
        try:
            with open(self.SAVE_FILE, "r") as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _load_save(self, name):
        """Load saves from json file"""
        saves = self._load_all_saves()
        data = saves.get(name)

        if not data:
            return

        board = GameBoard.from_dict(data)
        self.master.load_game(board)


class SingleplayerMenu(tk.Frame):
    """Single player menu"""
    def __init__(self, master):
        """Initialize the main menu frame"""
        super().__init__(master)

        ttk.Label(self, text="Choose Difficulty", font=("Arial", 18)).pack(pady=20)

        ttk.Button(
            self,
            text="Easy",
            width=20,
            command=lambda: master.start_game("singleplayer", "easy")
        ).pack(pady=5)

        ttk.Button(
            self,
            text="Medium",
            width=20,
            command=lambda: master.start_game("singleplayer", "medium")
        ).pack(pady=5)

        ttk.Button(
            self,
            text="Hard",
            width=20,
            command=lambda: master.start_game("singleplayer", "hard")
        ).pack(pady=5)

        ttk.Button(
            self,
            text="Back",
            width=20,
            command=master.show_main_menu
        ).pack(pady=20)


class WinScene(tk.Frame):
    """Win screen frame"""
    def __init__(self, master):
        """Initialize the main menu frame"""
        super().__init__(master)

        ttk.Label(
            self,
            text="Wall Player Wins",
            font=("Arial", 24, "bold"),
        ).pack(pady=40)

        ttk.Button(self,text="Home",width=20,command=master.show_main_menu).pack(pady=10)


class LoseScene(tk.Frame):
    """Lose screen frame"""
    def __init__(self, master):
        super().__init__(master)

        ttk.Label(self,text="Mouse Player Wins",font=("Arial", 24, "bold")).pack(pady=40)

        ttk.Button(self,text="Home",width=20,command=master.show_main_menu).pack(pady=10)


if __name__ == "__main__":
    app = TrapTheMouseApp()
    app.mainloop()

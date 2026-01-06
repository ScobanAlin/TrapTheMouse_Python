import tkinter as tk
from GameBoard import GameBoard
from GameBoardUI import GameBoardUI

class TrapTheMouseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Trap the Mouse")
        self.geometry("800x600")
        self.resizable(False, False)
        self.focus_force()
        self.current_frame = None
        self.show_main_menu()

    def switch_frame(self, frame_class, *args):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame_class(self, *args)
        self.current_frame.pack(expand=True, fill="both")

    def show_main_menu(self):
        self.switch_frame(MainMenu)

    def show_singleplayer_menu(self):
        self.switch_frame(SingleplayerMenu)

    def show_saved_games_menu(self):
        self.switch_frame(SavedGamesMenu)

    def show_win_scene(self):
        self.switch_frame(WinScene)

    def show_lose_scene(self):
        self.switch_frame(LoseScene)

    def start_game(self, mode, difficulty=None):
        board = GameBoard(mode, difficulty)
        self.switch_frame(GameBoardUI, board)

class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Trap the Mouse", font=("Arial", 20, "bold")).pack(pady=20)

        tk.Button(
            self,
            text="Singleplayer",
            width=20,
            command=master.show_singleplayer_menu
        ).pack(pady=10)


        tk.Button(self,text="Saved Games",width=20,command = master.show_saved_games_menu
                  ).pack(pady=10)

        tk.Button(
            self,
            text="1vs1",
            width=20,
            command=lambda: master.start_game("1vs1")
        ).pack(pady=10)


        tk.Button(self,
                  text="Exit Game",
                  width=20,
                  command= lambda: master.quit()).pack(pady=10)

class SavedGamesMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Saved Games", font=("Arial", 18)).pack(pady=20)

        tk.Button(
            self,
            text="Back",
            width=20,
            command=master.show_main_menu
        ).pack(pady=20)

class SingleplayerMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Choose Difficulty", font=("Arial", 18)).pack(pady=20)

        tk.Button(
            self,
            text="Easy",
            width=20,
            command=lambda: master.start_game("singleplayer", "easy")
        ).pack(pady=5)

        tk.Button(
            self,
            text="Medium",
            width=20,
            command=lambda: master.start_game("singleplayer", "medium")
        ).pack(pady=5)

        tk.Button(
            self,
            text="Hard",
            width=20,
            command=lambda: master.start_game("singleplayer", "hard")
        ).pack(pady=5)

        tk.Button(
            self,
            text="Back",
            width=20,
            command=master.show_main_menu
        ).pack(pady=20)


class WinScene(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(
            self,
            text="You Win! 🎉\nMouse Trapped",
            font=("Arial", 24, "bold"),
            fg="green"
        ).pack(pady=40)

        tk.Button(
            self,
            text="Home",
            width=20,
            command=master.show_main_menu
        ).pack(pady=10)


class LoseScene(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(
            self,
            text="You Lose 😢\nMouse Escaped",
            font=("Arial", 24, "bold"),
            fg="red"
        ).pack(pady=40)


        tk.Button(
            self,
            text="Home",
            width=20,
            command=master.show_main_menu
        ).pack(pady=10)


if __name__ == "__main__":
    app = TrapTheMouseApp()
    app.mainloop()

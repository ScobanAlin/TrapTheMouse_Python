import tkinter as tk


class TrapTheMouseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Trap the Mouse")
        self.geometry("800x600")
        self.resizable(False, False)

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

    def start_game(self, mode, difficulty=None):
        print("Game started!")
        print("Mode:", mode)
        print("Difficulty:", difficulty)
        # Later: self.switch_frame(GameBoard, mode, difficulty)



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

        tk.Button(
            self,
            text="Multiplayer",
            width=20,
            command=lambda: master.start_game("multiplayer")
        ).pack(pady=10)


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



if __name__ == "__main__":
    app = TrapTheMouseApp()
    app.mainloop()

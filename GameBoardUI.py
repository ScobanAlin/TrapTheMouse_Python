import tkinter as tk
from tkinter import ttk

import math
import json


class GameBoardUI(tk.Frame):
    HEX_RADIUS = 28
    PADDING = 50
    SAVE_FILE = "saves.json"
    DOT_RADIUS = 5
    DOT_COLOR = "#333333"
    COLOR_EMPTY = "#c8f26d"
    COLOR_WALL = "#8b4513"
    COLOR_MOUSE = "#ff4d4d"
    COLOR_OUTLINE = "#6aa84f"
    COLOR_HOVER = "#ffd966"
    COLOR_WALL_HOVER = "#93c47d"

    def __init__(self, master, board):
        super().__init__(master, bg="#9acd32")
        self.board = board
        self.hovered_cell = None

        self.main = tk.Frame(self, bg="#9acd32")
        self.main.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.main, bg="#9acd32", width=600, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        style = ttk.Style()
        style.theme_use("aqua")

        style.configure(
            "Game.TButton",
            font=("Segoe UI", 11),
            padding=10
        )

        style.map(
            "Game.TButton",
            background=[("active", "#b6d7a8")]
        )

        self.side = ttk.Frame(self.main)
        self.side.pack(side="right", fill="y", padx=0)

        self._build_side_panel()

        self.hex_h = math.sqrt(3) * self.HEX_RADIUS
        self.hex_w = 2 * self.HEX_RADIUS

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_hover)
        self.canvas.bind("<Leave>", self.clear_hover)

        self.draw_board()

    def _build_side_panel(self):
        ttk.Label(self.side, text="Game Info", font=("Arial", 16, "bold")).pack(pady=10)
        ttk.Label
        self.info = ttk.Label(self.side)
        self.info.pack(pady=5)

        self.score = ttk.Label(self.side)
        self.score.pack(pady=5)
        tk.Frame(self.side, bg="#323131").pack(expand=True, fill="both")

        ttk.Button(
            self.side,
            text="Undo",
            width=18,
            command=self.undo_move
        ).pack(pady=4)

        ttk.Button(
            self.side,
            text="Redo",
            width=18,
            command=self.redo_move
        ).pack(pady=4)

        ttk.Button(
            self.side,
            text="Go Back",
            command=self.confirm_exit
        ).pack(pady=10)

    def update_info(self):
        self.info.config(
            text=f"Mode: {self.board.game_type}\nDifficulty: {self.board.difficulty}\nTurn: {self.board.current_player.upper()}"
        )
        self.score.config(text=f"Score: {self.board.score}")

    def confirm_exit(self):
        modal = tk.Toplevel(self)
        modal.title("Confirm Exit")
        modal.geometry("300x200")
        modal.transient(self)
        modal.grab_set()

        ttk.Label(
            modal,
            text="Do you want to save the game\nbefore exiting?",
            font=("Arial", 11)
        ).pack(pady=15)

        ttk.Button(
            modal,
            text="Save & Exit",
            width=20,
            command=lambda: self._open_save_then_exit(modal)
        ).pack(pady=5)

        ttk.Button(
            modal,
            text="Exit Without Saving",
            width=20,
            command=lambda: self._exit_to_menu(modal)
        ).pack(pady=5)

        ttk.Button(
            modal,
            text="Cancel",
            width=20,
            command=modal.destroy
        ).pack(pady=5)

    def undo_move(self):
        if self.board.undo():
            self.hovered_cell = None
            self.draw_board()

    def redo_move(self):
        if self.board.redo():
            self.hovered_cell = None
            self.draw_board()

    def _exit(self, modal, save):
        if save:
            self.save_game()
        modal.destroy()
        self.master.show_main_menu()

    def save_game(self, exit_after=False):
        modal = tk.Toplevel(self)
        modal.title("Save Game")
        modal.geometry("300x150")
        modal.transient(self)
        modal.grab_set()

        ttk.Label(modal, text="Save name:").pack(pady=10)

        name_entry = tk.Entry(modal, width=30)
        name_entry.pack(pady=5)
        name_entry.focus()

        ttk.Button(
            modal,
            text="Save",
            command=lambda: self._save_with_name(
                name_entry.get(), modal, exit_after
            )
        ).pack(pady=10)

    def _save_with_name(self, name, modal, exit_after):
        if not name.strip():
            return

        all_saves = self._load_all_saves()
        all_saves[name] = self.board.to_dict()

        self._write_all_saves(all_saves)

        modal.destroy()

        if exit_after:
            self.master.show_main_menu()

    def on_hover(self, event):
        pos = self.pixel_to_hex(event.x, event.y)
        if pos != self.hovered_cell:
            self.hovered_cell = pos
            self.draw_board()

    def clear_hover(self, event):
        if self.hovered_cell is not None:
            self.hovered_cell = None
            self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")

        valid_mouse_moves = []
        valid_wall_moves = []

        if self.board.game_type == "1vs1" and self.board.is_mouse_turn():
            valid_mouse_moves = self.board.get_neighbors()

        if (
                self.board.game_type == "singleplayer"
                or (self.board.game_type == "1vs1" and self.board.is_wall_turn())
        ):
            valid_wall_moves = [
                (r, c)
                for r in range(self.board.SIZE)
                    for c in range(self.board.SIZE)
                        if self.board.is_free((r, c)) and (r, c) != self.board.mouse_pos
            ]

        for row in range(self.board.SIZE):
            for col in range(self.board.SIZE):
                cx, cy = self.hex_center(row, col)
                cell = (row, col)

                if cell in self.board.walls:
                    color = self.COLOR_WALL
                elif cell == self.hovered_cell and cell in valid_mouse_moves:
                    color = self.COLOR_HOVER
                elif cell == self.hovered_cell and cell in valid_wall_moves:
                    color = self.COLOR_WALL_HOVER
                else:
                    color = self.COLOR_EMPTY
                self.draw_hex(cx + 2, cy + 2, self.HEX_RADIUS, "#999999")
                self.draw_hex(cx, cy, self.HEX_RADIUS, color)
                if cell == self.board.mouse_pos:
                    self.canvas.create_text(
                        cx,
                        cy,
                        text="🐭",
                        font=("Apple Color Emoji", 30),
                    )

                if (
                        self.board.game_type == "1vs1"
                        and self.board.is_mouse_turn()
                        and cell in valid_mouse_moves
                ):
                    self.canvas.create_oval(
                        cx - self.DOT_RADIUS,
                        cy - self.DOT_RADIUS,
                        cx + self.DOT_RADIUS,
                        cy + self.DOT_RADIUS,
                        fill=self.DOT_COLOR,
                        outline=""
                    )
        self.update_info()

    def draw_hex(self, cx, cy, r, fill):
        points = []
        for i in range(6):
            angle = math.radians(60 * i - 30)
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            points.extend([x, y])

        self.canvas.create_polygon(
            points,
            fill=fill,
            outline=self.COLOR_OUTLINE,
            width=2
        )

    def hex_center(self, row, col):
        x = self.PADDING + col * self.hex_w
        y = self.PADDING + row * self.hex_h

        if row % 2 == 1:
            x += self.hex_w / 2

        return x, y

    def on_click(self, event):
        pos = self.pixel_to_hex(event.x, event.y)
        if pos is None:
            return

        if self.board.game_type == "singleplayer":
            if self.board.place_wall(pos):

                self.board.move_mouse_ai()

                if self.board.mouse_escaped():
                    self.draw_board()
                    self.master.show_lose_scene()
                    return

                if self.board.mouse_trapped():
                    self.draw_board()
                    self.master.show_win_scene()
                    return

                self.draw_board()



        else:
            if self.board.is_wall_turn():
                if self.board.place_wall(pos):
                    if self.board.mouse_trapped():
                        self.draw_board()
                        self.master.show_win_scene()
                        return
                    self.draw_board()
                return
            if self.board.is_mouse_turn():
                if self.board.mouse_trapped():
                    self.draw_board()
                    self.master.show_win_scene()
                    return
                if pos in self.board.get_neighbors():
                    self.board.move_mouse(pos)
                    if self.board.mouse_escaped():
                        self.draw_board()
                        self.master.show_lose_scene()
                        return
                    self.draw_board()

    def pixel_to_hex(self, x, y):
        for row in range(self.board.SIZE):
            for col in range(self.board.SIZE):
                cx, cy = self.hex_center(row, col)
                if math.dist((x, y), (cx, cy)) <= self.HEX_RADIUS:
                    return (row, col)
        return None

    def _load_all_saves(self):
        try:
            with open(self.SAVE_FILE, "r") as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def _open_save_then_exit(self, confirm_modal):
        confirm_modal.destroy()
        self.save_game(exit_after=True)

    def _exit_to_menu(self, confirm_modal):
        confirm_modal.destroy()
        self.master.show_main_menu()

    def _write_all_saves(self, data):
        with open(self.SAVE_FILE, "w") as f:
            json.dump(data, f, indent=2)

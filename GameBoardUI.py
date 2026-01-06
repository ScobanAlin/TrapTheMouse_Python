import tkinter as tk
import math


class GameBoardUI(tk.Frame):
    HEX_RADIUS = 28
    PADDING = 50

    COLOR_EMPTY = "#c8f26d"
    COLOR_WALL = "#8b4513"
    COLOR_MOUSE = "#ff4d4d"
    COLOR_OUTLINE = "#6aa84f"

    def __init__(self, master, game_board):
        super().__init__(master, bg="#9acd32")
        self.board = game_board

        self.canvas = tk.Canvas(
            self,
            bg="#9acd32",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.hex_height = math.sqrt(3) * self.HEX_RADIUS
        self.hex_width = 2 * self.HEX_RADIUS

        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_board()


    def draw_board(self):
        self.canvas.delete("all")

        for row in range(self.board.SIZE):
            for col in range(self.board.SIZE):
                cx, cy = self.hex_center(row, col)
                cell = (row, col)

                if cell == self.board.mouse_pos:
                    color = self.COLOR_MOUSE
                elif cell in self.board.walls:
                    color = self.COLOR_WALL
                else:
                    color = self.COLOR_EMPTY

                self.draw_hex(cx, cy, self.HEX_RADIUS, color)

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
        x = self.PADDING + col * self.hex_width
        y = self.PADDING + row * self.hex_height

        if row % 2 == 1:
            x += self.hex_width / 2

        return x, y

    def on_click(self, event):
        pos = self.pixel_to_hex(event.x, event.y)
        if pos is None:
            return


        if self.board.game_type == "singleplayer":
            if self.board.place_wall(pos):

                prev_pos = self.board.mouse_pos
                self.board.move_mouse_ai()

                if self.board.mouse_escaped():
                    self.draw_board()
                    self.master.show_lose_scene()
                    return

                if self.board.mouse_trapped():
                    self.draw_board()
                    self.master.show_win_scene()
                    return

                self.board.next_turn()
                self.draw_board()



        else:
            if self.board.is_wall_turn():
                if self.board.place_wall(pos):
                    self.board.switch_player()
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
                    self.board.switch_player()
                    self.draw_board()

    def pixel_to_hex(self, x, y):
        for row in range(self.board.SIZE):
            for col in range(self.board.SIZE):
                cx, cy = self.hex_center(row, col)
                if math.dist((x, y), (cx, cy)) <= self.HEX_RADIUS:
                    return (row, col)
        return None



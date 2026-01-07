import random
class GameBoard:
    SIZE = 11

    def __init__(self, game_type, difficulty=None):
        self.game_type = game_type
        self.difficulty = difficulty
        self.turn = 0
        self.current_player = "walls"
        self.score = 20000
        self.mouse_pos = (self.SIZE // 2, self.SIZE // 2)
        self.walls = set()
        self._init_walls()


    def _init_walls(self):

        if self.difficulty == "easy":
            wall_count = random.randint(8, 12)
        elif self.difficulty == "medium":
            wall_count = random.randint(13, 18)
        elif self.difficulty == "hard":
            wall_count = random.randint(19, 25)
        else:
            wall_count = random.randint(10, 15)

        while len(self.walls) < wall_count:
            x = random.randint(0, self.SIZE - 1)
            y = random.randint(0, self.SIZE - 1)

            if (x, y) != self.mouse_pos:
                self.walls.add((x, y))



    def is_inside_board(self, pos):
        x, y = pos
        return 0 <= x < self.SIZE and 0 <= y < self.SIZE

    def is_wall(self, pos):
        return pos in self.walls

    def is_free(self, pos):
        return self.is_inside_board(pos) and pos not in self.walls

    def is_wall_turn(self):
        return self.current_player == "walls"

    def is_mouse_turn(self):
        return self.current_player == "mouse"

    def switch_player(self):
        self.current_player = "mouse" if self.current_player == "walls" else "walls"


    def next_turn(self):
        self.turn += 1

    def place_wall(self, pos):
        if self.is_free(pos) and pos != self.mouse_pos:
            self.walls.add(pos)
            self.score = max(0, self.score - 50)
            return True
        return False

    def move_mouse(self, new_pos):
        if self.is_free(new_pos):
            self.mouse_pos = new_pos
            return True
        return False


    def mouse_escaped(self):
        x, y = self.mouse_pos
        return x == 0 or y == 0 or x == self.SIZE - 1 or y == self.SIZE - 1

    def mouse_trapped(self):
        return len(self.get_neighbors()) == 0

    def get_neighbors(self, pos=None):
        if pos is None:
            pos = self.mouse_pos

        r, c = pos

        if r % 2 == 0:
            directions = [
                (-1, -1), (-1, 0),
                (0, -1), (0, 1),
                (1, -1), (1, 0)
            ]
        else:
            directions = [
                (-1, 0), (-1, 1),
                (0, -1), (0, 1),
                (1, 0), (1, 1)
            ]

        neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if self.is_free((nr, nc)):
                neighbors.append((nr, nc))

        return neighbors

    def move_mouse_ai(self):
        if self.game_type != "singleplayer":
            return


        if self.difficulty == "easy":
            self.move_greedy()
        elif self.difficulty == "medium":
            self.move_bfs()
        elif self.difficulty == "hard":
            self.move_astar()


    def move_greedy(self):
        moves = self.get_neighbors()
        if not moves:
            return

        def distance_to_edge(pos):
            r, c = pos
            return min(r, c, self.SIZE - 1 - r, self.SIZE - 1 - c)

        best_move = min(moves, key=distance_to_edge)
        self.mouse_pos = best_move

    def to_dict(self):
        return {
            "game_type": self.game_type,
            "difficulty": self.difficulty,
            "turn": self.turn,
            "current_player": self.current_player,
            "mouse_pos": self.mouse_pos,
            "walls": list(self.walls),
            "score": self.score,
        }

    def from_dict(data):
        board = GameBoard(data["game_type"], data["difficulty"])
        board.turn = data["turn"]
        board.current_player = data["current_player"]
        board.mouse_pos = tuple(data["mouse_pos"])
        board.walls = set(tuple(w) for w in data["walls"])
        board.score = data["score"]
        return board
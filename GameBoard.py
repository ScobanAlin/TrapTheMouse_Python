import random


class GameBoard:
    """GameBoard class , the engine of the game"""
    SIZE = 11

    def __init__(self, game_type, difficulty=None):
        """Initialize the game board"""
        self.game_type = game_type
        self.difficulty = difficulty
        self.turn = 0
        self.current_player = "walls"
        self.score = 20000
        self.mouse_pos = (self.SIZE // 2, self.SIZE // 2)
        self.walls = set()
        self._init_walls()
        self.undo_stack = []
        self.redo_stack = []

    def save_state(self):
        """Save the game board state"""
        self.undo_stack.append(self.to_dict())
        self.redo_stack.clear()

    def undo(self):
        """Undo the current game state"""
        if not self.undo_stack:
            return False

        self.redo_stack.append(self.to_dict())
        state = self.undo_stack.pop()
        self._restore_from_dict(state)
        return True

    def redo(self):
        """Redo the current game state"""
        if not self.redo_stack:
            return False

        self.undo_stack.append(self.to_dict())
        state = self.redo_stack.pop()
        self._restore_from_dict(state)
        return True



    def _init_walls(self):
        """Initializing the walls"""
        if self.difficulty == "easy":
            wall_count = random.randint(19, 25)
        elif self.difficulty == "medium":
            wall_count = random.randint(13, 18)
        elif self.difficulty == "hard":
            wall_count = random.randint(8, 12)
        else:
            wall_count = random.randint(10, 15)

        while len(self.walls) < wall_count:
            pos = (
                random.randint(0, self.SIZE - 1),
                random.randint(0, self.SIZE - 1),
            )
            if pos != self.mouse_pos:
                self.walls.add(pos)



    def is_inside_board(self, pos):
        """Query to see if a position is inside the board"""
        r, c = pos
        return 0 <= r < self.SIZE and 0 <= c < self.SIZE

    def is_free(self, pos):
        """Query to see if a position is not a wall"""
        return self.is_inside_board(pos) and pos not in self.walls

    def is_wall_turn(self):
        """Query to see if it is wall player turn"""
        return self.current_player == "walls"

    def is_mouse_turn(self):
        """Query to see if it is mouse player turn"""
        return self.current_player == "mouse"

    def switch_player(self):
        """Switch the current_player"""
        self.current_player = "mouse" if self.current_player == "walls" else "walls"

    def place_wall(self, pos):
        """Place a wall on the board"""
        if self.game_type == "1vs1" and not self.is_wall_turn():
            return False

        if self.is_free(pos) and pos != self.mouse_pos:
            self.save_state()
            self.walls.add(pos)
            self.score -= 50
            self.turn += 1

            if self.game_type == "1vs1":
                self.switch_player()

            return True
        return False

    def move_mouse(self, new_pos):
        """Move mouse for 1vs1"""
        if self.game_type == "1vs1" and not self.is_mouse_turn():
            return False

        if new_pos in self.get_neighbors():
            self.save_state()
            self.mouse_pos = new_pos
            self.turn += 1

            if self.game_type == "1vs1":
                self.switch_player()

            return True
        return False

    def mouse_escaped(self):
        """Querry to see if the mouse escaped in singleplayer"""
        r, c = self.mouse_pos
        return r == 0 or c == 0 or r == self.SIZE - 1 or c == self.SIZE - 1

    def mouse_escaped_pos(self, pos):
        """Querry to see if the mouse escaped based on a position for 1vs1"""
        r, c = pos
        return r == 0 or c == 0 or r == self.SIZE - 1 or c == self.SIZE - 1

    def mouse_trapped(self):
        """Querry to see if the mouse escaped"""
        return len(self.get_neighbors()) == 0

    def get_neighbors(self, pos=None):
        """Returns the neighbors of the current position if they are not walls """
        if pos is None:
            pos = self.mouse_pos

        r, c = pos

        if r % 2 == 0:
            directions = [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 0)]
        else:
            directions = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1)]

        neighbors = []
        for dr, dc in directions:
            nxt = (r + dr, c + dc)
            if self.is_free(nxt):
                neighbors.append(nxt)
        return neighbors

    def move_mouse_ai(self):
        """Move the mouse ai , separates the game difficulty"""
        if self.game_type != "singleplayer":
            return

        self.save_state()

        if self.difficulty == "easy":
            self.move_greedy()
        elif self.difficulty == "medium":
            self.move_bfs()
        elif self.difficulty == "hard":
            self.move_astar()

        self.turn += 1

    def move_greedy(self):
        """Move the game difficulty easy , using greedy , shortest path to margin"""
        moves = self.get_neighbors()
        if not moves:
            return

        def dist_to_edge(p):
            """Returns minimum distance from the mouse to the margin"""
            r, c = p
            return min(r, c, self.SIZE - 1 - r, self.SIZE - 1 - c)

        self.mouse_pos = min(moves, key=dist_to_edge)

    def _fallback_move(self):
        """Fallback move for bfs and a* when mouse is entrapped but still able to move, maximizez lifetime"""
        neighbors = self.get_neighbors()
        if not neighbors:
            return

        def survival_score(pos):
            """Kind of an heuristic for surviving most"""
            return (
                    -self._trap_penalty(pos)
                    - self._wall_density_penalty(pos)
                    + len(self.get_neighbors(pos)) * 2
            )

        self.mouse_pos = max(neighbors, key=survival_score)

    def move_bfs(self):
        """Move the game difficulty easy , using BFS, takes the first step from the first path to exit found"""
        start = self.mouse_pos
        queue = [(start, [])]
        visited = {start}

        while queue:
            current, path = queue.pop(0)

            if self.mouse_escaped_pos(current):
                if path:
                    self.mouse_pos = path[0]
                return

            for n in self.get_neighbors(current):
                if n not in visited:
                    visited.add(n)
                    queue.append((n, path + [n]))

        self._fallback_move()

    def _distance_to_edge(self, pos):
        """Returns the distance to the edge of the given position"""
        r, c = pos
        return min(r, c, self.SIZE - 1 - r, self.SIZE - 1 - c)

    def _trap_penalty(self, pos):
        """Returns the trap penalty for the given position for the heuristic"""
        return (6 - len(self.get_neighbors(pos))) * 2

    def _wall_density_penalty(self, pos):
        """Returns the wall density penalty for the given position for the heuristic ,"""
        r, c = pos
        penalty = 0
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                p = (r + dr, c + dc)
                if self.is_inside_board(p) and p in self.walls:
                    penalty += 0.5
        return penalty

    def _heuristic(self, pos):
        """"Returns the heuristic for the given position"""
        return (
            self._distance_to_edge(pos)
            + self._trap_penalty(pos)
            + self._wall_density_penalty(pos)
        )

    def move_astar(self):
        """"Move the game difficulty easy , using A* """
        start = self.mouse_pos
        open_list = [(self._heuristic(start), 0, start, [])]
        visited = {}

        while open_list:
            open_list.sort(key=lambda x: x[0])
            f, g, current, path = open_list.pop(0)

            if self.mouse_escaped_pos(current):
                if path:
                    self.mouse_pos = path[0]
                return

            if current in visited and visited[current] <= g:
                continue

            visited[current] = g

            for n in self.get_neighbors(current):
                ng = g + 1
                nf = ng + self._heuristic(n)
                open_list.append((nf, ng, n, path + [n]))

        self._fallback_move()


    def to_dict(self):
        """Makes a GameBoard object into a dictionary for saving into json"""
        return {
            "game_type": self.game_type,
            "difficulty": self.difficulty,
            "turn": self.turn,
            "current_player": self.current_player,
            "mouse_pos": self.mouse_pos,
            "walls": list(self.walls),
            "score": self.score,
        }

    @staticmethod
    def from_dict(data):
        """parses a GameBoard object from json into a GameBoard object"""
        board = GameBoard(data["game_type"], data["difficulty"])
        board._restore_from_dict(data)
        return board

    def _restore_from_dict(self, data):
        """Helper function for extracting data"""
        self.game_type = data["game_type"]
        self.difficulty = data["difficulty"]
        self.turn = data["turn"]
        self.current_player = data["current_player"]
        self.mouse_pos = tuple(data["mouse_pos"])
        self.walls = set(tuple(w) for w in data["walls"])
        self.score = data["score"]

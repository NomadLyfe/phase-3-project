from .alphabeta import alphabeta, CustomEvalFn


class MiniChessGame:
    def __init__(self, board, active_color):
        self.board = board
        self.active_color = active_color

    def get_player_moves(self, player):
        return self._generate_legal_moves(player.color)

    def get_opponent_moves(self, player):
        return self._generate_legal_moves(
            "black" if player.color == "white" else "white"
        )

    def get_active_moves(self):
        return self._generate_legal_moves(self.active_color)

    def forecast_move(self, move):
        new_board = [row[:] for row in self.board]
        from_sq, to_sq = move
        fx, fy = from_sq
        tx, ty = to_sq
        new_board[tx][ty] = new_board[fx][fy]
        new_board[fx][fy] = None
        return (
            MiniChessGame(
                new_board, "black" if self.active_color == "white" else "white"
            ),
            False,
            None,
        )

    def get_player_position(self, player):
        positions = []
        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if piece and self._piece_color(piece) == player.color:
                    positions.append((x, y))
        return positions

    def _piece_color(self, piece):
        return "white" if piece.isupper() else "black"

    def _generate_legal_moves(self, color):
        moves = []
        direction = -1 if color == "white" else 1

        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if not piece or self._piece_color(piece) != color:
                    continue

                if piece.lower() == "p":
                    nx = x + direction
                    if 0 <= nx < 8:
                        if self.board[nx][y] is None:
                            moves.append(((x, y), (nx, y)))
                            start_row = 6 if color == "white" else 1
                            nx2 = x + 2 * direction
                            if x == start_row and self.board[nx2][y] is None:
                                moves.append(((x, y), (nx2, y)))
                        for dy in [-1, 1]:
                            ny = y + dy
                            if 0 <= ny < 8:
                                target = self.board[nx][ny]
                                if target and self._piece_color(target) != color:
                                    moves.append(((x, y), (nx, ny)))

                elif piece.lower() == "n":
                    for dx, dy in [
                        (-2, -1),
                        (-2, 1),
                        (-1, -2),
                        (-1, 2),
                        (1, -2),
                        (1, 2),
                        (2, -1),
                        (2, 1),
                    ]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < 8 and 0 <= ny < 8:
                            target = self.board[nx][ny]
                            if not target or self._piece_color(target) != color:
                                moves.append(((x, y), (nx, ny)))

                elif piece.lower() in ["b", "r", "q"]:
                    directions = []
                    if piece.lower() in ["b", "q"]:
                        directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
                    if piece.lower() in ["r", "q"]:
                        directions += [(0, -1), (-1, 0), (0, 1), (1, 0)]

                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        while 0 <= nx < 8 and 0 <= ny < 8:
                            target = self.board[nx][ny]
                            if target:
                                if self._piece_color(target) != color:
                                    moves.append(((x, y), (nx, ny)))
                                break
                            moves.append(((x, y), (nx, ny)))
                            nx += dx
                            ny += dy
        return moves


class MiniPlayer:
    def __init__(self, color):
        self.color = color
        self.eval_fn = CustomEvalFn()
        self.utility = lambda game, my_turn: self.eval_fn.score(game, self)
        self.killer_moves = {}
        self.completed = True
        self.max_time = None
        self.time_start = 0

    def store_killer_move(self, depth, move):
        if depth not in self.killer_moves:
            self.killer_moves[depth] = []
        self.killer_moves[depth].append(move)


def get_best_move(board, color):
    game = MiniChessGame(board, color)
    player = MiniPlayer(color)
    move, value = alphabeta(player, game, time_left=lambda: 1000, depth=2)
    return move

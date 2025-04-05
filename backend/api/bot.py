from .alphabeta import alphabeta, CustomEvalFn
from .chess_objects import ChessGame, Knight


class Player:
    def __init__(self, color, game):
        self.color = color
        self.eval_fn = CustomEvalFn(game, color)
        self.utility = lambda game, my_turn: self.eval_fn.score(game, self)
        self.killer_moves = {}
        self.completed = True
        self.max_time = None
        self.time_start = 0

    def store_killer_move(self, depth, move):
        if depth not in self.killer_moves:
            self.killer_moves[depth] = []
        self.killer_moves[depth].append(move)


def get_best_move(game, color):
    print(f"[BOT] AI Turn: {color}")
    for i, row in enumerate(game.board):
        for j, piece in enumerate(row):
            if piece and isinstance(piece, Knight):
                print(f"[BOT] Knight at {piece.pos} on board[{i}][{j}]")
    player = Player(color, game)
    move, value = alphabeta(player, game, time_left=lambda: 1000, depth=2)
    return move

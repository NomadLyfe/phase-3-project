from copy import deepcopy
from math import inf as infinity
from .chess_objects import ChessGame


class Player:
    def __init__(self, color):
        self.color = color


def alphabeta(
    player, game, depth, alpha=-infinity, beta=infinity, maximizing=True, time_left=None
):
    if depth == 0 or game.is_checkmate(player.color):
        return None, CustomEvalFn(game, player.color)

    def max_value(game, depth, alpha, beta):
        best_move = None
        best_value = -infinity
        for piece, moves in game.all_moves(player.color):
            for m in moves:
                new_game = deepcopy(game)
                for i, row in enumerate(new_game.board):
                    for j, cell_piece in enumerate(row):  # fixed overwrite
                        if cell_piece:
                            cell_piece.pos = (i, j)
                new_game.move_piece(piece.pos, m)
                moved_piece = new_game.get_piece(m)
                if moved_piece:
                    moved_piece.pos = m
                _, v = alphabeta(player, new_game, depth - 1, alpha, beta, False)
                if v > best_value:
                    best_value = v
                    best_move = (piece.pos, m)
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
        return best_move, best_value

    def min_value(game, depth, alpha, beta):
        best_move = None
        best_value = infinity
        opponent_color = "black" if player.color == "white" else "white"
        for piece, moves in game.all_moves(opponent_color):
            for m in moves:
                new_game = deepcopy(game)
                for i, row in enumerate(new_game.board):
                    for j, cell_piece in enumerate(row):  # fixed overwrite
                        if cell_piece:
                            cell_piece.pos = (i, j)
                new_game.move_piece(piece.pos, m)
                moved_piece = new_game.get_piece(m)
                if moved_piece:
                    moved_piece.pos = m
                _, v = alphabeta(player, new_game, depth - 1, alpha, beta, True)
                if v < best_value:
                    best_value = v
                    best_move = (piece.pos, m)
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
        return best_move, best_value

    return (
        max_value(game, depth, alpha, beta)
        if maximizing
        else min_value(game, depth, alpha, beta)
    )


def CustomEvalFn(game, color):
    values = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 1000}
    total = 0
    for row in game.board:
        for piece in row:
            if piece:
                val = values.get(piece.symbol.upper(), 0)
                total += val if piece.color == color else -val
    return total

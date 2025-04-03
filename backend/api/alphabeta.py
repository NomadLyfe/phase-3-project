def alphabeta(
    player, game, time_left, depth, alpha=float("-inf"), beta=float("inf"), my_turn=True
):
    def max_value(state, curr_depth, alpha, beta):
        new_game_state, is_over, winner = state
        elapsed_time = player.time_start - time_left()
        if player.max_time and elapsed_time >= player.max_time:
            score = player.utility(new_game_state, my_turn)
            player.completed = False
            return score, None
        if is_over or curr_depth >= depth:
            score = player.utility(new_game_state, my_turn)
            return score, None
        v, move = float("-inf"), None
        killer_moves = player.killer_moves.get(curr_depth, [])
        # moves = sorted(
        #     new_game_state.get_player_moves(player),
        #     key=lambda m: (m in killer_moves, player.utility(new_game_state.forecast_move(m)[0], my_turn)),
        #     reverse=True,
        # )
        moves = sorted(
            new_game_state.get_player_moves(player),
            key=lambda m: (
                m in killer_moves,
                -len(new_game_state.forecast_move(m)[0].get_opponent_moves(player)),
                len(new_game_state.forecast_move(m)[0].get_player_moves(player)),
            ),
            reverse=True,
        )
        for a in moves:
            v2, a2 = min_value(
                new_game_state.forecast_move(a), curr_depth + 1, alpha, beta
            )
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                player.store_killer_move(curr_depth, a)
                return v, move
        return v, move

    def min_value(state, curr_depth, alpha, beta):
        new_game_state, is_over, winner = state
        elapsed_time = player.time_start - time_left()
        if player.max_time and elapsed_time >= player.max_time:
            score = player.utility(new_game_state, my_turn)
            player.completed = False
            return score, None
        if is_over or curr_depth >= depth:
            score = player.utility(new_game_state, my_turn)
            return score, None
        v, move = float("inf"), None
        killer_moves = player.killer_moves.get(curr_depth, [])
        # moves = sorted(
        #     new_game_state.get_opponent_moves(player),
        #     key=lambda m: (m in killer_moves, player.utility(new_game_state.forecast_move(m)[0], my_turn)),
        # )
        moves = sorted(
            new_game_state.get_opponent_moves(player),
            key=lambda m: (
                m in killer_moves,
                -len(new_game_state.forecast_move(m)[0].get_opponent_moves(player)),
                len(new_game_state.forecast_move(m)[0].get_player_moves(player)),
            ),
        )
        for a in moves:
            v2, a2 = max_value(
                new_game_state.forecast_move(a), curr_depth + 1, alpha, beta
            )
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                player.store_killer_move(curr_depth, a)
                return v, move
        return v, move

    is_over = not game.get_active_moves()
    winner = None

    if my_turn:
        value, move = max_value((game, is_over, winner), 0, alpha, beta)
    else:
        value, move = min_value((game, is_over, winner), 0, alpha, beta)
    return move, value


class CustomEvalFn:
    def __init__(self):
        # You can load piece-square tables here if needed
        pass

    def _piece_color(self, piece):
        return "white" if piece.isupper() else "black"

    def score(self, game, my_player=None):
        board = game.board  # 2D array
        score = 0

        for row in board:
            for piece in row:
                if piece:
                    score += self.piece_value(piece)

        # Bonus for number of legal moves
        my_moves = game.get_player_moves(my_player)
        opp_moves = game.get_opponent_moves(my_player)
        capture_bonus = 0
        for move in my_moves:
            _, to = move
            tx, ty = to
            target = game.board[tx][ty]
            if target and self._piece_color(target) != my_player.color:
                capture_bonus += abs(self.piece_value(target)) * 1.5  # weighted

        mobility_bonus = len(my_moves) - 1.2 * len(opp_moves)
        return score + mobility_bonus + capture_bonus

    def piece_value(self, piece):
        values = {
            "P": 1,
            "p": -1,
            "N": 3,
            "n": -3,
            "B": 3,
            "b": -3,
            "R": 5,
            "r": -5,
            "Q": 9,
            "q": -9,
            "K": 0,
            "k": 0,
        }
        return values.get(piece, 0)

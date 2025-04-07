# chess_objs.py (updated with en passant, check, checkmate, and promotion logic)

from typing import List, Tuple, Optional

Position = Tuple[int, int]  # (row, col)


class Piece:
    def __init__(self, color: str, pos: Position):
        self.color = color
        self.pos = pos
        self.symbol = "?"

    def possible_moves(self, board, ignore_check=False) -> List[Position]:
        return []

    def is_enemy(self, other: "Piece") -> bool:
        return other and self.color != other.color

    def __repr__(self):
        return self.symbol.upper() if self.color == "white" else self.symbol.lower()


class King(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = "K"
        self.has_moved = False

    def possible_moves(self, board, ignore_check=False) -> List[Position]:
        moves = []
        x, y = self.pos
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if board.is_valid_square((nx, ny)) and board.is_empty_or_enemy(
                    (nx, ny), self.color
                ):
                    moves.append((nx, ny))

        if not self.has_moved and (ignore_check or not board.in_check(self.color)):
            row = 7 if self.color == "white" else 0
            if board.can_castle_kingside(self.color):
                moves.append((row, 6))
            if board.can_castle_queenside(self.color):
                moves.append((row, 2))

        return moves


class Queen(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = "Q"

    def possible_moves(self, board, ignore_check=False):
        return Rook(self.color, self.pos).possible_moves(board) + Bishop(
            self.color, self.pos
        ).possible_moves(board)


class Rook(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = "R"
        self.has_moved = False

    def possible_moves(self, board, ignore_check=False):
        return board.sliding_moves(
            self.pos, self.color, directions=[(1, 0), (-1, 0), (0, 1), (0, -1)]
        )


class Bishop(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = "B"

    def possible_moves(self, board, ignore_check=False):
        return board.sliding_moves(
            self.pos, self.color, directions=[(1, 1), (-1, -1), (-1, 1), (1, -1)]
        )


class Knight(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = "N"

    def possible_moves(self, board, ignore_check=False):
        x, y = self.pos
        deltas = [
            (2, 1),
            (1, 2),
            (-1, 2),
            (-2, 1),
            (-2, -1),
            (-1, -2),
            (1, -2),
            (2, -1),
        ]
        return [
            (x + dx, y + dy)
            for dx, dy in deltas
            if board.is_valid_square((x + dx, y + dy))
            and board.is_empty_or_enemy((x + dx, y + dy), self.color)
        ]


class Pawn(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = "P"
        self.just_moved_two = False

    def possible_moves(self, board, ignore_check=False):
        x, y = self.pos
        direction = -1 if self.color == "white" else 1
        moves = []

        one_step = (x + direction, y)
        if board.is_valid_square(one_step) and board.get_piece(one_step) is None:
            moves.append(one_step)
            two_step = (x + 2 * direction, y)
            if (
                (x == 6 and self.color == "white") or (x == 1 and self.color == "black")
            ) and board.get_piece(two_step) is None:
                moves.append(two_step)

        for dy in [-1, 1]:
            diag = (x + direction, y + dy)
            if board.is_valid_square(diag):
                target = board.get_piece(diag)
                if target and target.color != self.color:
                    moves.append(diag)
                # En passant
                adjacent = board.get_piece((x, y + dy))
                if (
                    isinstance(adjacent, Pawn)
                    and adjacent.color != self.color
                    and adjacent.just_moved_two
                ):
                    moves.append(diag)

        return moves


class ChessGame:
    def __init__(self, skip_setup=False):
        self.board: List[List[Optional[Piece]]] = [
            [None for _ in range(8)] for _ in range(8)
        ]
        self.turn = "white"
        if not skip_setup:
            self.setup_board()
        self.last_move: Optional[Tuple[Position, Position]] = None

    def setup_board(self):
        for i in range(8):
            self.board[6][i] = Pawn("white", (6, i))
            self.board[1][i] = Pawn("black", (1, i))

        placements = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i, cls in enumerate(placements):
            self.board[7][i] = cls("white", (7, i))
            self.board[0][i] = cls("black", (0, i))

    def is_valid_square(self, pos: Position) -> bool:
        x, y = pos
        return 0 <= x < 8 and 0 <= y < 8

    def get_piece(self, pos: Position) -> Optional[Piece]:
        x, y = pos
        return self.board[x][y]

    def is_empty_or_enemy(self, pos: Position, color: str) -> bool:
        piece = self.get_piece(pos)
        return piece is None or piece.color != color

    def is_enemy(self, pos: Position, color: str) -> bool:
        piece = self.get_piece(pos)
        return piece and piece.color != color

    def sliding_moves(
        self, pos: Position, color: str, directions: List[Tuple[int, int]]
    ) -> List[Position]:
        moves = []
        for dx, dy in directions:
            x, y = pos
            while True:
                x += dx
                y += dy
                if not self.is_valid_square((x, y)):
                    break
                if self.get_piece((x, y)) is None:
                    moves.append((x, y))
                elif self.is_enemy((x, y), color):
                    moves.append((x, y))
                    break
                else:
                    break
        return moves

    def in_check(self, color: str) -> bool:
        king_pos = None
        for row in self.board:
            for piece in row:
                if isinstance(piece, King) and piece.color == color:
                    king_pos = piece.pos
        for row in self.board:
            for piece in row:
                if (
                    piece
                    and piece.color != color
                    and king_pos in piece.possible_moves(self, ignore_check=True)
                ):
                    return True
        return False

    def can_castle_kingside(self, color: str) -> bool:
        row = 7 if color == "white" else 0
        king = self.get_piece((row, 4))
        rook = self.get_piece((row, 7))
        return (
            isinstance(king, King)
            and not king.has_moved
            and isinstance(rook, Rook)
            and not rook.has_moved
            and self.board[row][5] is None
            and self.board[row][6] is None
        )

    def can_castle_queenside(self, color: str) -> bool:
        row = 7 if color == "white" else 0
        king = self.get_piece((row, 4))
        rook = self.get_piece((row, 0))
        return (
            isinstance(king, King)
            and not king.has_moved
            and isinstance(rook, Rook)
            and not rook.has_moved
            and self.board[row][1] is None
            and self.board[row][2] is None
            and self.board[row][3] is None
        )

    def move_piece(self, from_pos: Position, to_pos: Position):
        piece = self.get_piece(from_pos)
        if not piece or piece.color != self.turn:
            return False

        # Reset en passant flags
        for row in self.board:
            for p in row:
                if isinstance(p, Pawn):
                    p.just_moved_two = False

        target = self.get_piece(to_pos)

        if isinstance(piece, King) and abs(to_pos[1] - from_pos[1]) == 2:
            if to_pos[1] > from_pos[1]:
                self.board[to_pos[0]][5] = self.get_piece((to_pos[0], 7))
                self.board[to_pos[0]][7] = None
            else:
                self.board[to_pos[0]][3] = self.get_piece((to_pos[0], 0))
                self.board[to_pos[0]][0] = None
            piece.has_moved = True

        if isinstance(piece, Rook):
            piece.has_moved = True

        if isinstance(piece, Pawn):
            if abs(to_pos[0] - from_pos[0]) == 2:
                piece.just_moved_two = True
            if to_pos[1] != from_pos[1] and target is None:
                self.board[from_pos[0]][to_pos[1]] = None
            if (to_pos[0] == 0 and piece.color == "white") or (
                to_pos[0] == 7 and piece.color == "black"
            ):
                self.board[to_pos[0]][to_pos[1]] = Queen(piece.color, to_pos)
                self.board[from_pos[0]][from_pos[1]] = None
                self.turn = "black" if self.turn == "white" else "white"
                return True

        self.board[from_pos[0]][from_pos[1]] = None
        self.board[to_pos[0]][to_pos[1]] = piece
        piece.pos = to_pos
        self.last_move = (from_pos, to_pos)
        self.turn = "black" if self.turn == "white" else "white"
        return True

    def all_moves(self, color: str) -> List[Tuple[Piece, List[Position]]]:
        result = []
        for row in self.board:
            for piece in row:
                if piece and piece.color == color:
                    result.append((piece, piece.possible_moves(self)))
        return result

    def is_checkmate(self, color: str) -> bool:
        if not self.in_check(color):
            return False

        for piece, moves in self.all_moves(color):
            for to_pos in moves:
                test_game = ChessGame.deserialize_board(self.serialize_board())
                test_game.turn = color
                if test_game.move_piece(piece.pos, to_pos) and not test_game.in_check(
                    color
                ):
                    return False  # Found a legal move that gets out of check

        return True  # No legal move gets out of check → checkmate

    def is_stalemate(self, color: str) -> bool:
        if self.in_check(color):
            return False

        for piece, moves in self.all_moves(color):
            for to_pos in moves:
                test_game = ChessGame.deserialize_board(self.serialize_board())
                test_game.turn = color
                if test_game.move_piece(piece.pos, to_pos) and not test_game.in_check(
                    color
                ):
                    return False

        return True

    def serialize_board(self):
        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if piece:
                    piece.pos = (i, j)
        return [[repr(p) if p else None for p in row] for row in self.board]

    @classmethod
    def deserialize_board(cls, data):
        piece_map = {
            "P": Pawn,
            "p": Pawn,
            "R": Rook,
            "r": Rook,
            "N": Knight,
            "n": Knight,
            "B": Bishop,
            "b": Bishop,
            "Q": Queen,
            "q": Queen,
            "K": King,
            "k": King,
        }
        game = cls(skip_setup=True)
        for i in range(8):
            for j in range(8):
                symbol = data[i][j]
                if symbol:
                    color = "white" if symbol.isupper() else "black"
                    piece_cls = piece_map[symbol]
                    game.board[i][j] = piece_cls(color, (i, j))
        return game

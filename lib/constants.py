PAWN = '\u265F'
KNIGHT = '\u265E'
ROOK = '\u265C'
BISHOP = '\u265D'
QUEEN = '\u265B'
KING = '\u265A'
EMPTY = '\u25FC'

black_text = "\033[30m{}\033[0m"
white_text = "\033[37m{}\033[0m"

B_PAWN = black_text.format(PAWN)
W_PAWN = white_text.format(PAWN)
B_EMPTY = black_text.format(EMPTY)
W_EMPTY = white_text.format(EMPTY)
B_KNIGHT = black_text.format(KNIGHT)
W_KNIGHT = white_text.format(KNIGHT)
B_BISHOP = black_text.format(BISHOP)
W_BISHOP = white_text.format(BISHOP)
B_ROOK = black_text.format(ROOK)
W_ROOK = white_text.format(ROOK)
B_QUEEN = black_text.format(QUEEN)
W_QUEEN = white_text.format(QUEEN)
B_KING = black_text.format(KING)
W_KING = white_text.format(KING)

WHITE_PIECES = {'K': W_KING, 'Q': W_QUEEN, 'B': W_BISHOP, 'R': W_ROOK, 'N': W_KNIGHT, 'P': W_PAWN}
BLACK_PIECES = {'K': B_KING, 'Q': B_QUEEN, 'B': B_BISHOP, 'R': B_ROOK, 'N': B_KNIGHT, 'P': B_PAWN}
EMPTY_SPACES = [B_EMPTY, W_EMPTY]

EMPTY_BOARD = [[W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY],
               [B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY],
               [W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY],
               [B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY],
               [W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY],
               [B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY],
               [W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY],
               [B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY]]

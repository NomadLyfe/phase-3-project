from constants import PAWN,KNIGHT,ROOK,BISHOP,QUEEN,KING,black_text,white_text,WHITE_PIECES,BLACK_PIECES,EMPTY_BOARD,LETTERS,NUMBERS,EMPTY_SPACES


class ChessPieceAction():

    def __init__(self, letter, number, turn_count, color):
        self.letter = letter
        self.number = number
        self.turn_count = turn_count
        self.color = color

    def capture(self, board_state, piece, pos):
        captured_piece = board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)]
        board_state[pos[1]][pos[0]] = EMPTY_BOARD[pos[1]][pos[0]]
        board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(piece)
        if self.color == white_text:
            self.turn_count += 1
        return captured_piece


class PawnAction(ChessPieceAction):

    def move(self, board_state, is_capture):
        for i, row in enumerate(board_state):
            for j, piece in enumerate(row):
                if piece == self.color.format(PAWN):
                    x_diff = LETTERS.index(self.letter) - j
                    y_diff = NUMBERS.index(self.number) - i
                    is_valid = True
                    if self.color == white_text and x_diff == 0:
                        if not (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES):
                            pass
                        elif y_diff == -1:
                            board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(PAWN)
                            board_state[NUMBERS.index(self.number)+1][LETTERS.index(self.letter)] = EMPTY_BOARD[NUMBERS.index(self.number)+1][LETTERS.index(self.letter)]
                            self.turn_count += 1
                            return True
                        elif y_diff == -2 and i == 6:
                            for k in range(1, abs(y_diff)):
                                if not (board_state[NUMBERS.index(self.number)-k][LETTERS.index(self.letter)] in EMPTY_SPACES):
                                    is_valid = False
                            if is_valid == True:
                                board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(PAWN)
                                board_state[NUMBERS.index(self.number)+2][LETTERS.index(self.letter)] = EMPTY_BOARD[NUMBERS.index(self.number)+2][LETTERS.index(self.letter)]
                                if self.color == white_text:
                                    self.turn_count += 1
                                return True
                    elif self.color == black_text and x_diff == 0:
                        if not (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES):
                            pass
                        elif y_diff == 1:
                            board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(PAWN)
                            board_state[NUMBERS.index(self.number)-1][LETTERS.index(self.letter)] = EMPTY_BOARD[NUMBERS.index(self.number)-1][LETTERS.index(self.letter)]
                            return True
                        elif y_diff == 2 and i == 1:
                            is_valid = True
                            for k in range(1, abs(y_diff)):
                                if (not board_state[NUMBERS.index(self.number)-k][LETTERS.index(self.letter)] in EMPTY_SPACES):
                                    is_valid = False
                            if is_valid == True:
                                board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(PAWN)
                                board_state[NUMBERS.index(self.number)-2][LETTERS.index(self.letter)] = EMPTY_BOARD[NUMBERS.index(self.number)-2][LETTERS.index(self.letter)]
                                if self.color == white_text:
                                    self.turn_count += 1
                                return True
    
    def capture(self, board_state):
        for i, row in enumerate(board_state):
            for j, piece in enumerate(row):
                if piece == self.color.format(PAWN):
                    x_diff = LETTERS.index(self.letter) - j
                    y_diff = NUMBERS.index(self.number) - i
                    if self.color == white_text and abs(x_diff) == 1 and y_diff == -1:
                        if board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in (EMPTY_SPACES + list(WHITE_PIECES.values())):
                            pass
                        elif board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values()):
                            board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(PAWN)
                            board_state[NUMBERS.index(self.number)-y_diff][LETTERS.index(self.letter)-x_diff] = EMPTY_BOARD[NUMBERS.index(self.number)-y_diff][LETTERS.index(self.letter)-x_diff]
                            self.turn_count += 1
                            return True
                    elif self.color == black_text and abs(x_diff) == 1 and y_diff == 1:
                        if board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in (EMPTY_SPACES + list(BLACK_PIECES.values())):
                            pass
                        elif board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values()):
                            board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(PAWN)
                            board_state[NUMBERS.index(self.number)-y_diff][LETTERS.index(self.letter)-x_diff] = EMPTY_BOARD[NUMBERS.index(self.number)-y_diff][LETTERS.index(self.letter)-x_diff]
                            self.turn_count += 1
                            return True


class KnightAction(ChessPieceAction):

    def move(self, board_state, is_capture):
        for i, row in enumerate(board_state):
            for j, piece in enumerate(row):
                if piece == self.color.format(KNIGHT):
                    x_diff = LETTERS.index(self.letter) - j
                    y_diff = NUMBERS.index(self.number) - i
                    if (abs(x_diff), abs(y_diff)) in [(1,2),(2,1)]:
                        if (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(WHITE_PIECES.values())) and self.color == white_text:
                            pass
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values())) and self.color == black_text:
                            pass
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values())) and self.color == white_text:
                            if is_capture:
                                self.capture(board_state, KNIGHT, (j, i))
                                return True
                            else:
                                input('\nIf you are trying to capture, ensure you are properly using "x" in your chess notation! Click "Enter" to continue...')
                                print('')
                                return False
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES):
                            board_state[i][j] = EMPTY_BOARD[i][j]
                            board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(KNIGHT)
                            if self.color == white_text:
                                self.turn_count += 1
                            return True
        return False

class RookAction(ChessPieceAction):

    def move(self, board_state, is_capture):
        for i, row in enumerate(board_state):
            for j, piece in enumerate(row):
                if piece == self.color.format(ROOK):
                    x_diff = LETTERS.index(self.letter) - j
                    y_diff = NUMBERS.index(self.number) - i
                    if (x_diff == 0) ^ (y_diff == 0):
                        r = x_diff if x_diff != 0 else y_diff
                        for k in range(1, abs(r)):
                            dirr = int(x_diff/abs(x_diff)) if x_diff != 0 else int(y_diff/abs(y_diff))
                            if not (board_state[NUMBERS.index(self.number)-(k*(dirr if y_diff != 0 else 0))][LETTERS.index(self.letter)-(k*(dirr if x_diff != 0 else 0))] in EMPTY_SPACES):
                                return False
                        if (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(WHITE_PIECES.values())) and self.color == white_text:
                            pass
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values())) and self.color == black_text:
                            pass
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values())) and self.color == white_text:
                            if is_capture:
                                self.capture(board_state, ROOK, (j, i))
                                return True
                            else:
                                print('\n\nIf you are trying to capture, ensure you are properly using "x" in your chess notation!')
                                return False
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES):
                            board_state[i][j] = EMPTY_BOARD[i][j]
                            board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(ROOK)
                            if self.color == white_text:
                                self.turn_count += 1
                            return True
        return False


class BishopAction(ChessPieceAction):

    def move(self, board_state, is_capture):
        for i, row in enumerate(board_state):
            for j, piece in enumerate(row):
                if piece == self.color.format(BISHOP):
                    x_diff = LETTERS.index(self.letter) - j
                    y_diff = NUMBERS.index(self.number) - i
                    if abs(x_diff) == abs(y_diff):
                        for k in range(1, abs(x_diff)):
                            x_dirr = int(x_diff/abs(x_diff))
                            y_dirr = int(y_diff/abs(y_diff))
                            if not (board_state[NUMBERS.index(self.number)-(k*y_dirr)][LETTERS.index(self.letter)-(k*x_dirr)] in EMPTY_SPACES):
                                print(x_diff, y_diff)
                                return False
                        if (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(WHITE_PIECES.values())) and self.color == white_text:
                            pass
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values())) and self.color == black_text:
                            pass
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values())) and self.color == white_text:
                            if is_capture:
                                self.capture(board_state, BISHOP, (j, i))
                                return True
                            else:
                                print('\n\nIf you are trying to capture, ensure you are properly using "x" in your chess notation!')
                                return False
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES):
                            board_state[i][j] = EMPTY_BOARD[i][j]
                            board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(BISHOP)
                            if self.color == white_text:
                                self.turn_count += 1
                            return True
        return False


class QueenAction(ChessPieceAction):

    def move(self, board_state, is_capture):
        for i, row in enumerate(board_state):
            for j, piece in enumerate(row):
                if piece == self.color.format(QUEEN):
                    x_diff = LETTERS.index(self.letter) - j
                    y_diff = NUMBERS.index(self.number) - i
                    if ((x_diff == 0) ^ (y_diff == 0)) or abs(x_diff) == abs(y_diff):
                        if x_diff == 0 or y_diff == 0:
                            r = x_diff if x_diff != 0 else y_diff
                            for k in range(1, abs(r)):
                                dirr = int(x_diff/abs(x_diff)) if x_diff != 0 else int(y_diff/abs(y_diff))
                                if not (board_state[NUMBERS.index(self.number)-(k*(dirr if y_diff != 0 else 0))][LETTERS.index(self.letter)-(k*(dirr if x_diff != 0 else 0))] in EMPTY_SPACES):
                                    return False
                        else:
                            for k in range(1, abs(x_diff)):
                                x_dirr = int(x_diff/abs(x_diff))
                                y_dirr = int(y_diff/abs(y_diff))
                                if not (board_state[NUMBERS.index(self.number)-(k*y_dirr)][LETTERS.index(self.letter)-(k*x_dirr)] in EMPTY_SPACES):
                                    print(x_diff, y_diff)
                                    return False
                        if (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values())) and self.color == black_text:
                            pass
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(WHITE_PIECES.values())) and self.color == white_text:
                            pass
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values())) and self.color == white_text:
                            if is_capture:
                                self.capture(board_state, QUEEN, (j, i))
                                return True
                            else:
                                print('\n\nIf you are trying to capture, ensure you are properly using "x" in your chess notation!')
                                return False
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES):
                            board_state[i][j] = EMPTY_BOARD[i][j]
                            board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(QUEEN)
                            if self.color == white_text:
                                self.turn_count += 1
                            return True
        return False


class KingAction(ChessPieceAction):

    def move(self, board_state, is_capture):
        for i, row in enumerate(board_state):
            for j, piece in enumerate(row):
                if piece == self.color.format(KING):
                    x_diff = LETTERS.index(self.letter) - j
                    y_diff = NUMBERS.index(self.number) - i
                    if (x_diff == 0 or y_diff == 0 or x_diff == y_diff or x_diff == -y_diff) and (abs(x_diff) == 1 or abs(y_diff) == 1):
                        if (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values())) and self.color == black_text:
                            pass
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(WHITE_PIECES.values())) and self.color == white_text:
                            pass
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values())) and self.color == white_text:
                            if is_capture:
                                self.capture(board_state, KING, (j, i))
                                return True
                            else:
                                print('\n\nIf you are trying to capture, ensure you are properly using "x" in your chess notation!')
                                return False
                        elif board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES:
                            board_state[i][j] = EMPTY_BOARD[i][j]
                            board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(KING)
                            if self.color == white_text:
                                self.turn_count += 1
                            return True
        return False

from constants import PAWN,KNIGHT,ROOK,BISHOP,QUEEN,KING,black_text,white_text,WHITE_PIECES,BLACK_PIECES,EMPTY_BOARD,LETTERS,NUMBERS,EMPTY_SPACES

class PawnAction():
    def __init__(self, letter, number, turn_count, color):
        self.letter = letter
        self.number = number
        self.turn_count = turn_count
        self.color = color
    def move(self, board_state):
        #break_out_flag = False
        for i, row in enumerate(board_state):
            for j, piece in enumerate(row):
                if piece == self.color.format(PAWN):
                    x_diff = LETTERS.index(self.letter) - j
                    y_diff = NUMBERS.index(self.number) - i
                    is_valid = True
                    if self.color == white_text and x_diff == 0:
                        if not board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES:
                            input('\nThat is an illegal move! Click "Enter" to continue...')
                            print('')
                        elif board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values()):
                            return False
                        elif y_diff == -1:
                            board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(PAWN)
                            board_state[NUMBERS.index(self.number)+1][LETTERS.index(self.letter)] = EMPTY_BOARD[NUMBERS.index(self.number)+1][LETTERS.index(self.letter)]
                            self.turn_count += 1
                            return True
                            #break_out_flag = True
                            #break
                        elif y_diff == -2 and i == 6:
                            for k in range(1, abs(y_diff)):
                                if (not board_state[NUMBERS.index(self.number)-k][LETTERS.index(self.letter)-k] in EMPTY_SPACES):
                                    is_valid = False
                            if is_valid == True:
                                board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(PAWN)
                                board_state[NUMBERS.index(self.number)+2][LETTERS.index(self.letter)] = EMPTY_BOARD[NUMBERS.index(self.number)+2][LETTERS.index(self.letter)]
                                if self.color == white_text:
                                    self.turn_count += 1
                                return True
                                #break_out_flag = True
                                #break
                    elif self.color == black_text and x_diff == 0:
                        if not board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES:
                            return False
                        elif board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(WHITE_PIECES.values()):
                            return False
                        elif y_diff == 1:
                            board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(PAWN)
                            board_state[NUMBERS.index(self.number)-1][LETTERS.index(self.letter)] = EMPTY_BOARD[NUMBERS.index(self.number)-1][LETTERS.index(self.letter)]
                            return True
                            #break_out_flag = True
                            #break
                        elif y_diff == 2 and i == 1:
                            is_valid = True
                            for k in range(1, abs(y_diff)):
                                if (not board_state[NUMBERS.index(self.number)-k][LETTERS.index(self.letter)-k] in EMPTY_SPACES):
                                    is_valid = False
                            if is_valid == True:
                                board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(PAWN)
                                board_state[NUMBERS.index(self.number)-2][LETTERS.index(self.letter)] = EMPTY_BOARD[NUMBERS.index(self.number)-2][LETTERS.index(self.letter)]
                                if self.color == white_text:
                                    self.turn_count += 1
                                return True
                                #break_out_flag = True
                                #break
    def capture(self, board_state):
        pass

class KnightAction():
    def __init__(self, letter, number, turn_count, color):
        self.letter = letter
        self.number = number
        self.turn_count = turn_count
        self.color = color
    def move(self, board_state):
        break_out_flag = False
        for i, row in enumerate(board_state):
            for j, piece in enumerate(row):
                if piece == self.color.format(KNIGHT):
                    x_diff = LETTERS.index(self.letter) - j
                    y_diff = NUMBERS.index(self.number) - i
                    if (abs(x_diff) == abs(y_diff) + 1 or abs(y_diff) == abs(x_diff) + 1) and (abs(x_diff) == 1 or abs(y_diff) == 1):
                        if (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(WHITE_PIECES.values())) and self.color == white_text:
                            input('\nThat is an illegal move! Click "Enter" to continue...')
                            print('')
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values())) and self.color == black_text:
                            return False
                        elif (not board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES) and self.color == white_text:
                            input('\nIf you are trying to capture, ensure you are properly using "x" in your chess notation! Click "Enter" to continue...')
                            print('')
                        else:
                            board_state[i][j] = EMPTY_BOARD[i][j]
                            board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(KNIGHT)
                            if self.color == white_text:
                                self.turn_count += 1
                            print(j, i, LETTERS.index(self.letter), NUMBERS.index(self.number))
                            return True
                            #break_out_flag = True
                            #break
            if break_out_flag:
                break
    def capture(self, board_state):
        pass

class RookAction():
    def __init__(self, letter, number, turn_count, color):
        self.letter = letter
        self.number = number
        self.turn_count = turn_count
        self.color = color
    def move(self, board_state):
        break_out_flag = False
        for i, row in enumerate(board_state):
            for j, piece in enumerate(row):
                if piece == self.color.format(ROOK):
                    x_diff = LETTERS.index(self.letter) - j
                    y_diff = NUMBERS.index(self.number) - i
                    if x_diff == 0 or y_diff == 0:
                        is_valid = True
                        if x_diff == 0:
                            for k in range(1, abs(y_diff)):
                                if y_diff > 0:
                                    if (not board_state[NUMBERS.index(self.number)-k][LETTERS.index(self.letter)] in EMPTY_SPACES):
                                        is_valid = False
                                else:
                                    if (not board_state[NUMBERS.index(self.number)+k][LETTERS.index(self.letter)] in EMPTY_SPACES):
                                        is_valid = False
                        else:
                            for k in range(1, abs(x_diff)):
                                if x_diff > 0:
                                    if (not board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)-k] in EMPTY_SPACES):
                                        is_valid = False
                                else:
                                    if (not board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)+k] in EMPTY_SPACES):
                                        is_valid = False
                        if (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values())) and self.color == white_text:
                            input('\nIf you are trying to capture, ensure you are properly using "x" in your chess notation! Click "Enter" to continue...')
                            print('')
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values())) and self.color == black_text:
                            return False
                        elif is_valid and (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES):
                            board_state[i][j] = EMPTY_BOARD[i][j]
                            board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(ROOK)
                            if self.color == white_text:
                                self.turn_count += 1
                            return True
                            #break_out_flag = True
                            #break
                        elif self.color == white_text:
                            input('\nThat is an illegal move! Click "Enter" to continue...')
                            print('')
            if break_out_flag:
                break
    def capture(self, board_state):
        pass

class BishopAction():
    def __init__(self, letter, number, turn_count, color):
        self.letter = letter
        self.number = number
        self.turn_count = turn_count
        self.color = color
    def move(self, board_state):
        break_out_flag = False
        for i, row in enumerate(board_state):
            for j, piece in enumerate(row):
                if piece == self.color.format(BISHOP):
                    x_diff = LETTERS.index(self.letter) - j
                    y_diff = NUMBERS.index(self.number) - i
                    if (x_diff == y_diff) or (x_diff == -y_diff):
                        is_valid = True
                        for k in range(1, abs(x_diff)):
                            if x_diff == y_diff and x_diff > 0:
                                if (not board_state[NUMBERS.index(self.number)-k][LETTERS.index(self.letter)-k] in EMPTY_SPACES):
                                    is_valid = False
                            elif x_diff != y_diff and x_diff < 0:
                                if (not board_state[NUMBERS.index(self.number)-k][LETTERS.index(self.letter)+k] in EMPTY_SPACES):
                                    is_valid = False
                            elif x_diff != y_diff and y_diff < 0:
                                if (not board_state[NUMBERS.index(self.number)+k][LETTERS.index(self.letter)-k] in EMPTY_SPACES):
                                    is_valid = False
                            else:
                                if (not board_state[NUMBERS.index(self.number)+k][LETTERS.index(self.letter)+k] in EMPTY_SPACES):
                                    is_valid = False
                        if (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values())) and self.color == white_text:
                            input('\nIf you are trying to capture, ensure you are properly using "x" in your chess notation! Click "Enter" to continue...')
                            print('')
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values())) and self.color == black_text:
                            return False
                        elif is_valid and (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES):
                            board_state[i][j] = EMPTY_BOARD[i][j]
                            board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(BISHOP)
                            if self.color == white_text:
                                self.turn_count += 1
                            return True
                            #break_out_flag = True
                            #break
                        elif self.color == white_text:
                            input('\nThat is an illegal move! Click "Enter" to continue...')
                            print('')
            if break_out_flag:
                break
    def capture(self, board_state):
        pass

class QueenAction():
    def __init__(self, letter, number, turn_count, color):
        self.letter = letter
        self.number = number
        self.turn_count = turn_count
        self.color = color
    def move(self, board_state):
        break_out_flag = False
        for i, row in enumerate(board_state):
            for j, piece in enumerate(row):
                if piece == self.color.format(QUEEN):
                    x_diff = LETTERS.index(self.letter) - j
                    y_diff = NUMBERS.index(self.number) - i
                    if (x_diff == 0) or (y_diff == 0) or (x_diff == y_diff) or (x_diff == -y_diff):
                        is_valid = True
                        if x_diff == 0:
                            for k in range(1, abs(y_diff)):
                                if y_diff > 0:
                                    if (not board_state[NUMBERS.index(self.number)-k][LETTERS.index(self.letter)] in EMPTY_SPACES):
                                        is_valid = False
                                else:
                                    if (not board_state[NUMBERS.index(self.number)+k][LETTERS.index(self.letter)] in EMPTY_SPACES):
                                        is_valid = False
                        elif y_diff == 0:
                            for k in range(1, abs(x_diff)):
                                if x_diff > 0:
                                    if (not board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)-k] in EMPTY_SPACES):
                                        is_valid = False
                                else:
                                    if (not board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)+k] in EMPTY_SPACES):
                                        is_valid = False
                        else:
                            for k in range(1, abs(x_diff)):
                                if x_diff == y_diff and x_diff > 0:
                                    if (not board_state[NUMBERS.index(self.number)-k][LETTERS.index(self.letter)-k] in EMPTY_SPACES):
                                        is_valid = False
                                elif x_diff != y_diff and x_diff < 0:
                                    if (not board_state[NUMBERS.index(self.number)-k][LETTERS.index(self.letter)+k] in EMPTY_SPACES):
                                        is_valid = False
                                elif x_diff != y_diff and y_diff < 0:
                                    if (not board_state[NUMBERS.index(self.number)+k][LETTERS.index(self.letter)-k] in EMPTY_SPACES):
                                        is_valid = False
                                else:
                                    if (not board_state[NUMBERS.index(self.number)+k][LETTERS.index(self.letter)+k] in EMPTY_SPACES):
                                        is_valid = False
                        if (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values())) and self.color == white_text:
                            input('\nIf you are trying to capture, ensure you are properly using "x" in your chess notation! Click "Enter" to continue...')
                            print('')
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values())) and self.color == black_text:
                            return False
                        elif is_valid and (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES):
                            board_state[i][j] = EMPTY_BOARD[i][j]
                            board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(QUEEN)
                            if self.color == white_text:
                                self.turn_count += 1
                            return True
                            #break_out_flag = True
                            #break
                        elif self.color == white_text:
                            input('\nThat is an illegal move! Click "Enter" to continue...')
                            print('')
            if break_out_flag:
                break
    def capture(self, board_state):
        pass

class KingAction():
    def __init__(self, letter, number, turn_count, color):
        self.letter = letter
        self.number = number
        self.turn_count = turn_count
        self.color = color
    def move(self, board_state):
        break_out_flag = False
        for i, row in enumerate(board_state):
            for j, piece in enumerate(row):
                if piece == self.color.format(KING):
                    x_diff = LETTERS.index(self.letter) - j
                    y_diff = NUMBERS.index(self.number) - i
                    if (x_diff == 0 or y_diff == 0 or x_diff == y_diff or x_diff == -y_diff) and (abs(x_diff) == 1 or abs(y_diff) == 1):
                        if (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values())) and self.color == white_text:
                            input('\nIf you are trying to capture, ensure you are properly using "x" in your chess notation! Click "Enter" to continue...')
                            print('')
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values())) and self.color == black_text:
                            return False
                        elif board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES:
                            board_state[i][j] = EMPTY_BOARD[i][j]
                            board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(KING)
                            if self.color == white_text:
                                self.turn_count += 1
                            return True
                            #break_out_flag = True
                            #break
                        elif self.color == white_text:
                            input('\nThat is an illegal move! Click "Enter" to continue...')
                            print('')
            if break_out_flag:
                break
    def capture(self, board_state):
        pass

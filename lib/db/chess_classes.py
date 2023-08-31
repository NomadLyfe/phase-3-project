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
    
    def lookforcheck(self, board_state, piece, pos):
        enemy_color = black_text if self.color == white_text else white_text
        pos_x_diff = 7 - LETTERS.index(self.letter)
        pos_y_diff = 7 - NUMBERS.index(self.number)
        neg_x_diff = 0 - LETTERS.index(self.letter)
        neg_y_diff = 0 - NUMBERS.index(self.number)
        if piece == QUEEN:
            for i in range(1, (pos_x_diff if pos_x_diff < pos_y_diff else pos_y_diff) + 1):
                if board_state[NUMBERS.index(self.number) + i][LETTERS.index(self.letter) + i] == enemy_color.format(KING):
                    no_in_between = True
                    for j in range(1, i):
                        if not (board_state[NUMBERS.index(self.number) + j][LETTERS.index(self.letter) + j] in EMPTY_SPACES):
                            no_in_between = False
                    if no_in_between:
                        return True
            for i in range(1, (abs(neg_x_diff) if abs(neg_x_diff) < pos_y_diff else pos_y_diff) + 1):
                if board_state[NUMBERS.index(self.number) + i][LETTERS.index(self.letter) - i] == enemy_color.format(KING):
                    no_in_between = True
                    for j in range(1, i):
                        if not (board_state[NUMBERS.index(self.number) + j][LETTERS.index(self.letter) - j] in EMPTY_SPACES):
                            no_in_between = False
                    if no_in_between:
                        return True
            for i in range(1, (pos_x_diff if pos_x_diff < abs(neg_y_diff) else abs(neg_y_diff))+1):
                if board_state[NUMBERS.index(self.number) - i][LETTERS.index(self.letter) + i] == enemy_color.format(KING):
                    no_in_between = True
                    for j in range(1, i):
                        if not (board_state[NUMBERS.index(self.number) - j][LETTERS.index(self.letter) + j] in EMPTY_SPACES):
                            no_in_between = False
                    if no_in_between:
                        return True
            for i in range(1, (abs(neg_x_diff) if abs(neg_x_diff) < abs(neg_y_diff) else abs(neg_y_diff)) + 1):
                if board_state[NUMBERS.index(self.number) - i][LETTERS.index(self.letter) - i] == enemy_color.format(KING):
                    no_in_between = True
                    for j in range(1, i):
                        if not (board_state[NUMBERS.index(self.number) - j][LETTERS.index(self.letter) - j] in EMPTY_SPACES):
                            no_in_between = False
                    if no_in_between:
                        return True
            for i in range(1, pos_x_diff + 1):
                if board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter) + i] == enemy_color.format(KING):
                    no_in_between = True
                    for j in range(1, i):
                        if not (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter) + j] in EMPTY_SPACES):
                            no_in_between = False
                    if no_in_between:
                        return True
            for i in range(1, pos_y_diff + 1):
                if board_state[NUMBERS.index(self.number) + i][LETTERS.index(self.letter)] == enemy_color.format(KING):
                    no_in_between = True
                    for j in range(1, i):
                        if not (board_state[NUMBERS.index(self.number) + j][LETTERS.index(self.letter)] in EMPTY_SPACES):
                            no_in_between = False
                    if no_in_between:
                        return True
            for i in range(1, abs(neg_x_diff) + 1):
                if board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter) - i] == enemy_color.format(KING):
                    no_in_between = True
                    for j in range(1, i):
                        if not (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter) - j] in EMPTY_SPACES):
                            no_in_between = False
                    if no_in_between:
                        return True
            for i in range(1, abs(neg_y_diff) + 1):
                if board_state[NUMBERS.index(self.number) - i][LETTERS.index(self.letter)] == enemy_color.format(KING):
                    no_in_between = True
                    for j in range(1, i):
                        if not (board_state[NUMBERS.index(self.number) - j][LETTERS.index(self.letter)] in EMPTY_SPACES):
                            no_in_between = False
                    if no_in_between:
                        return True
            return False
        elif piece == BISHOP:
            for i in range(1, (pos_x_diff if pos_x_diff < pos_y_diff else pos_y_diff) + 1):
                if board_state[NUMBERS.index(self.number) + i][LETTERS.index(self.letter) + i] == enemy_color.format(KING):
                    no_in_between = True
                    for j in range(1, i):
                        if not (board_state[NUMBERS.index(self.number) + j][LETTERS.index(self.letter) + j] in EMPTY_SPACES):
                            no_in_between = False
                    if no_in_between:
                        return True
            for i in range(1, (abs(neg_x_diff) if abs(neg_x_diff) < pos_y_diff else pos_y_diff) + 1):
                if board_state[NUMBERS.index(self.number) + i][LETTERS.index(self.letter) - i] == enemy_color.format(KING):
                    no_in_between = True
                    for j in range(1, i):
                        if not (board_state[NUMBERS.index(self.number) + j][LETTERS.index(self.letter) - j] in EMPTY_SPACES):
                            no_in_between = False
                    if no_in_between:
                        return True
            for i in range(1, (pos_x_diff if pos_x_diff < abs(neg_y_diff) else abs(neg_y_diff))+1):
                if board_state[NUMBERS.index(self.number) - i][LETTERS.index(self.letter) + i] == enemy_color.format(KING):
                    no_in_between = True
                    for j in range(1, i):
                        if not (board_state[NUMBERS.index(self.number) - j][LETTERS.index(self.letter) + j] in EMPTY_SPACES):
                            no_in_between = False
                    if no_in_between:
                        return True
            for i in range(1, (abs(neg_x_diff) if abs(neg_x_diff) < abs(neg_y_diff) else abs(neg_y_diff)) + 1):
                if board_state[NUMBERS.index(self.number) - i][LETTERS.index(self.letter) - i] == enemy_color.format(KING):
                    no_in_between = True
                    for j in range(1, i):
                        if not (board_state[NUMBERS.index(self.number) - j][LETTERS.index(self.letter) - j] in EMPTY_SPACES):
                            no_in_between = False
                    if no_in_between:
                        return True
            return False
        elif piece == ROOK:
            for i in range(1, pos_x_diff + 1):
                if board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter) + i] == enemy_color.format(KING):
                    no_in_between = True
                    for j in range(1, i):
                        if not (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter) + j] in EMPTY_SPACES):
                            no_in_between = False
                    if no_in_between:
                        return True
            for i in range(1, pos_y_diff + 1):
                if board_state[NUMBERS.index(self.number) + i][LETTERS.index(self.letter)] == enemy_color.format(KING):
                    no_in_between = True
                    for j in range(1, i):
                        if not (board_state[NUMBERS.index(self.number) + j][LETTERS.index(self.letter)] in EMPTY_SPACES):
                            no_in_between = False
                    if no_in_between:
                        return True
            for i in range(1, abs(neg_x_diff) + 1):
                if board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter) - i] == enemy_color.format(KING):
                    no_in_between = True
                    for j in range(1, i):
                        if not (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter) - j] in EMPTY_SPACES):
                            no_in_between = False
                    if no_in_between:
                        return True
            for i in range(1, abs(neg_y_diff) + 1):
                if board_state[NUMBERS.index(self.number) - i][LETTERS.index(self.letter)] == enemy_color.format(KING):
                    no_in_between = True
                    for j in range(1, i):
                        if not (board_state[NUMBERS.index(self.number) - j][LETTERS.index(self.letter)] in EMPTY_SPACES):
                            no_in_between = False
                    if no_in_between:
                        return True
            return False
        elif piece == KNIGHT:
            if NUMBERS.index(self.number) < 7 and LETTERS.index(self.letter) < 6 and board_state[NUMBERS.index(self.number) + 1][LETTERS.index(self.letter) + 2] == enemy_color.format(KING):
                return True
            elif NUMBERS.index(self.number) < 7 and LETTERS.index(self.letter) > 1 and board_state[NUMBERS.index(self.number) + 1][LETTERS.index(self.letter) - 2] == enemy_color.format(KING):
                return True
            elif NUMBERS.index(self.number) > 0 and LETTERS.index(self.letter) < 6 and board_state[NUMBERS.index(self.number) - 1][LETTERS.index(self.letter) + 2] == enemy_color.format(KING):
                return True
            elif NUMBERS.index(self.number) > 0 and LETTERS.index(self.letter) > 1 and board_state[NUMBERS.index(self.number) - 1][LETTERS.index(self.letter) - 2] == enemy_color.format(KING):
                return True
            elif NUMBERS.index(self.number) < 6 and LETTERS.index(self.letter) < 7 and board_state[NUMBERS.index(self.number) + 2][LETTERS.index(self.letter) + 1] == enemy_color.format(KING):
                return True
            elif NUMBERS.index(self.number) < 6 and LETTERS.index(self.letter) > 0 and board_state[NUMBERS.index(self.number) + 2][LETTERS.index(self.letter) - 1] == enemy_color.format(KING):
                return True
            elif NUMBERS.index(self.number) > 1 and LETTERS.index(self.letter) < 7 and board_state[NUMBERS.index(self.number) - 2][LETTERS.index(self.letter) + 1] == enemy_color.format(KING):
                return True
            elif NUMBERS.index(self.number) > 1 and LETTERS.index(self.letter) > 0 and board_state[NUMBERS.index(self.number) - 2][LETTERS.index(self.letter) - 1] == enemy_color.format(KING):
                return True
            else:
                return False
        elif piece == PAWN:
            if (NUMBERS.index(self.number) == 7 and self.color == black_text) or (NUMBERS.index(self.number) == 7 and self.color == white_text):
                return False
            elif board_state[NUMBERS.index(self.number) + (1 if self.color == black_text else -1)][LETTERS.index(self.letter) + (-1 if LETTERS.index(self.letter) == 7 else 1)] == enemy_color.format(KING):
                return True
            elif board_state[NUMBERS.index(self.number) + (1 if self.color == black_text else -1)][LETTERS.index(self.letter) + (1 if LETTERS.index(self.letter) == 0 else -1)] == enemy_color.format(KING):
                return True
            else:
                return False
        return False
    
    def is_king_in_check(self):
        pass

    def is_king_in_mate(self):
        pass


class PawnAction(ChessPieceAction):

    def move(self, board_state, is_capture, is_check = False, is_mate = False):
        for i, row in enumerate(board_state):
            for j, piece in enumerate(row):
                if piece == self.color.format(PAWN):
                    x_diff = LETTERS.index(self.letter) - j
                    y_diff = NUMBERS.index(self.number) - i
                    check_for_check = self.lookforcheck(board_state, PAWN, (j,i))
                    if x_diff == 0 and not is_capture:
                        if not (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES):
                            pass
                        elif y_diff == (-1 if self.color == white_text else 1):
                            if is_check != check_for_check and not is_check:
                                print('\n\nThat move will place the enemy in check, please use "+" after the move if this is your intention.')
                            else:
                                if check_for_check and is_check:
                                    print('\n\nYou put Black in check!')
                                board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(PAWN)
                                board_state[i][j] = EMPTY_BOARD[i][j]
                                if self.color == white_text:
                                    self.turn_count += 1
                                return True
                        elif y_diff == (-2 if self.color == white_text else 2) and i == (6 if self.color == white_text else 1):
                            if not (board_state[5 if self.color == white_text else 2][LETTERS.index(self.letter)] in EMPTY_SPACES):
                                return False
                            board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(PAWN)
                            board_state[i][j] = EMPTY_BOARD[i][j]
                            if self.color == white_text:
                                self.turn_count += 1
                            return True
                    elif abs(x_diff) == 1 and y_diff == (-1 if self.color == white_text else 1) and is_capture:
                        if (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(WHITE_PIECES.values())) and self.color == white_text:
                            pass
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values())) and self.color == black_text:
                            pass
                        elif is_capture and not (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES):
                            if is_check != check_for_check and not is_check:
                                print('\n\nThat move will place the enemy in check, please use "+" after the move if this is your intention.')
                            else:
                                if check_for_check and is_check:
                                    print('\n\nYou put Black in check!')
                                captured_piece = board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)]
                                self.capture(board_state, PAWN, (j, i))
                                return captured_piece
                        elif self.color == white_text:
                            print('\n\nIf you are trying to capture, ensure you are properly using "x" in your chess notation!')
                            return False
        return False


class KnightAction(ChessPieceAction):

    def move(self, board_state, is_capture, is_check = False, is_mate = False):
        for i, row in enumerate(board_state):
            for j, piece in enumerate(row):
                if piece == self.color.format(KNIGHT):
                    x_diff = LETTERS.index(self.letter) - j
                    y_diff = NUMBERS.index(self.number) - i                    
                    if (abs(x_diff), abs(y_diff)) in [(1,2),(2,1)]:
                        check_for_check = self.lookforcheck(board_state, KNIGHT, (j,i))
                        if (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(WHITE_PIECES.values())) and self.color == white_text:
                            pass
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values())) and self.color == black_text:
                            pass
                        elif not (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES):
                            if is_capture:
                                if is_check != check_for_check and not is_check:
                                    print('\n\nThat move will place the enemy in check, please use "+" after the move if this is your intention.')
                                else:
                                    print(check_for_check)
                                    if check_for_check and is_check:
                                        print('\n\nYou put Black in check!')
                                    captured_piece = board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)]
                                    self.capture(board_state, KNIGHT, (j, i))
                                    return captured_piece
                            else:
                                print('\n\nIf you are trying to capture, ensure you are properly using "x" in your chess notation!')
                                return False
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES) and not is_capture:
                            if is_check != check_for_check and not is_check:
                                print('\n\nThat move will place the enemy in check, please use "+" after the move if this is your intention.')
                            else:
                                if check_for_check and is_check:
                                    print('\n\nYou put Black in check!')
                                board_state[i][j] = EMPTY_BOARD[i][j]
                                board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(KNIGHT)
                                if self.color == white_text:
                                    self.turn_count += 1
                                return True
        return False

class RookAction(ChessPieceAction):

    def move(self, board_state, is_capture, is_check = False, is_mate = False):
        for i, row in enumerate(board_state):
            for j, piece in enumerate(row):
                if piece == self.color.format(ROOK):
                    x_diff = LETTERS.index(self.letter) - j
                    y_diff = NUMBERS.index(self.number) - i
                    if (x_diff == 0) ^ (y_diff == 0):
                        check_for_check = self.lookforcheck(board_state, ROOK, (j,i))
                        print(check_for_check)
                        r = x_diff if x_diff != 0 else y_diff
                        for k in range(1, abs(r)):
                            dirr = int(x_diff/abs(x_diff)) if x_diff != 0 else int(y_diff/abs(y_diff))
                            if not (board_state[NUMBERS.index(self.number)-(k*(dirr if y_diff != 0 else 0))][LETTERS.index(self.letter)-(k*(dirr if x_diff != 0 else 0))] in EMPTY_SPACES):
                                return False
                        if (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(WHITE_PIECES.values())) and self.color == white_text:
                            pass
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values())) and self.color == black_text:
                            pass
                        elif not (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES):
                            if is_capture:
                                if is_check != check_for_check and not is_check:
                                    print('\n\nThat move will place the enemy in check, please use "+" after the move if this is your intention.')
                                else:
                                    if check_for_check and is_check:
                                        print('\n\nYou put Black in check!')
                                    captured_piece = board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)]
                                    self.capture(board_state, ROOK, (j, i))
                                    return captured_piece
                            else:
                                print('\n\nIf you are trying to capture, ensure you are properly using "x" in your chess notation!')
                                return False
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES) and not is_capture:
                            if is_check != check_for_check and not is_check:
                                print('\n\nThat move will place the enemy in check, please use "+" after the move if this is your intention.')
                            else:
                                if check_for_check and is_check:
                                    print('\n\nYou put Black in check!')
                                board_state[i][j] = EMPTY_BOARD[i][j]
                                board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(ROOK)
                                if self.color == white_text:
                                    self.turn_count += 1
                                return True
        return False


class BishopAction(ChessPieceAction):

    def move(self, board_state, is_capture, is_check = False, is_mate = False):
        for i, row in enumerate(board_state):
            for j, piece in enumerate(row):
                if piece == self.color.format(BISHOP):
                    x_diff = LETTERS.index(self.letter) - j
                    y_diff = NUMBERS.index(self.number) - i
                    if abs(x_diff) == abs(y_diff):
                        check_for_check = self.lookforcheck(board_state, BISHOP, (j,i))
                        for k in range(1, abs(x_diff)):
                            x_dirr = int(x_diff/abs(x_diff))
                            y_dirr = int(y_diff/abs(y_diff))
                            if not (board_state[NUMBERS.index(self.number)-(k*y_dirr)][LETTERS.index(self.letter)-(k*x_dirr)] in EMPTY_SPACES):
                                return False
                        if (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(WHITE_PIECES.values())) and self.color == white_text:
                            pass
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in list(BLACK_PIECES.values())) and self.color == black_text:
                            pass
                        elif not (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES):
                            if is_capture:
                                if is_check != check_for_check and not is_check:
                                    print('\n\nThat move will place the enemy in check, please use "+" after the move if this is your intention.')
                                else:
                                    if check_for_check and is_check:
                                        print('\n\nYou put Black in check!')
                                    captured_piece = board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)]
                                    self.capture(board_state, BISHOP, (j, i))
                                    return captured_piece
                            else:
                                print('\n\nIf you are trying to capture, ensure you are properly using "x" in your chess notation!')
                                return False
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES) and not is_capture:
                            if is_check != check_for_check and not is_check:
                                print('\n\nThat move will place the enemy in check, please use "+" after the move if this is your intention.')
                            else:
                                if check_for_check and is_check:
                                    print('\n\nYou put Black in check!')
                                board_state[i][j] = EMPTY_BOARD[i][j]
                                board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(BISHOP)
                                if self.color == white_text:
                                    self.turn_count += 1
                                return True
        return False


class QueenAction(ChessPieceAction):

    def move(self, board_state, is_capture, is_check = False, is_mate = False):
        for i, row in enumerate(board_state):
            for j, piece in enumerate(row):
                if piece == self.color.format(QUEEN):
                    x_diff = LETTERS.index(self.letter) - j
                    y_diff = NUMBERS.index(self.number) - i
                    if ((x_diff == 0) ^ (y_diff == 0)) or abs(x_diff) == abs(y_diff):
                        check_for_check = self.lookforcheck(board_state, QUEEN, (j,i))
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
                        elif not (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES):
                            if is_capture:
                                if is_check != check_for_check and not is_check:
                                    print('\n\nThat move will place the enemy in check, please use "+" after the move if this is your intention.')
                                else:
                                    if check_for_check and is_check:
                                        print('\n\nYou put Black in check!')
                                    captured_piece = board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)]
                                    self.capture(board_state, QUEEN, (j, i))
                                    return captured_piece
                            else:
                                print('\n\nIf you are trying to capture, ensure you are properly using "x" in your chess notation!')
                                return False
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES) and not is_capture:
                            if is_check != check_for_check and not is_check:
                                print('\n\nThat move will place the enemy in check, please use "+" after the move if this is your intention.')
                            else:
                                if check_for_check and is_check:
                                    print('\n\nYou put Black in check!')
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
                        elif not (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES):
                            if is_capture:
                                captured_piece = board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)]
                                self.capture(board_state, KING, (j, i))
                                return captured_piece
                            else:
                                print('\n\nIf you are trying to capture, ensure you are properly using "x" in your chess notation!')
                                return False
                        elif (board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] in EMPTY_SPACES) and not is_capture:
                            board_state[i][j] = EMPTY_BOARD[i][j]
                            board_state[NUMBERS.index(self.number)][LETTERS.index(self.letter)] = self.color.format(KING)
                            if self.color == white_text:
                                self.turn_count += 1
                            return True
        return False
    
    def castle(self, side, board_state):
        valid = False
        y = 0 if self.color == black_text else 7
        if board_state[y][4] == self.color.format(KING):
            if side == 'ks' and board_state[y][5] in EMPTY_SPACES and board_state[y][6] in EMPTY_SPACES and board_state[y][7] == self.color.format(ROOK):
                valid = True
            elif side == 'qs' and board_state[y][3] in EMPTY_SPACES and board_state[y][2] in EMPTY_SPACES and board_state[y][1] in EMPTY_SPACES and board_state[y][0] == self.color.format(ROOK):
                valid = True        
        if valid:
            board_state[y][4] = EMPTY_BOARD[y][4]
            board_state[y][4 + (2 if side == 'ks' else -2)] = self.color.format(KING)
            board_state[y][7 if side == 'ks' else 0] = EMPTY_BOARD[y][7 if side == 'ks' else 0]
            board_state[y][4 + (1 if side == 'ks' else -1)] = self.color.format(ROOK)
            return True
        else:
            return False

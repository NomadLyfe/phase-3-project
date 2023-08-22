import string
from random import choice as rc
from constants import B_ROOK,B_KNIGHT,B_BISHOP,B_QUEEN,B_KING,B_BISHOP,B_KNIGHT,B_ROOK,B_PAWN,W_ROOK,W_KNIGHT,W_BISHOP,W_QUEEN,W_KING,W_BISHOP,W_KNIGHT,W_ROOK,W_PAWN,W_EMPTY,B_EMPTY,PAWN,KNIGHT,ROOK,BISHOP,QUEEN,KING,black_text,white_text,WHITE_PIECES,BLACK_PIECES,LETTERS,NUMBERS
from chess_classes import Pawn,Knight,Rook,Bishop,Queen,King

board_state = [[B_ROOK,B_KNIGHT,B_BISHOP,B_QUEEN,B_KING,B_BISHOP,B_KNIGHT,B_ROOK],
               [B_PAWN,B_PAWN,B_PAWN,B_PAWN,B_PAWN,B_PAWN,B_PAWN,B_PAWN],
               [W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY],
               [B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY],
               [W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY],
               [B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY],
               [W_PAWN,W_PAWN,W_PAWN,W_PAWN,W_PAWN,W_PAWN,W_PAWN,W_PAWN],
               [W_ROOK,W_KNIGHT,W_BISHOP,W_QUEEN,W_KING,W_BISHOP,W_KNIGHT,W_ROOK]]

active_game = True
turn_count = 1
h = False
while active_game:
    print(f'Turn: {turn_count}\n\n    _________________________')
    for i in range(8):
        for j in range(11):
            if j == 0:
                print(NUMBERS[i] ,end='  ')
            elif j == 1:
                print('|', end=' ')
            elif j == 10:
                print('|')
            else:
                print(board_state[i][j-2], end='  ')
    print('    ', end='')
    for i in range (25):
        print('\u203E', end='')
    print('')
    print('     ', end='')
    for i in range(8):
        print(LETTERS[i], end='  ')
    print('\n')
    
    if not h:
        move = input("Enter your move using standard chess notation (Enter 'h' for help):  ")
    else:
        move = input("King: 'K', Queen: 'Q', Bishop: 'B', Rook: 'R', Knight: 'N', Pawn: ''.\n" \
                    "After the piece, write the space identifier with letter followed by number.\n" \
                    "A pawn's movement will just be the space identifier.\n" \
                    "Use an 'x' between the peice and the space to signify a capture.\n" \
                    "For pawn captures use starting column, followed by 'x' then space identifier.\n" \
                    "For Kingside castle: 'O-O'; for Queenside castle: 'O-O-O'.\n" \
                    "For check: input a '+' immidiately after the move.\n" \
                    "For checkmate: input a '#' immidiately after the move.\n" \
                    "Examples: 'Kb6', 'e4', Nxe4', 'exd5', 'O-O', 'Nd6+', 'Rh8#'.\n\n" \
                    "Tell me your move using standard chess notation:  ")
        h = False
    
    if move == 'h':
        h = True
    elif 'x' in move:
        if move[0] in string.ascii_uppercase:
            pass
        else:
            pass
    elif 'O' in move:
        pass
    elif '+' in move:
        pass
    elif '#' in move:
        pass
    else:
        if move[0] in string.ascii_uppercase:
            if WHITE_PIECES[move[0]] == white_text.format(KNIGHT):
                moving_knight = Knight(move[1], move[2], turn_count, white_text)
                moving_knight.move(board_state)
                turn_count = moving_knight.turn_count
            elif WHITE_PIECES[move[0]] == white_text.format(ROOK):
                moving_rook = Rook(move[1], move[2], turn_count, white_text)
                moving_rook.move(board_state)
                turn_count = moving_rook.turn_count
            elif WHITE_PIECES[move[0]] == white_text.format(BISHOP):
                moving_bishop = Bishop(move[1], move[2], turn_count, white_text)
                moving_bishop.move(board_state)
                turn_count = moving_bishop.turn_count
            elif WHITE_PIECES[move[0]] == white_text.format(KING):
                moving_king = King(move[1], move[2], turn_count, white_text)
                moving_king.move(board_state)
                turn_count = moving_king.turn_count
            elif WHITE_PIECES[move[0]] == white_text.format(QUEEN):
                moving_queen = Queen(move[1], move[2], turn_count, white_text)
                moving_queen.move(board_state)
                turn_count = moving_queen.turn_count
        else:
            moving_pawn = Pawn(move[0], move[1], turn_count, white_text)
            moving_pawn.move(board_state)
            turn_count = moving_pawn.turn_count
    
    if not h:
        is_move_possible = False
        while not is_move_possible:
            random_y = rc(range(len(board_state)))
            random_x = rc(range(len(board_state)))
            random_piece = board_state[random_y][random_x]
            while not random_piece in list(BLACK_PIECES.values()):
                random_y = rc(range(len(board_state)))
                random_x = rc(range(len(board_state)))
                random_piece = board_state[random_y][random_x]
            random_letter = rc(LETTERS)
            random_number = rc(NUMBERS)
            if random_piece == black_text.format(KNIGHT):
                moving_knight = Knight(random_letter, random_number, turn_count, black_text)
                if moving_knight.move(board_state):
                    is_move_possible = True
            elif random_piece == black_text.format(ROOK):
                moving_rook = Rook(random_letter, random_number, turn_count, black_text)
                if moving_rook.move(board_state):
                    is_move_possible = True
            elif random_piece == black_text.format(BISHOP):
                moving_bishop = Bishop(random_letter, random_number, turn_count, black_text)
                if moving_bishop.move(board_state):
                    is_move_possible = True
            elif random_piece == black_text.format(KING):
                moving_king = King(random_letter, random_number, turn_count, black_text)
                if moving_king.move(board_state):
                    is_move_possible = True
            elif random_piece == black_text.format(QUEEN):
                moving_queen = Queen(random_letter, random_number, turn_count, black_text)
                if moving_queen.move(board_state):
                    is_move_possible = True
            elif random_piece == black_text.format(PAWN):
                moving_pawn = Pawn(random_letter, random_number, turn_count, black_text)
                if moving_pawn.move(board_state):
                    is_move_possible = True
            print(f'{random_piece} at ({random_x}, {random_y}) going to ({random_letter}, {random_number}).')

import string
from random import choice as rc
from constants import B_ROOK,B_KNIGHT,B_BISHOP,B_QUEEN,B_KING,B_BISHOP,B_KNIGHT,B_ROOK,B_PAWN,KNIGHT,ROOK,BISHOP,QUEEN,KING,black_text,white_text,WHITE_PIECES,BLACK_PIECES,LETTERS,NUMBERS
from chess_classes import PawnAction,KnightAction,RookAction,BishopAction,QueenAction,KingAction
from models import Game, User, session

valid_login = False
user = None
while not valid_login:
    valid_login = True
    input_username = input("\n\nWelcome to Jeremy's CLI Chess Minigame! Play the computer and see how well you can do!\n\n\n" \
                    "If you are new, please enter a unique username (if you are a returning player, type in your username):  ")
    username_output = session.query(User.username).filter(User.username == input_username).first()
    if username_output == None:
        input_password = input("\n\nPlease enter a password for your account:  ")
        user = User(username = input_username, password = input_password)
    else:
        input_password = input("\n\nPlease enter your password:  ")
        password_output = session.query(User.password).filter(User.username == username_output[0]).first()
        if input_password == password_output[0]:
            user = session.query(User).filter(User.username == username_output[0]).first()
        else:
            input('\n\nThat is the wrong password! Click "enter" to be returned to the first page...')
            print(' ')
            valid_login = False
valid_selection = False
while not valid_selection:
    valid_selection = True
    print("\n\n       Welcome to the CLI Chess Minigame Main Menu       \n" \
              "          __________           ________________          \n" \
              "         | New Game |         | Hi-Score Chart |         \n" \
              "          ‾‾‾‾‾‾‾‾‾‾           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾          \n")
    selection = input('Please select an option by typing in the selection here:  ')
    if selection == 'New Game':
        h = False
        new_game = Game(turn_count = 1)
        board_state = new_game.board_state
        turn_count = new_game.turn_count
        active_game = new_game.active_game
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
            move = False
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
            possible = None
            if move == 'h':
                h = True
            elif not move:
                input('\nAn empty input is not a valid input! Click "Enter" to continue...')
                print('')
            elif 'x' in move:
                if move[0] in string.ascii_uppercase:
                    if WHITE_PIECES[move[0]] == white_text.format(KNIGHT):
                        knight_is_capture = KnightAction(move[2], move[3], turn_count, white_text)
                        possible = knight_is_capture.capture(board_state)
                        turn_count = knight_is_capture.turn_count
                        if not possible:
                            input('\nThat is an illegal move! Click "Enter" to continue...')
                            print('')
                    elif WHITE_PIECES[move[0]] == white_text.format(ROOK):
                        rook_is_capture = RookAction(move[2], move[3], turn_count, white_text)
                        possible = rook_is_capture.capture(board_state)
                        turn_count = rook_is_capture.turn_count
                        if not possible:
                            input('\nThat is an illegal move! Click "Enter" to continue...')
                            print('')
                    elif WHITE_PIECES[move[0]] == white_text.format(BISHOP):
                        bishop_is_capture = BishopAction(move[2], move[3], turn_count, white_text)
                        possible = bishop_is_capture.capture(board_state)
                        turn_count = bishop_is_capture.turn_count
                        if not possible:
                            input('\nThat is an illegal move! Click "Enter" to continue...')
                            print('')
                    elif WHITE_PIECES[move[0]] == white_text.format(KING):
                        king_is_capture = KingAction(move[2], move[3], turn_count, white_text)
                        possible = king_is_capture.capture(board_state)
                        turn_count = king_is_capture.turn_count
                        if not possible:
                            input('\nThat is an illegal move! Click "Enter" to continue...')
                            print('')
                    elif WHITE_PIECES[move[0]] == white_text.format(QUEEN):
                        queen_is_capture = QueenAction(move[2], move[3], turn_count, white_text)
                        possible = queen_is_capture.capture(board_state)
                        turn_count = queen_is_capture.turn_count
                        if not possible:
                            input('\nThat is an illegal move! Click "Enter" to continue...')
                            print('')
                else:
                    pawn_is_capture = PawnAction(move[2], move[3], turn_count, white_text)
                    possible = pawn_is_capture.capture(board_state)
                    turn_count = pawn_is_capture.turn_count
                    if not possible:
                        input('\nThat is an illegal move! Click "Enter" to continue...')
                        print('')
            elif 'O' in move:
                pass
            elif '+' in move:
                pass
            elif '#' in move:
                pass
            else:
                if move[0] in string.ascii_uppercase:
                    if WHITE_PIECES[move[0]] == white_text.format(KNIGHT):
                        moving_knight = KnightAction(move[1], move[2], turn_count, white_text)
                        possible = moving_knight.move(board_state)
                        turn_count = moving_knight.turn_count
                        if not possible:
                            input('\nThat is an illegal move! Click "Enter" to continue...')
                            print('')
                    elif WHITE_PIECES[move[0]] == white_text.format(ROOK):
                        moving_rook = RookAction(move[1], move[2], turn_count, white_text)
                        possible = moving_rook.move(board_state)
                        turn_count = moving_rook.turn_count
                        if not possible:
                            input('\nThat is an illegal move! Click "Enter" to continue...')
                            print('')
                    elif WHITE_PIECES[move[0]] == white_text.format(BISHOP):
                        moving_bishop = BishopAction(move[1], move[2], turn_count, white_text)
                        possible = moving_bishop.move(board_state)
                        turn_count = moving_bishop.turn_count
                        if not possible:
                            input('\nThat is an illegal move! Click "Enter" to continue...')
                            print('')
                    elif WHITE_PIECES[move[0]] == white_text.format(KING):
                        moving_king = KingAction(move[1], move[2], turn_count, white_text)
                        possible = moving_king.move(board_state)
                        turn_count = moving_king.turn_count
                        if not possible:
                            input('\nThat is an illegal move! Click "Enter" to continue...')
                            print('')
                    elif WHITE_PIECES[move[0]] == white_text.format(QUEEN):
                        moving_queen = QueenAction(move[1], move[2], turn_count, white_text)
                        possible = moving_queen.move(board_state)
                        turn_count = moving_queen.turn_count
                        if not possible:
                            input('\nThat is an illegal move! Click "Enter" to continue...')
                            print('')
                else:
                    moving_pawn = PawnAction(move[0], move[1], turn_count, white_text)
                    possible = moving_pawn.move(board_state)
                    turn_count = moving_pawn.turn_count
                    if not possible:
                            input('\nThat is an illegal move! Click "Enter" to continue...')
                            print('')
            
            if not h and move and possible:
                is_move_possible = False
                while not is_move_possible:
                    random_capture = rc([True, False])
                    random_y = rc(range(len(board_state)))
                    random_x = rc(range(len(board_state)))
                    random_piece = board_state[random_y][random_x]
                    while not random_piece in list(BLACK_PIECES.values()):
                            random_y = rc(range(len(board_state)))
                            random_x = rc(range(len(board_state)))
                            random_piece = board_state[random_y][random_x]
                    random_letter = rc(LETTERS)
                    random_number = rc(NUMBERS)
                    if random_capture:
                        captured_piece = None
                        if random_piece == B_KNIGHT:
                            knight_is_capturing = KnightAction(random_letter, random_number, turn_count, black_text)
                            if knight_is_capturing.capture(board_state):
                                is_move_possible = True
                                captured_piece = knight_is_capturing.capture(board_state)
                        elif random_piece == B_ROOK:
                            rook_is_capturing = RookAction(random_letter, random_number, turn_count, black_text)
                            if rook_is_capturing.capture(board_state):
                                is_move_possible = True
                                captured_piece = rook_is_capturing.capture(board_state)
                        elif random_piece == B_BISHOP:
                            bishop_is_capturing = BishopAction(random_letter, random_number, turn_count, black_text)
                            if bishop_is_capturing.capture(board_state):
                                is_move_possible = True
                                captured_piece = bishop_is_capturing.capture(board_state)
                        elif random_piece == B_KING:
                            king_is_capturing = KingAction(random_letter, random_number, turn_count, black_text)
                            if king_is_capturing.capture(board_state):
                                is_move_possible = True
                                captured_piece = king_is_capturing.capture(board_state)
                        elif random_piece == B_QUEEN:
                            queen_is_capturing = QueenAction(random_letter, random_number, turn_count, black_text)
                            if queen_is_capturing.capture(board_state):
                                is_move_possible = True
                                captured_piece = queen_is_capturing.capture(board_state)
                        elif random_piece == B_PAWN:
                            pawn_is_capturing = PawnAction(random_letter, random_number, turn_count, black_text)
                            if pawn_is_capturing.capture(board_state):
                                is_move_possible = True
                                captured_piece = pawn_is_capturing.capture(board_state)
                        if is_move_possible:
                            print(f'\nBlack responds by capturing {captured_piece}  with {random_piece}  at {random_letter}{random_number}\n')
                        #print(f'{random_piece} at ({random_x}, {random_y}) going to ({random_letter}, {random_number}).')
                    else:
                        if random_piece == B_KNIGHT:
                            moving_knight = KnightAction(random_letter, random_number, turn_count, black_text)
                            if moving_knight.move(board_state):
                                is_move_possible = True
                        elif random_piece == B_ROOK:
                            moving_rook = RookAction(random_letter, random_number, turn_count, black_text)
                            if moving_rook.move(board_state):
                                is_move_possible = True
                        elif random_piece == B_BISHOP:
                            moving_bishop = BishopAction(random_letter, random_number, turn_count, black_text)
                            if moving_bishop.move(board_state):
                                is_move_possible = True
                        elif random_piece == B_KING:
                            moving_king = KingAction(random_letter, random_number, turn_count, black_text)
                            if moving_king.move(board_state):
                                is_move_possible = True
                        elif random_piece == B_QUEEN:
                            moving_queen = QueenAction(random_letter, random_number, turn_count, black_text)
                            if moving_queen.move(board_state):
                                is_move_possible = True
                        elif random_piece == B_PAWN:
                            moving_pawn = PawnAction(random_letter, random_number, turn_count, black_text)
                            if moving_pawn.move(board_state):
                                is_move_possible = True
                        if is_move_possible:
                            print(f'\nBlack responds with {random_piece}  to {random_letter}{random_number}\n')
                        #print(f'{random_piece} at ({random_x}, {random_y}) going to ({random_letter}, {random_number}).')
    elif selection == 'Hi-Score Chart':
        pass
    else:
        input('\n\nThat is not a valid option. Next time, please type one of the two options exactly as they apear. Click "Enter" to continue...')
        valid_selection = False

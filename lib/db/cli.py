import string
from random import choice as rc
from constants import B_ROOK,B_KNIGHT,B_BISHOP,B_QUEEN,B_KING,B_BISHOP,B_KNIGHT,B_ROOK,B_PAWN,KNIGHT,ROOK,BISHOP,QUEEN,KING,PAWN,black_text,white_text,WHITE_PIECES,BLACK_PIECES,LETTERS,NUMBERS
from chess_classes import PawnAction,KnightAction,RookAction,BishopAction,QueenAction,KingAction
from models import Game, User, session

'''valid_login = False
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
    selection = input('Please select an option by typing in the selection here:  ')'''
if True:    
    selection = 'New Game'
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
            elif 'O' in move:
                pass
            elif '+' in move:
                pass
            elif '#' in move:
                pass
            else:
                is_capture = False
                piece_key = 'P'
                (row, column) = (move[0], move[1])
                if move[0] in string.ascii_uppercase:
                    piece_key = move[0]
                    (row, column) = (move[1], move[2])  
                if 'x' in move:
                    is_capture = True
                    (row, column) = (move[2], move[3])             
                piece_to_action = {
                    'N': KnightAction,
                    'R': RookAction,
                    'B': BishopAction,
                    'K': KingAction,
                    'Q': QueenAction,
                    'P': PawnAction
                }
                moving_piece = piece_to_action[piece_key](row, column, turn_count, white_text)
                possible = moving_piece.move(board_state, is_capture)
                turn_count = moving_piece.turn_count
                if not possible:
                    input('\nThat is an illegal move! Click "Enter" to continue...')
                    print('')
            
            if not h and move and possible:
                is_move_possible = False
                while not is_move_possible:
                    random_capture = rc([True, False])                  
                    random_letter = rc(LETTERS)
                    random_number = rc(NUMBERS)
                    random_piece = rc(list(BLACK_PIECES.values()))
                    captured_piece = None
                    piece_to_action = {
                        B_KNIGHT: KnightAction,
                        B_ROOK: RookAction,
                        B_BISHOP: BishopAction,
                        B_KING: KingAction,
                        B_QUEEN: QueenAction,
                        B_PAWN: PawnAction
                    }
                    moving_piece = piece_to_action[random_piece](random_letter, random_number, turn_count, black_text)
                    captured_piece = moving_piece.move(board_state, random_capture)
                    if captured_piece:
                        is_move_possible = True
                    if is_move_possible:
                        print(f'\nBlack responds with {random_piece}  to {random_letter}{random_number}{f" to capture {captured_piece}." if random_capture else "."}\n')
                    print(f' Attempting: Capture is {random_capture}. {random_piece}  going to ({random_letter}, {random_number}).')
    elif selection == 'Hi-Score Chart':
        pass
    else:
        input('\n\nThat is not a valid option. Next time, please type one of the two options exactly as they apear. Click "Enter" to continue...')
        valid_selection = False

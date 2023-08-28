import string
from random import choice as rc
from constants import B_ROOK,B_KNIGHT,B_BISHOP,B_QUEEN,B_KING,B_BISHOP,B_KNIGHT,B_ROOK,B_PAWN,KNIGHT,ROOK,BISHOP,QUEEN,KING,PAWN,black_text,white_text,WHITE_PIECES,BLACK_PIECES,LETTERS,NUMBERS
from chess_classes import PawnAction,KnightAction,RookAction,BishopAction,QueenAction,KingAction
from models import Game, User, HiScoreChart, session

valid_login = False
curr_user = None
while not valid_login:
    input_username = input("\n\nWelcome to Jeremy's CLI Chess Minigame! Play the computer and see how well you can do!\n\n\n" \
                    "If you are new, please enter a unique username (if you are a returning player, type in your username):  ")
    username_output = session.query(User.username).filter(User.username == input_username).first()
    if username_output == None:
        input_password = input("\n\nPlease enter a new password for your account:  ")
        if input_password == None:
            input('\n\nThat is an invalid password! Click "enter" to be returned to the first page...')
            print(' ')
            valid_login = False
        else:
            curr_user = User(username = input_username, password = input_password)
            valid_login = True
    else:
        input_password = input("\n\nPlease enter your password:  ")
        password_output = session.query(User.password).filter(User.username == username_output[0]).first()
        if input_password == password_output[0]:
            curr_user = session.query(User).filter(User.username == username_output[0]).first()
            valid_login = True
        else:
            input('\n\nThat is the wrong password! Click "enter" to be returned to the first page...')
            print(' ')
            valid_login = False
valid_selection = False
while not valid_selection:
    valid_selection = True
    print("\n\n        Welcome to the CLI Chess Minigame Main Menu        \n" \
              "          ___________           _________________          \n" \
              "         |1. New Game|         |2. Hi-Score Chart|         \n" \
              "          ‾‾‾‾‾‾‾‾‾‾‾           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾          \n")
    selection = input('Please type 1 or 2 to make a selection:  ')
    if selection == '1' or selection == 'New Game':
        h = False
        is_win = False
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
                side = None
                if move == 'O-O':
                    side = 'ks'
                    castle_move = KingAction(7, 1, turn_count, white_text)
                    castle = castle_move.castle(side, board_state)
                    if castle:
                        possible = True
                elif move == 'O-O-O':
                    side = 'qs'
                    castle_move = KingAction(7, 5, turn_count, white_text)
                    castle = castle_move.castle(side, board_state)
                    if castle:
                        possible = True
                else:
                    input('\nYour input is not valid! Click "Enter" to continue...')
                    print('')
            elif '+' in move:
                pass
            elif '#' in move:
                is_win = True
                active_game = False
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
                        print(f'\nBlack responds with {random_piece}  to {random_letter}{random_number}{f", capturing your {captured_piece} ." if random_capture else "."}\n')
                    #print(f' Attempting: Capture is {random_capture}. {random_piece}  going to ({random_letter}, {random_number}).')
        if is_win:
            print('\n\nCongratulations, you won!!!')
            print('\nThis game, your number of moves to win, and username will be saved on the Hi Score Chart!')
            new_hi_score = HiScoreChart(user= curr_user, game= new_game, turn_count=new_game.turn_count)
            input('\nPress "Enter" to return to the main menu...')
            valid_selection = False
        else:
            print('The computer won. Try again next time!')
            input('Press "Enter" to return to the main menu...')
            valid_selection = False
    elif selection == '2' or selection == 'Hi-Score Chart':
        more_pages = True
        start = 0
        end = 10
        chart = session.query(HiScoreChart).order_by(HiScoreChart.turn_count).all()
        while more_pages:
            if (end) >= len(chart):
                end = len(chart)
            print(f'\nGames {start+1} - {end} of {len(chart)}.\n')
            print('--------------------------------------')
            print('| User         | Game ID | Turns Won |')
            print('--------------------------------------\n--------------------------------------')
            for i in range(start,end):
                spaces1 = '            '
                for letter in chart[i].username:
                    spaces1 = spaces1.replace(' ', '', 1)
                spaces2 = '       '
                for letter in str(chart[i].game_id):
                    spaces2 = spaces2.replace(' ', '', 1)
                spaces3 = '         '
                for letter in str(chart[i].turn_count):
                    spaces3 = spaces3.replace(' ', '', 1)
                print(f'| {chart[i].username}{spaces1} | {chart[i].game_id}{spaces2} | {chart[i].turn_count}{spaces3} |')
                print('--------------------------------------')
            inp = input('\nSubmit "+" to go to the next page, "-" for the previous page, or "ENTER" to return to the Home Page:  ')
            if inp == '+':
                if end != len(chart):
                    start += 10
                    end += 10
                else:
                    inp = input('\nThat was the last page of Hi Scores. Please submit "-" for the previous page or "Enter" to return to the Home Page:  ')
            if inp == '-':
                if start != 0:
                    start -= 10
                    end -= 10
                else:
                    input('\nThis is the first page of Hi Scores, please press "Enter" to make another selection:  ')
            if inp == '':
                more_pages = False
                valid_selection = False
    else:
        input('\n\nThat is not a valid option. Next time, please type one of the two options exactly as they apear. Click "Enter" to continue...')
        valid_selection = False

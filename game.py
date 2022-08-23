"""A command-line interface version of the classic game IQ Tester"""

# Set width of command-line displays
WIDTH = 45

# Template for a new, full board
NEW_BOARD = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

# JUMPS provides a list of the possible jumps from each hole
# '1': [('2', '4')] -> A peg in '1' can jump a peg in '2' to '4' (if empty)
JUMPS = {
    '1': [('2', '4'), ('3', '6')],
    '2': [('4', '7'), ('5', '9')],
    '3': [('6', 'a'), ('5', '8')],
    '4': [('2', '1'), ('7', 'b'), ('8', 'd'), ('5', '6')],
    '5': [('8', 'c'), ('9', 'e')],
    '6': [('3', '1'), ('5', '4'), ('9', 'd'), ('a', 'f')],
    '7': [('4', '2'), ('8', '9')],
    '8': [('5', '3'), ('9', 'a')],
    '9': [('8', '7'), ('5', '2')],
    'a': [('6', '3'), ('9', '8')],
    'b': [('7', '4'), ('c', 'd')],
    'c': [('8', '5'), ('d', 'e')],
    'd': [('8', '4'), ('9', '6'), ('c', 'b'), ('d', 'f')],
    'e': [('9', '5'), ('d', 'c')],
    'f': [('a', '6'), ('e', 'd')],
}

# MOVES provides a list of all possible moves
# ('1', '2', '4') -> jump from '1' over '2' to '4' AND '4' over '2' to '1'
MOVES = [
    ('1', '2', '4'), ('1', '3', '6'), ('2', '4', '7'), ('3', '6', 'a'),
    ('4', '7', 'b'), ('4', '8', 'd'), ('4', '5', '6'), ('5', '8', 'c'),
    ('5', '9', 'e'), ('6', '9', 'd'), ('6', 'a', 'f'), ('7', '8', '9'),
    ('8', '9', 'a'), ('b', 'c', 'd'), ('c', 'd', 'e'), ('d', 'e', 'f'),
    ('2', '5', '9'), ('3', '5', '8'),
    ]

# use to format command line output
class format:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


def show_board(board, up='0', jumps=[]):
    print()
    print(' IQ TESTER '.center(WIDTH, '-'))
    blank_row = '|' + ''.center(WIDTH - 2) + '|'
    print(blank_row)
    # outer loop iterates once for each row of the board
    for row in range(5):
        # index of first hole in row is the (row)th triangular number
        row_start_idx = int(row * (row + 1) / 2)
        row_display = ''
        width_inc = 0
        # inner loop iterates once for each hole in the current row
        for hole in range(row + 1):
            # set current hole's index, hex value, and peg (boolean)
            hole_idx = row_start_idx + hole
            hex_val = hex(hole_idx + 1)[-1]
            peg = board[hole_idx] == hex_val

            # Evaluate if hole is part of a jump
            #  - landing place: green (with number)
            #  - jumped peg: red (with hex_val)
            landing = jumped = False
            for i, jump in enumerate(jumps):
                if hex_val == jump[1]:
                    landing = True
                    break
                elif hex_val == jump[0]:
                    jumped = True
                    break

            # if peg in hole and it is lifted
            if peg and hex_val == up:
                row_display += format.BLUE + format.BOLD + hex_val + format.END + ' '
                width_inc += 13
            # if peg in hole and it could be jumped
            elif peg and jumped:
                row_display += format.RED + format.BOLD + hex_val + format.END + ' '
                width_inc += 13
            # if no peg in hole and it could be a landing spot for lifted peg
            elif not peg and landing:
                row_display += format.GREEN + format.BOLD + str(i) + format.END + ' '
                width_inc += 13
            # if no peg (and not a landing spot)
            elif not peg and not landing:
                row_display += '  '
            # if peg and cannot be jumped
            elif peg:
                row_display += hex_val + ' '

        # display row
        if width_inc > 0:
            row_display = ' ' + row_display
        print('|' + row_display.center(WIDTH - 2 + width_inc) + '|')

    # finish border
    print(blank_row)
    print(''.center(WIDTH, '-'), '\n')


def remove_one_peg(board):
    print(' BEGIN GAME '.center(WIDTH, '*'), '\n')
    print('The game starts with one empty hole.\n')
    peg = ''
    while peg != ' ' and peg not in board:
        peg = input('>> Which peg would you like to remove? ')
    board[int(peg, 16) - 1] = ' '


def is_game_over(board):
    for move in MOVES:
        # middle hole must have a peg for a valid jump to exist in this move
        if board[int(move[1], 16) - 1] == ' ':
            continue
        # exactly one side hole must have a peg for a valid jump to exist
        left = 0 if board[int(move[0], 16) - 1] == ' ' else 1
        right = 0 if board[int(move[2], 16) - 1] == ' ' else 1
        if left + right == 1:
            return False
    return True


def choose_peg_to_move(board):
    valid_jumps = []
    while True:
        peg = input(' >> What peg would like to move? ')
        potential_jumps = JUMPS[peg]
        for jump in potential_jumps:
            # 'over' must have a peg and 'to' must be empty
            if (board[int(jump[0], 16) - 1] != ' ' and 
                board[int(jump[1], 16) - 1] == ' '):
                valid_jumps.append(jump)
        if valid_jumps:
            break
        print(f'   > There are no valid jumps from {peg}. Try again!')
    return peg, valid_jumps


def pick_jump(jumps):
    hole = '0'
    green = format.GREEN + format.BOLD + 'green' + format.END
    blue = format.BLUE + format.BOLD + 'blue' + format.END
    while True:
        hole = input(f' >> Enter {green} number to place {blue} peg: ')
        try:
            int(hole)
        except ValueError:
            continue
        if 0 <= hole < len(jumps):
            break
    return jumps[hole]


def apply_jump(peg, jump, board):
    # remove peg from lifted location
    board[int(peg, 16) - 1] = ' '
    # remove jumped peg from board
    board[int(jump[0], 16) - 1] = ' '
    # place peg in landing place
    board[int(jump[1], 16) - 1] = jump[1]


def game_over(board):
    print()
    print(" GAME OVER ".center(WIDTH, '*'), end='\n\n')
    remaining = 0
    for hole in board:
        if hole != ' ':
            remaining += 1
    match remaining:
        case 1:
            print('1 peg left. Wow! GENIUS!! 50 points!!')
        case 2:
            print('2 pegs left. Above average! 25 points!')
        case 3:
            print('3 pegs left. Just so-so. 10 points.')
        case _:
            print(f'{remaining} pegs left. Not good. 0 points.')
    print()
    print(" GAME OVER ".center(WIDTH, '*'), end='\n\n')
    quit()


def new_game():
    board = NEW_BOARD.copy()
    show_board(board)
    remove_one_peg(board)
    show_board(board)
    while True:
        if is_game_over(board):
            game_over(board)
        else:
            peg, jumps = choose_peg_to_move(board)
            show_board(board, peg, jumps)
            jump = pick_jump(jumps)
            apply_jump(peg, jump, board)
            show_board(board)


if __name__ == "__main__":
    new_game()

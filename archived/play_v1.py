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
    'd': [('8', '4'), ('9', '6'), ('c', 'b'), ('e', 'f')],
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
class Format:
    formats = {
        'PURPLE': '\033[95m',
        'CYAN': '\033[96m',
        'DARKCYAN': '\033[36m',
        'BLUE': '\033[94m',
        'GREEN': '\033[92m',
        'YELLOW': '\033[93m',
        'RED': '\033[91m',
        'BOLD': '\033[1m',
        'UNDERLINE': '\033[4m',
        'END': '\033[0m',
    }

    def apply(self, text, options=['BOLD']):
        for format in options:
            text = self.formats[format] + text
        return text + self.formats['END']

f = Format()

PROMPT = f.apply('>>', ['BOLD'])

def show_board(board, up='0', jumps=[]):
    print()
    print(' IQ TESTER BOARD '.center(WIDTH, '-'))
    blank_row = '|' + ''.center(WIDTH - 2) + '|'
    print(blank_row)
    print('|' + '/ \\'.center(WIDTH - 2) + '|')
    # outer loop iterates once for each row of the board
    for row in range(5):
        # index of first hole in row is the (row)th triangular number
        row_start_idx = int(row * (row + 1) / 2)
        row_display = '/ '
        width_inc = 0
        formatted_pegs = 0
        # inner loop iterates once for each hole in the current row
        for hole in range(row + 1):
            # set current hole's index, hex value, and peg (boolean)
            hole_idx = row_start_idx + hole
            hex_val = hex(hole_idx + 1)[-1]
            peg = board[hole_idx] == hex_val

            # Check if peg is an option to be jumped
            jumped = False
            for jump in jumps:
                if hex_val == jump[0]:
                    jumped = True
                    break

            # if peg in hole and it is lifted
            if peg and hex_val == up:
                row_display += f.apply(hex_val, ['BOLD', 'BLUE']) + ' '
                width_inc += 13
                formatted_pegs += 1
            # if peg in hole and it could be jumped
            elif peg and jumped:
                row_display += f.apply(hex_val, ['BOLD', 'RED']) + ' '
                width_inc += 13
                formatted_pegs += 1
            # if peg and cannot be jumped
            elif peg:
                row_display += hex_val + ' '
            # if no peg
            else:
                row_display += '  '

        # display row
        row_display += '\\'
        if formatted_pegs % 2 == 1:
            row_display = ' ' + row_display
        print('|' + row_display.center(WIDTH - 2 + width_inc) + '|')

    # finish border
    print('|' + '-------------'.center(WIDTH - 2) + '|')
    print(blank_row)
    print(''.center(WIDTH, '-'), '\n')


def remove_one_peg(board):
    print('The game starts with one empty hole.\n')
    peg = ''
    while peg != ' ' and peg not in board:
        peg = input(f'Which peg would you like to remove? {PROMPT} ')
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
        peg = input(f'What peg would like to move? {PROMPT} ')
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
    red = f.apply('red', ['BOLD', 'RED'])
    while True:
        peg = input(f'Enter {red} number of peg to jump: {PROMPT} ')
        for jump in jumps:
            if peg == jump[0]:
                return jump


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
            result = '1 peg left. Wow! GENIUS!! 50 points!!'
            points = 50
        case 2:
            result = '2 pegs left. Above average! 25 points!'
            points = 25
        case 3:
            result = '3 pegs left. Just so-so. 10 points.'
            points = 10
        case _:
            result = f'{remaining} pegs left. Not good. 0 points.'
            points = 0
    print(f.apply(f'{result}'.center(WIDTH), ['GREEN']))
    print()
    print(''.center(WIDTH, '*'), end='\n\n')
    return points


def new_game():
    print()
    print(' BEGIN GAME '.center(WIDTH, '*'))
    board = NEW_BOARD.copy()
    show_board(board)
    remove_one_peg(board)
    show_board(board)
    while True:
        if is_game_over(board):
            points = game_over(board)
            return points
        else:
            peg, jumps = choose_peg_to_move(board)
            if len(jumps) > 1:
                show_board(board, peg, jumps)
                jump = pick_jump(jumps)
            else:
                jump = jumps[0]
            apply_jump(peg, jump, board)
            show_board(board)


def start():
    total_points = 0
    print()
    print(f.apply(''.center(WIDTH, '*'), ['BOLD']))
    print(f.apply(' WELCOME TO IQ TESTER '.center(WIDTH, '*'), ['BOLD']))
    print(f.apply(''.center(WIDTH, '*'), ['BOLD']), end='\n\n')
    while True:
        print(f.apply(f'>>> Your Total Score: {total_points} <<<'.center(WIDTH), ['BOLD', 'GREEN']))
        print()
        play = input(f'Want to start a new game (y/n)? {PROMPT} ')
        if play in ['y', 'Y', '1']:
            total_points += new_game()
        else:
            quit()

if __name__ == "__main__":
    start()

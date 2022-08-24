import time
from tools.formatter import space
from tools.board import Board


class Game:
    """API for a game of IQ Tester"""

    def __init__(self, formatter):
        self.f = formatter
        self.b = Board(self.f, 5)

    @space
    def header(self):
        self.f.printf(*self.f.bold(' START NEW GAME '.center(self.f.w, "*")))
        print()
        print('Each letter in the board represents a peg in a hole.'.center(self.f.w))

    def remove_one_peg(self):
        peg = ''
        peg = self.f.prompt('The game starts with one empty hole. Pick a peg to remove')
        self.b.remove(peg)

    def pick_peg(self, moves):
        while True:
            pick = self.f.prompt('Choose a peg to move')
            location = self.b.locate_peg(pick)
            if location in moves:
                return location
            else:
                print('* You must choose a red peg from the board. Try again *'.center(self.f.w))

    def pick_jump(self, jumps):
        while True:
            pick = self.f.prompt('Choose the peg you want to jump')
            location = self.b.locate_peg(pick)
            for jump in jumps:
                if jump[0] == location:
                    return jump
            print('* You must choose a green peg from the board to jump over. Try again *'.center(self.f.w))

    def make_jump(self, leaving, jump):
        # Peg leaving from jump[0], jumping over jump[1], landing in jump[2]
        jumping, landing = jump
        peg = self.b.board[leaving[0]][leaving[1]]
        self.b.board[leaving[0]][leaving[1]] = None
        self.b.board[jumping[0]][jumping[1]] = None
        self.b.board[landing[0]][landing[1]] = peg

    def game_over(self):
        self.f.printf(*self.f.bold(' GAME OVER '.center(self.f.w, "*")))
        print()
        left = self.b.pegs_left()
        match left:
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
                result = f'{left} pegs left. Not good. 0 points.'
                points = 0
        self.f.printf(*self.f.apply(f'{result}'.center(self.f.w), ['GREEN']))
        print()
        print(('*' * self.f.w))
        time.sleep(2)
        return points

    def play(self):
        print()
        self.header()
        self.b.show()
        self.remove_one_peg()
        while True:
            moves = self.b.get_moves()
            if len(moves) == 0:
                self.b.show()
                return self.game_over()
            self.b.show(set(moves.keys()))
            pick = self.pick_peg(moves)
            jumps = moves[pick]
            if len(jumps) == 1:
                jump = jumps[0]
            else:
                jumpees = set([jump[0] for jump in jumps])
                self.b.show(jumpees, color='GREEN')
                jump = self.pick_jump(jumps)
            self.make_jump(pick, jump)

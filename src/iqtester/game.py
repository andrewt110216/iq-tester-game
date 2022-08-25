import time
from .formatter import space
from .board import Board


class Game:
    """Manager for a game of IQ Tester"""

    def __init__(self, formatter):
        self.f = formatter
        self.b = Board(self.f, 5)

    @space
    def header(self):
        self.f.center(" START NEW GAME ", fill="*")
        print()
        self.f.center("Each letter in the board represents a peg in a hole.")

    @space
    def invalid(self):
        self.f.center("* Invalid selection. Try again. *")

    def validate(self, peg):
        return len(peg) == 1 and (97 <= ord(peg) < 97 + self.b.holes)

    @space
    def remove_one_peg(self):
        """Ask the user to remove one peg from the board to start the game"""
        peg = ""
        while True:
            peg = self.f.prompt("Pick a peg to remove to start the game")
            if self.validate(peg) and self.b.remove(peg):
                break
            self.invalid()
            print()

    @space
    def pick_peg(self, moves):
        """Ask the user to pick a peg for the next move"""
        while True:
            pick = self.f.prompt("Choose a peg to move")
            if self.validate(pick):
                location = self.b.locate_peg(pick)
                if location in moves:
                    return location
            # invalid pick. highlight possible choices and try again
            self.b.show(moves.keys())
            self.invalid()
            print()
            self.f.center("* The possible pegs to move are highlighted red. *")
            print()

    @space
    def pick_jump(self, jumps):
        """Ask the user to choose which peg they want to jump over"""
        while True:
            pick = self.f.prompt("Choose the peg you want to jump")
            if self.validate(pick):
                location = self.b.locate_peg(pick)
                for jump in jumps:
                    if jump[0] == location:
                        return jump
            self.invalid()

    def make_jump(self, pick, jump):
        """Update the board to reflect the chosen jump"""
        over, to = jump
        peg = self.b.board[pick[0]][pick[1]]
        self.b.board[pick[0]][pick[1]] = None
        self.b.board[over[0]][over[1]] = None
        self.b.board[to[0]][to[1]] = peg

    @space
    def game_over(self):
        """Handle the end of the game and display results"""
        self.f.center(" GAME OVER ", s=["BOLD"], fill="*")
        print()
        left = self.b.pegs_left()
        match left:
            case 1:
                points = 50
                result = "1 peg left. Wow! GENIUS!! 50 points!!"
            case 2:
                points = 25
                result = "2 pegs left. Above average! 25 points!"
            case 3:
                points = 10
                result = "3 pegs left. Just so-so. 10 points."
            case _:
                points = 0
                result = f"{left} pegs left. Not good. 0 points."
        self.f.center(f"{result}", s=["GREEN"])
        print()
        print(("*" * self.f.w))
        time.sleep(1)
        return points

    @space
    def play(self):
        """Drive game sequence"""
        self.header()
        self.b.show()
        self.remove_one_peg()
        while True:
            moves = self.b.get_moves()
            if len(moves) == 0:
                self.b.show()
                return self.game_over()
            self.b.show()
            pick = self.pick_peg(moves)
            jumps = moves[pick]
            if len(jumps) == 1:
                jump = jumps[0]
            else:
                jumpees = set([jump[0] for jump in jumps])
                self.b.show(jumpees, color="GREEN")
                jump = self.pick_jump(jumps)
            self.make_jump(pick, jump)

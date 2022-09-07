from .formatter import space


class Board:
    """Represent the board of the IQ Test game"""

    def __init__(self, formatter, rows):
        self.f = formatter
        self.rows = rows
        self.holes = self.rows * (self.rows + 1) // 2
        self.pegs = [chr(i) for i in range(97, 97 + self.holes)]
        self.board = self.initiate()

    def initiate(self):
        """Create triangular array with peg (letter) in each hole (element)"""
        board = []
        for i in range(self.rows):
            start = i * (i + 1) // 2
            row = [x for x in self.pegs[start: start + i + 1]]
            board.append(row)
        return board

    def pegs_left(self):
        """Tally up the number of remaining pegs on the board"""
        count = 0
        for row in self.board:
            for val in row:
                count += val is not None
        return count

    def locate_peg(self, peg):
        """Search board for peg and return location or None if not found"""
        for i in range(self.rows):
            for j in range(i + 1):
                if self.board[i][j] == peg:
                    return (i, j)
        return None

    @space
    def show(self, highlight=set(), color="RED"):
        """Print board to command line"""
        w = 30
        print(" IQ Tester Board ".center(w - 2, "-").center(self.f.w))
        self.f.center("", in_w=w, in_b="|")

        # iterate over each row of the board
        for i in range(self.rows):
            disp = ""
            fmt_chars = 0
            # iterate over each peg and add it to display string
            for j in range(i + 1):
                val = self.board[i][j]
                # there is a peg in the position
                if val:
                    # check if it should be highlighted
                    if (i, j) in highlight:
                        val, inc = self.f.apply(val, ["BOLD", color])
                        fmt_chars += inc
                    disp += val + " "
                # empty hole
                else:
                    disp += ". "
            # print row
            self.f.center(disp, in_w=w, in_b="|", fc=fmt_chars)

        # finish boarder
        self.f.center("", in_w=w, in_b="|")
        print(("-" * (w - 2)).center(self.f.w))

    def remove(self, peg):
        """Remove peg from the board"""
        for i in range(self.rows):
            for j in range(i + 1):
                if self.board[i][j] == peg:
                    self.board[i][j] = None
                    return True
        return False

    def get_moves(self):
        """Return a list of the possible moves on the board"""
        moves = {}
        # for each hole, check for possible moves, which require a peg in hole,
        # a peg in neighbor, and the landing place to be empty
        for i in range(self.rows):
            for j in range(i + 1):
                if self.board[i][j]:
                    moves[(i, j)] = []
                    # check down-left
                    if (
                        i < self.rows - 2
                        and self.board[i + 1][j]
                        and self.board[i + 2][j] is None
                    ):
                        moves[(i, j)].append(((i + 1, j), (i + 2, j)))
                    # check down-right
                    if (
                        i < self.rows - 2
                        and self.board[i + 1][j + 1]
                        and self.board[i + 2][j + 2] is None
                    ):
                        moves[(i, j)].append(((i + 1, j + 1), (i + 2, j + 2)))
                    # check up-left
                    if (
                        i > 1
                        and j > 1
                        and self.board[i - 1][j - 1]
                        and self.board[i - 2][j - 2] is None
                    ):
                        moves[(i, j)].append(((i - 1, j - 1), (i - 2, j - 2)))
                    # check up-right
                    if (
                        i > 1
                        and j <= i - 2
                        and self.board[i - 1][j]
                        and self.board[i - 2][j] is None
                    ):
                        moves[(i, j)].append(((i - 1, j), (i - 2, j)))
                    # check left
                    if (
                        j > 1
                        and self.board[i][j - 1]
                        and self.board[i][j - 2] is None
                    ):
                        moves[(i, j)].append(((i, j - 1), (i, j - 2)))
                    # check right
                    if (
                        j < i - 1
                        and self.board[i][j + 1]
                        and self.board[i][j + 2] is None
                    ):
                        moves[(i, j)].append(((i, j + 1), (i, j + 2)))
                    # if no moves, remove dictionary key
                    if moves[(i, j)] == []:
                        del moves[(i, j)]
        return moves

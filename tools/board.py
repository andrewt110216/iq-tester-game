from tools.formatter import Formatter, space


class Board:
    """Represent the board of the IQ Test game"""

    def __init__(self, formatter, rows):
        self.f = formatter
        self.rows = rows
        self.holes = self.rows * (self.rows + 1) // 2
        self.pegs = [chr(i) for i in range(97, 97 + self.holes)]
        self.board = self.initiate()

    def initiate(self):
        """Create triangular array with a peg (letter) in each hole (element)"""
        board = []
        for i in range(self.rows):
            start = i * (i + 1) // 2
            row = [x for x in self.pegs[start: start + i + 1]]
            board.append(row)
        return board

    def pegs_left(self):
        count = 0
        for row in self.board:
            for val in row:
                if val:
                    count += 1
        return count

    def locate_peg(self, peg):
        for i in range(self.rows):
            for j in range(i + 1):
                if self.board[i][j] == peg:
                    return (i, j)
        return None

    @space
    def show(self, highlight=set(), color='RED'):
        """Print board to command line"""
        w = 30
        print(' IQ Tester Board '.center(w, '-').center(self.f.w))
        self.f.print_bar(' '.center(w))
        # extract pegs that can be picked or jumped on next move
        for i in range(self.rows):
            disp = ''
            off = 0
            for j in range(i + 1):
                val = self.board[i][j]
                # peg exists and can be picked
                if val and (i, j) in highlight:
                    val, inc = self.f.apply(val, ['BOLD', color])
                    disp += val + ' '
                    off += inc
                # peg exists but cannot be picked
                elif val:
                    disp += val + ' '
                # no peg in hole
                else:
                    disp += '  '
            self.f.print_row(disp, w, i, off > 0)
        self.f.print_bar(' '.center(w))
        print(('-' * w).center(self.f.w))

    def remove(self, peg):
        """Remove peg from the board"""
        for i in range(self.rows):
            for j in range(i + 1):
                if self.board[i][j] == peg:
                    self.board[i][j] = None

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
                    if (i < self.rows - 2 and
                        self.board[i + 1][j] and
                        self.board[i + 2][j] is None):
                        moves[(i, j)].append(((i + 1, j), (i + 2, j)))
                    # check down-right
                    if (i < self.rows - 2 and
                        self.board[i + 1][j + 1] and
                        self.board[i + 2][j + 2] is None):
                        moves[(i, j)].append(((i + 1, j + 1), (i + 2, j + 2)))
                    # check up-left
                    if (i > 1 and j > 1 and
                        self.board[i - 1][j - 1] and
                        self.board[i - 2][j - 2] is None):
                        moves[(i, j)].append(((i - 1, j - 1), (i - 2, j - 2)))
                    # check up-right
                    if (i > 1 and j <= i - 2 and
                        self.board[i - 1][j] and
                        self.board[i - 2][j] is None):
                        moves[(i, j)].append(((i - 1, j), (i - 2, j)))
                    # check left
                    if (j > 1 and
                        self.board[i][j - 1] and
                        self.board[i][j - 2] is None):
                        moves[(i, j)].append(((i, j - 1), (i, j - 2)))
                    # check right
                    if (j < i - 1 and
                        self.board[i][j + 1] and
                        self.board[i][j + 2] is None):
                        moves[(i, j)].append(((i, j + 1), (i, j + 2)))
                    # if no moves, remove dictionary key
                    if moves[(i, j)] == []:
                        del moves[(i, j)]
        return moves

if __name__ == "__main__":
    f = Formatter(79)
    b = Board(f)
    for row in b.board:
        print(row)
    b.show()

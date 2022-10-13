from collections import defaultdict
from typing import Dict, List, Set, Tuple
from .formatter import space, Formatter


# === Type Aliases & Explanations ===

# A peg is represented by a single character (string of length 1), where ""
# represents an empty hole
Peg = str

# The board is a 2D-array, where each element of the inner list corresponds to
# the value of the hole at that location on the board
BoardMatrix = List[List[Peg]]

# The coordinates to access a certain location on the board are represented as
# a tuple where index 0 is the row index and index 1 is the column index
BoardLocation = Tuple[int, int]

# The location of a given Peg (or whether or not it is still on the board) can
# be determined in O(1) time using a PegsMap, mapping each peg to its location
PegsMap = Dict[Peg, BoardLocation]

# A move for a certain Peg is represented as a tuple where index 0 is the
# BoardLocation of the Peg to be jumped over and index 1 is the BoardLocation
# of where the Peg lands
Jump = Tuple[BoardLocation, BoardLocation]

# All possible moves for a given board configuration can be represented by a
# dictionary mapping each Peg to a list of its possible Jumps
MovesMap = Dict[Peg, List[Jump]]

class Board:
    """Manager of the board for a game of IQ Tester"""

    # Set the minimum and maximum number of rows allowed in a board
    MIN_ROWS = 1
    MAX_ROWS = 7

    def __init__(self, rows: int, f: Formatter) -> None:

        # The Formatter instance used to format print statements
        self.f = f

        # Validate and store the number of rows in the board
        if not self.MIN_ROWS <= rows <= self.MAX_ROWS:
            raise NotImplementedError(
                f"rows must be in [{self.MIN_ROWS}:{self.MAX_ROWS}] not {rows}"
            )
        self.num_rows = rows

        # The number of holes in the board is equal to the (num_rows)th
        # triangular number = n * (n + 1) / 2
        # Use // to cast to int
        self.num_holes = self.num_rows * (self.num_rows + 1) // 2

        # Map each peg character to its current location on the board
        self.peg_locations_map: PegsMap = {}

        # Map each peg character to a list of its current possible jumps
        # Initially, there are no possible moves for a full board
        # The MovesMap is recalculated any time the board state changes by
        # the _update_moves_map method
        self.moves_map: MovesMap = {}

        # Board is a 2D array, where each row represents a hole on the board
        # and each element is either a peg (peg_char) or 0 (empty hole)
        self.board: BoardMatrix = self.initiate()

    def _is_location_valid(self, i: int, j: int) -> bool:
        """Return True if i, j are valid row, column indices, respectively"""

        # Row references must be in the range: [0, number of rows)
        # Col references must be in the range: [0, row index]
        return 0 <= i < self.num_rows and 0 <= j <= i

    def initiate(self) -> BoardMatrix:
        """Return a board (2D array) with a peg character in each hole"""

        # Generate a list of the characters to be used as pegs
        peg_chars = [chr(i) for i in range(97, 97 + self.num_holes)]

        # Generate and add one row at a time to the board
        board: BoardMatrix = []
        for i in range(self.num_rows):

            # Calculate the index of the first peg character for this row
            row_start_peg_idx = i * (i + 1) // 2

            # Process one peg in the row at a time
            current_row = []
            for j in range(i + 1):

                # Get peg character, insert into current row, and add to map
                peg_char = peg_chars[row_start_peg_idx + j]
                current_row.append(peg_char)
                self.peg_locations_map[peg_char] = (i, j)

            # Append current row to board
            board.append(current_row)

        return board

    def number_of_pegs(self) -> int:
        """Return the number of pegs remaining on the board"""

        # The number of pegs is just the number of keys in the PegsMap
        return len(self.peg_locations_map)

    def remove_peg(self, peg: Peg) -> None:
        """Remove peg from the board if it is on the board"""

        # Make sure peg is in board by checking PegsMap
        if peg in self.peg_locations_map:

            # Remove peg from board and update PegsMap
            peg_location = self.peg_locations_map[peg]
            self.board[peg_location[0]][peg_location[1]] = ""
            del self.peg_locations_map[peg]

            # Refresh moves map attribute
            self._update_moves_map()

    def make_move(self, peg: Peg, jump: Jump) -> None:
        """
        Update the board's state for the move represented by peg and jump

        Parameters
        ----------
        peg : Peg
            The peg that is to be moved
        jump : Jump
            The jump that peg is to make
        """

        # Remove peg from its current location
        peg_location: BoardLocation = self.peg_locations_map[peg]
        self.board[peg_location[0]][peg_location[1]] = ""

        # Get the peg that is being jumped and its location
        jumped_location: BoardLocation = jump[0]
        jumped_peg: Peg = self.board[jumped_location[0]][jumped_location[1]]

        # Remove the jumped peg from the board
        self.board[jumped_location[0]][jumped_location[1]] = ""

        # Remove the jumped peg from the PegsMap
        del self.peg_locations_map[jumped_peg]

        # Set peg in the jump's landing location
        landing_location: BoardLocation = jump[1]
        self.board[landing_location[0]][landing_location[1]] = peg

        # Update pegs location in the PegsMap
        self.peg_locations_map[peg] = landing_location

        # Refresh moves map attribute
        self._update_moves_map()

    def _update_moves_map(self) -> None:
        """
        Generate a MovesMap, dictionary mapping every peg on the board a list
        of its current possible jumps, and set it as the moves_map attribute

        This method should be called any time the board state changes in order
        to maintain the moves_map attribute

        Time Complexity: O(m) where m is the number of pegs on the board
        """

        # Initialize a new MovesMap with empty lists as default values
        current_moves_map: MovesMap = defaultdict(list)

        # Reference diagram of board indices:
        # Row Index  Column Index
        #     0           0
        #     1          0 1
        #     2         0 1 2
        #     3        0 1 2 3
        #     4       0 1 2 3 4

        # Define each "direction" from peg's location (i, j) as a tuple, such
        # that the adjacent hole location is: (i + row offset, j + col offset)
        directions = [
            (1, 0),     # Down and left
            (1, 1),     # Down and right
            (-1, -1),   # Up and left
            (-1, 0),    # Up and right
            (0, -1),    # Left
            (0, 1),     # Right
        ]

        # Iterate over each peg on the board
        for peg, location in self.peg_locations_map.items():

            # Get row and column indices for location
            i, j = location

            # Check in each direction for possible jumps
            for row_offset, col_offset in directions:

                # Define the "jumped" and "landing" locations in direction
                jumped_i, landing_i = i + row_offset, i + row_offset * 2
                jumped_j, landing_j = j + col_offset, j + col_offset * 2

                # Validate jumped and landing locations
                if (
                    not self._is_location_valid(jumped_i, jumped_j)
                    or not self._is_location_valid(landing_i, landing_j)
                ):
                    # Peg cannot jump in this direction
                    continue

                # A jump is possible if there is a peg in the jumped location
                # and the landing location is empty
                if (
                    self.board[jumped_i][jumped_j]
                    and not self.board[landing_i][landing_j]
                ):
                    # Add this jump for peg to MovesMap
                    jump = ((jumped_i, jumped_j), (landing_i, landing_j))
                    current_moves_map[peg].append(jump)

        # Update instance attribute with new MovesMap
        self.moves_map = current_moves_map

    @space
    def print_board(
        self,
        highlight_pegs: Set[Peg] = set(),
        color: str = "RED"
    ) -> None:
        """
        Print the board to the command line, optionally formatting certain pegs

        Parameters
        ----------
        highlight_pegs : Set[Pegs]
            A set of pegs to be highlighted with color
        color : str
            The style code of the color used to highlight `highlight_pegs`
            For options, see Formatter class
        """

        # Set width of box to contain the board
        width = 30

        # Print header row followed by empty row
        print(" IQ Tester Board ".center(width - 2, "-").center(self.f.width))
        self.f.center("", inner_width=width, inner_border_char="|")

        # Iterate over each row of the board
        for i in range(self.num_rows):

            # Assemble ouput string and count format characters
            output = ""
            format_chars = 0

            # Iterate over each peg and add it to output string
            for j in range(i + 1):

                hole_value = self.board[i][j]

                # Handle case that there is a peg at this location
                if hole_value:

                    # Check if it should be highlighted
                    if hole_value in highlight_pegs:

                        # Add formatting and increment format character count
                        hole_value, inc_format_chars = self.f.apply_formatting(
                            hole_value,
                            ["BOLD", color]
                        )
                        format_chars += inc_format_chars

                    # Add hole value to output string
                    output += hole_value + " "

                # Handle case of empty hole
                else:

                    # Add period to output string
                    output += ". "

            # Print current row of board
            self.f.center(
                output,
                inner_width=width,
                inner_border_char="|",
                format_char_count=format_chars
            )

        # Finish border of box
        self.f.center("", inner_width=width, inner_border_char="|")
        print(("-" * (width - 2)).center(self.f.width))

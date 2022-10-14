from typing import Dict, List, Set, Tuple
import time
import copy
from .formatter import space, Formatter
from .board import Board, BoardLocation, Jump, Move, Peg


class Game:
    """Manager for a game of IQ Tester"""

    def __init__(
        self,
        f: Formatter,
        size: int = 5,
        pause: float = 2,
        msg_pause: float = 0.75
    ) -> None:

        # The Formatter instance used to format print statements
        self.f = f

        # The game board
        self.b = Board(size, self.f)

        # Store a list of previous states of the board, with the most recent
        # state at the end of the list
        self.previous_board_states: List[Board] = []

        # Setting for length (in seconds) of pause after game over
        self.pause = pause

        # Setting for length (in seconds) of pause when certain messages are
        # displayed, like invalid selection or updated settings
        self.msg_pause = msg_pause

    def play(self) -> int:
        """Initiate and handle the game logic"""

        # Display New Game header
        self.print_new_game_header()

        # Print initial board
        self.b.print_board()

        # Prompt user to remove one peg
        self.remove_one_peg()

        # Gameplay loop
        while True:

            # Print current status of board
            self.b.print_board()

            # Check if game is over (i.e. no possible moves)
            if not self.b.moves_map:
                return self.game_over()

            # Prompt user to pick a peg to move
            peg: Peg = self.choose_peg_to_move()

            # Handle user selection to quit and return to session
            if peg == '!':
                return -1

            # Handle case of only a single possible jump for peg
            jump: Jump
            if len(self.b.moves_map[peg]) == 1:
                jump = self.b.moves_map[peg][0]

            # Handle case of multiple possible jumps for peg
            else:

                # Prompt user to choose a jump from the possible jumps
                jump = self.choose_jump_for_peg(peg)

            # Save the current state of the board before executing the move
            self.save_state()

            # Make the move, consisting of the chosen peg and chosen jump
            self.b.make_move(peg, jump)

    @space
    def print_new_game_header(self) -> None:
        """Print header rows for a new game"""
        self.f.center(" START NEW GAME ", fill_char="*", end="\n\n")
        self.f.center("Each letter in the board represents a peg in a hole.")

    def remove_one_peg(self) -> None:
        """Prompt user to choose one peg to remove from the board to start"""

        # Infinite loop to re-prompt until input is valid
        while True:

            # Prompt user to choose a peg
            self.f.center("The game begins with one hole on the board empty.")
            user_input = self.f.prompt("Choose a peg to remove to start")

            # Handle case of valid selection
            if user_input in self.b.peg_locations_map:
                self.b.remove_peg(user_input)
                return

            # Handle case of invalid selection
            self.invalid()

    def choose_peg_to_move(self) -> Peg:
        """Prompt user to choose a peg to move"""

        # Inifinte loop to re-prompt until input is valid
        while True:

            # Print list of special options and prompt user
            self.f.center(
                "Options: Undo Last Move ('.') | Hint ('>') | Quit Game ('!')",
                ["RED"],
            )
            user_input = self.f.prompt(
                "Input an option or choose a peg to move"
            )

            # Handle special options
            if user_input == '.':
                self.revert_state()
                self.b.print_board()
            elif user_input == '>':
                self.show_hint()
            elif user_input == '!':
                return user_input

            # Handle case of valid peg selection with possible moves
            elif (
                user_input in self.b.peg_locations_map
                and self.b.moves_map[user_input]
            ):
                return user_input

            # Handle case of invalid user input
            else:
                # Notify user of invalid input
                self.invalid()

                # Get list of pegs that could be moved
                pegs_that_can_move = {
                    peg for peg, jumps in self.b.moves_map.items() if jumps
                }

                # Print the board, highlighting the pegs that can be moved
                self.b.print_board(pegs_that_can_move)
                self.f.center(
                    "* Only highlighted pegs can move *",
                    ["RED"],
                    end="\n\n"
                )

    @space
    def choose_jump_for_peg(self, peg: Peg) -> Jump:
        """Prompt user to choose one of multiple possible jumps for peg"""

        # Initialize an empty set to store the possible pegs to jump over
        possible_pegs_to_jump: Set[Peg] = set()

        # Initialize dictionary mapping each peg to be jumped to its jump index
        peg_to_jump_to_index_map: Dict[Peg, int] = {}

        # Iterate over possible jumps to populate above two data structures
        for i, jump in enumerate(self.b.moves_map[peg]):
            location_jumped: BoardLocation = jump[0]
            peg_to_jump = self.b.board[location_jumped[0]][location_jumped[1]]
            peg_to_jump_to_index_map[peg_to_jump] = i
            possible_pegs_to_jump.add(peg_to_jump)

        # Print board, highlighting possible pegs to be jumped over
        self.b.print_board(possible_pegs_to_jump, "BOLD")

        # Inifinte loop to re-prompt until input is valid
        while True:

            # Ask user to select the peg to be jumped over
            self.f.center(f"* {peg} can jump over the bold pegs *")
            user_input = self.f.prompt("Choose the peg to jump over")

            # Handle case of valid selection
            if user_input in possible_pegs_to_jump:

                # Return the jump corresponding to the chosen peg to be jumped
                possible_moves = self.b.moves_map[peg]
                return possible_moves[peg_to_jump_to_index_map[user_input]]

            # Notify user of invalid input
            self.invalid()

    def revert_state(self) -> None:
        """Undo the last move by reverting the board to its previous state"""

        # Handle case of no previous states
        if not self.previous_board_states:
            print()
            self.f.center("* Unable to go back *", end="\n\n")
            return

        # Pop most recent board state and make it the current board
        self.b = self.previous_board_states.pop()

    def invalid(self) -> None:
        """Print message notifying the user of an invalid selection"""
        self.f.center("* Invalid selection. Try again. *", end="\n\n")
        time.sleep(self.msg_pause)

    def save_state(self) -> None:
        """Make a deep copy of the board and add it to previous_board_states"""
        board_copy: Board = copy.deepcopy(self.b)
        self.previous_board_states.append(board_copy)

    def show_hint(self) -> None:
        """Get optimal solution for current board and display to user"""

        # Warn user about possible wait time
        num_pegs = self.b.number_of_pegs()

        # Handle case of too many pegs to solve in under a minute
        MAX = 13
        if num_pegs > MAX:
            msg = f"* Hints are disabled for over {MAX} pegs due to run time *"
            self.f.center(msg)
            time.sleep(self.msg_pause)
            self.b.print_board()
            return

        # Handle case of long estimated time to solve
        elif num_pegs > 11:

            # Map number of remaining pegs to estimated time to solve
            time_estimates = {
                13: 40,
                12: 10,
                11: 3,
            }

            seconds = time_estimates[num_pegs]
            msg = f"* It may take up to {seconds} seconds to calculate " + \
                  f"the optimal solution for {num_pegs} pegs *"
            self.f.center(msg, ["RED"])
            key = self.f.prompt("Input 'x' to cancel or any key to continue")
            if key.lower() == 'x':
                self.b.print_board()
                return

        # Request optimal solution from board instance and unpack
        solution: Tuple[int, List[Move]] = self.b.solve()
        opt_res: int = solution[0]
        opt_moves: List[Move] = solution[1]

        # Extract first move details from optimal moves
        first_move: Move = opt_moves[0]
        peg: Peg = first_move[0]
        jump: Jump = first_move[1]
        peg_jumped: Peg = self.b.board[jump[0][0]][jump[0][1]]

        # Display board and provide hint to user
        self.b.print_board({peg, peg_jumped}, "GREEN")
        if opt_res == 1:
             self.f.center(
                f"You still have a chance to leave just 1 peg!",
                ["GREEN"],
            )
        else:
            self.f.center(
                f"The best you can do is leave {opt_res} pegs.",
                ["GREEN"],
            )
        self.f.center(
            f"* Hint: Jump '{peg}' over '{peg_jumped}' *",
            ["GREEN"],
            end="\n\n"
        )

    @space
    def game_over(self) -> int:
        """Manage end of game and return points earned this game"""

        # Notify user that game is over
        self.f.center(" GAME OVER ", ["BOLD"], "*", end="\n\n")

        # Get number of pegs left on board and handle each case
        num_pegs = self.b.number_of_pegs()

        if num_pegs == 1:
            points = 50
            result = "1 peg left. Wow! GENIUS!! 50 points!!"
        elif num_pegs == 2:
            points = 25
            result = "2 pegs left. Above average! 25 points!"
        elif num_pegs == 3:
            points = 10
            result = "3 pegs left. Just so-so. 10 points."
        else:
            points = 0
            result = f"{num_pegs} pegs left. Not good. 0 points."

        # Notify user of result
        self.f.center(result, ["GREEN"], end="\n\n")
        print(("*" * self.f.width))

        # Pause before returning number of points earned this game
        time.sleep(self.pause)
        return points

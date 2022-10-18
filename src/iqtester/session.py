from typing import Generator, List, Optional, Sequence, Tuple
import time
from .formatter import Formatter, space
from .game import Game


class Session:
    """Manager of a session of play for the game IQ Tester"""

    def __init__(self, width: int = 78, msg_pause: float = 0.75) -> None:

        # Initialize the attribute to store instances of Game
        self.game: Optional[Game] = None

        # Initialize session statistics
        self.played = 0
        self.total_score = 0

        # Initialize session settings
        self.board_size = 5
        self.prompt_color = "BLUE"
        self.menu_width = 40
        self.menu_side_border = '|'
        self.menu_top_border = '-'
        self.game_over_pause = 1.25
        self.msg_pause = msg_pause

        # To make a setting customizable, add it to settings menu map and add
        # it to the settings_test_args_map in test_session_settings.py
        # key: user input to select on settings menu
        # value: (attribute name, description, type, lower bound, upper bound)
        colors = {"BLUE", "RED", "GREEN", "BLACK", "GRAY"}  # See formatter.py
        times = (0.0, 3.01, 0.01)
        chars = {'|', '*', '-', '.', '~', 'x'}
        self.settings_menu_map = {
            "b": ('board_size', 'Board Size', int, (4, 7, 1)),
            "c": ('prompt_color', 'Prompt Color', str, colors),
            "p": ('game_over_pause', 'Game Over Pause Time', float, times),
            "m": ('msg_pause', 'Message Pause Time', float, times),
            "s": ('menu_side_border', 'Menu Side Borders', str, chars),
            "t": ('menu_top_border', 'Menu Top/Bottom Borders', str, chars),
            "w": ('menu_width', 'Menu Width', int, (40, 79, 1)),
        }

        # Create a Formatter object to manage formats of statements to stdout
        self.f_width = width
        self.f = Formatter(self.f_width, self.prompt_color)

    def get_average(self) -> float:
        """Return the average points per game for this session"""
        if self.played == 0:
            return round(0, 1)
        return round(self.total_score / self.played, 1)

    def start(self) -> None:
        """Initiate and manage a new session of games"""

        self.print_new_session_header()

        # Infinite loop to keep playing until user quits
        selection_prompt = "Select a menu option"
        while True:

            self.main_menu()
            main_choice = self.f.prompt(selection_prompt).lower()

            # Handle selection to start new game
            if main_choice == "":
                self.game = Game(
                    self.f, self.board_size, self.game_over_pause,
                    self.msg_pause
                )
                game_score = self.game.play()

                # Handle user selection to quit mid-game
                if game_score == -1:
                    continue

                # Update session statistics
                self.total_score += game_score
                self.played += 1

            # Handle selection to go to settings menu
            elif main_choice == "s":

                # Ininite loop on settings menu until user returns to main menu
                while True:
                    self.settings_menu()
                    setting = self.f.prompt(selection_prompt).lower()

                    # Handle valid menu selection
                    if setting in self.settings_menu_map:
                        self.update_setting(*self.settings_menu_map[setting])

                        # Create new Formatter object in case settings changed
                        self.f = Formatter(self.f_width, self.prompt_color)

                    # Handle return to main menu
                    else:
                        self.f.center("Returning to Main Menu...")
                        time.sleep(self.msg_pause)
                        break

            # Treat any other input as choice to quit
            else:
                break

        # Handle quit
        self.f.center("Thanks for playing!", ['BOLD'])
        self.print_footer()

    @space
    def main_menu(self) -> None:
        """Display the main menu including statistics and gameplay options"""

        width = self.menu_width
        border = self.menu_side_border

        self.print_menu_top("MAIN MENU", width, border)

        # Game statistics rows
        stats = [
            ("GAMES PLAYED: ", str(self.played)),
            ("YOUR TOTAL SCORE: ", f"{self.total_score:,}"),
            ("AVERAGE SCORE: ", f"{self.get_average():,}"),
        ]

        # Menu options
        opts = [
            ("New Game", "[ENTER]"),
            ("Settings Menu", "[s]"),
            ("Quit", "[q]"),
        ]

        # Find maximum label length and value length between both blocks
        lens_stats = max_element_lens(stats)
        lens_options = max_element_lens(opts)
        left, right = [max(x) for x in zip(lens_stats, lens_options)]
        left += 2

        # Print each block
        formats = ['BOLD', 'GREEN']
        self.print_menu_block(stats, formats, width, left, right, border)
        self.print_menu_space(width, border)
        formats = ['BOLD', 'RED']
        self.print_menu_block(opts, formats, width, left, right, border, '.')

        self.print_menu_bottom(width, border)

    @space
    def settings_menu(self) -> None:
        """Display settings menu and allow user to change settings"""

        width = self.menu_width
        border = self.menu_side_border

        self.print_menu_top("SETTINGS MENU", width, border)

        # Generate row labels & values from settings menu map
        opts = []
        for key, args in self.settings_menu_map.items():
            # [Setting Label] ([Current Value])
            label = f"{args[1]} ({getattr(self, args[0])})"
            value = f"[{key}]"
            opts.append((label, value))

        opts.append(("Return to Main Menu", "[r]"))

        left, right = max_element_lens(opts)
        left += 2

        formats = ['BOLD', 'RED']
        self.print_menu_block(opts, formats, width, left, right, border, '.')

        self.print_menu_bottom(width, border)

    def print_menu_top(self, header: str, width: int, border: str) -> None:
        """Print the top of a menu including its header with a border"""
        self.f.center("", [], self.menu_top_border, width - 2)
        self.print_menu_space(width, border)
        self.f.center(f"{header}", ['BOLD'], " ", width, border)
        self.print_menu_space(width, border)

    def print_menu_bottom(self, width: int, border: str) -> None:
        """Print the top of a menu including its header with a border"""
        self.print_menu_space(width, border)
        self.f.center("", [], self.menu_top_border, width - 2)

    def print_menu_space(self, width: int, border: str) -> None:
        """Print a blank row of a menu box"""
        self.f.center("", inner_width=width, inner_border_char=border)

    def print_menu_block(
        self,
        rows_label_value: List[Tuple[str, str]],
        formats: List[str],
        width: int,
        left_just: int,
        right_just: int,
        border: str,
        fill_char: str = " ",
    ) -> None:
        """
        Print a block of menu options of a menu box with proper alignment

        Parameters
        ----------
        rows_label_value : List[Tuple[str, str]]
            Strings to be printed on the left and right side of each row
        formats : List[str]
            Format codes to be applied (see Formatter class for options)
        width : int
            Width of menu box
        border : str
            Border character for left and right sides of menu
        fill_char : str
            Fill character printed between right and left sides of row
        """

        # Print each row with formatting and proper alignment
        for label, value in rows_label_value:
            display = f"{label:{fill_char}<{left_just}}"
            display += f"{value:{fill_char}>{right_just}}"
            self.f.center(display, formats, " ", width, border)

    def update_setting(
        self,
        name: str,
        desc: str,
        type: type,
        options,    # See below for typing options
    ) -> None:
        """
        Prompt user to update a setting, validate input, and make update

        Parameters
        ----------
        name : str
            Name of attribute for the setting (e.g. 'board_size')
        desc : str
            Description of setting (e.g. 'Board Size')
        type : type
            Type of value for setting (e.g. int)
        options: Tuple[int] | Tuple[float] | Set[str]
            Defines the allowable values for setting
            Range or Frange defines (start, stop, step) of allowable numbers
            Set provides all allowable values
        """

        # Options is a tuple defining a range
        was_tuple = False
        if isinstance(options, tuple):
            was_tuple = True
            start, stop, step = options
            last = stop - step
            prompt = f"Enter desired {desc} between {start} and {last}:"
            range_msg = f"{desc} must be between {start} and {last}"

        # Options is a set of the possible values
        elif isinstance(options, set):
            prompt = f"Enter desired {desc} from {options}:"
            range_msg = f"{desc} must be in {options}"

        type_msg = f"{desc} must of {str(type)}"

        # Infinite loop to re-prompt until input is valid
        while True:

            # Options was a tuple: create fresh range or frange each loop
            if was_tuple and isinstance(start, int):
                options = range(start, stop, step)
            elif was_tuple and isinstance(start, float):
                options = frange(start, stop, step)

            user_input = self.f.prompt(prompt)

            # Validate input
            try:
                user_input = type(user_input)
                if user_input in options:
                    break
                self.f.center(f"* {range_msg}. Try again. *", ["RED"])

            # Handle input of wrong type
            except (TypeError, ValueError, NameError):
                self.f.center(f"* {type_msg}. Try again. *", ["RED"])

        # Update setting
        self.f.center(f"Updating {desc} to {user_input}...", end="\n\n")
        setattr(self, name, user_input)
        time.sleep(self.msg_pause)

    @space
    def print_new_session_header(self) -> None:
        """Print header and instructions for a new session"""
        self.f.center('', ["BOLD", "BLUE"], '*')
        self.f.center(' WELCOME TO IQ TESTER ', ["BOLD"], '*')
        self.f.center('', ["BOLD", "BLUE"], '*', end="\n\n")
        self.f.center("Start with any one hole empty.")
        self.f.center("As you jump the pegs remove them from the board.")
        self.f.center("Try to leave only one peg. See how you rate!")

    @space
    def print_footer(self) -> None:
        """Print footer rows for a session"""
        self.f.center("For even more fun compete with someone. Lots of luck!")
        self.f.center("Copyright (C) 1975 Venture MFG. Co., INC. U.S.A.")
        self.f.center("Python package `iqtester` by Andrew Tracey, 2022.")
        self.f.center("Follow me: https://www.github.com/andrewt110216")


def max_element_lens(sequences: Sequence[Sequence[str]]) -> List[int]:
    """
    For a sequence of sequences of strings, return the lengths of the
    longest strings at each position in the inner sequences

    Example
    -------
    >>> sequences = [('Apple', '1,345'), ('Watermelon', '512'), ('a', '1')]
    >>> print(max_lens(sequences))
    [10, 5]
    """

    out = []

    for elements in zip(*sequences):

        # Find element in elements with max length
        longest = max(elements, key=lambda x: len(x))

        # Append its length to out
        out.append(len(longest))

    return out


def frange(start: float, stop: float = None, step: float = 1.0) -> Generator:
    """Generator like built-in range but allowing for floating point values"""

    # If stop is not defined, assume start is 0 and stop is start
    if stop is None:
        stop = start
        start = 0.0

    count = 0
    while True:
        temp = float(start + count * step)
        if step > 0 and temp >= stop:
            break
        elif step < 0 and temp <= stop:
            break
        yield round(temp, 2)
        count += 1
